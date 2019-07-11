from plumbum import local
from plumbum.cmd import mkdir
from datetime import datetime
from distutils.util import strtobool
import re
import boto
import sys
import os

from openvpn_cert_generator.utils.md5sum_dir import md5sum_dir


def init_s3_connection(region):
    return boto.s3.connect_to_region(region)


def parse_s3_url(full_path):
    _, path = re.split('\:\/+', full_path, 1)
    try:
        bucket, bucket_path = path.split('/')
    except ValueError:
        bucket = path
        bucket_path = ''
    return [bucket, bucket_path]


def list_dirs_from_path(conn, full_path):
    bucket, prefix = parse_s3_url(full_path)
    return (key.name for key in conn.get_bucket(bucket).list(prefix, '/'))


def get_latest_dir_from_root_path(conn, full_path):
    dir_list = sorted(list_dirs_from_path(conn, full_path), reverse=True)
    if dir_list:
        return dir_list[0]
    else:
        return ''


def pull_latest_certs_from_root_path(conn, settings):
    full_path = settings['S3_CERT_ROOT_PATH']
    dest_dir = settings['KEY_DIR']
    dir_override = settings['S3_DIR_OVERRIDE']

    if dir_override:
        remote_target_dir = dir_override.rstrip('/') + '/'
    else:
        remote_target_dir = get_latest_dir_from_root_path(conn, full_path)

    mkdir.run(['-p', dest_dir], retcode=0)
    if remote_target_dir:
        with local.env(**settings):
            awscli = local['/usr/local/bin/aws']
            bucket, prefix = parse_s3_url(full_path)
            s3_path = "s3://{}/{}{}".format(bucket, prefix, remote_target_dir)
            awscli.run(['s3', 'cp', s3_path, dest_dir, '--recursive'],
                       retcode=0, stderr=sys.stdout)


def push_certs_to_root_path(conn, settings):
    # check if we need to upload
    full_path = settings['S3_CERT_ROOT_PATH']
    certs_dir = settings['KEY_DIR']
    dry_run = strtobool(settings.get('S3_PUSH_DRYRUN', 'false'))

    existing_shas = []
    for entry in list_dirs_from_path(conn, full_path):
        if len(entry.split('-', 2)) > 2:
            existing_shas.append(entry.split('-', 2)[2].strip('/'))

    certs_dir_sha = md5sum_dir(certs_dir.encode('utf-8'))
    if certs_dir_sha in existing_shas:
        print('SHA: {} already exists in s3. Aborting upload'.format(certs_dir_sha))
        sys.exit(0)
    else:
        new_dir_name = '{}-{}/'.format(datetime.utcnow().strftime("%Y%m%d-%H%M%SZ"), certs_dir_sha)
        s3_path = os.path.join(full_path, new_dir_name)
        awscli = local['/usr/local/bin/aws']

        print('Uploading certs to {}'.format(s3_path))
        params = ['s3', 'cp', certs_dir, s3_path, '--recursive']
        if dry_run:
            params.append('--dryrun')
        awscli.run(params, retcode=0, stdout=sys.stdout, stderr=sys.stdout)
