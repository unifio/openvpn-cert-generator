from plumbum import local
from plumbum.cmd import mkdir, rm, touch
from glob import glob
from distutils.util import strtobool
import os
import sys


def build_server(settings):
    force = strtobool(settings.get('FORCE_CERT_REGEN', 'false'))
    with local.env(**settings):
        pkitool = local[os.path.join(local.env['EASY_RSA'], 'pkitool')]
        openssl = local['openssl']

        if force:
            print('FORCE_CERT_REGEN=true, regenerating {}'.format(local.env['KEY_DIR']))
            rm(['-rf', local.env['KEY_DIR']])

        if not local.path(local.env['KEY_DIR']).exists():
            print('KEY_DIR does not exist, creating')
            mkdir.run(['-p', local.env['KEY_DIR']], retcode=0)
            # see if this needs to be separate
            touch(os.path.join(local.env['KEY_DIR'], 'index.txt'), retcode=0)
            with open(os.path.join(local.env['KEY_DIR'], 'serial'),
                      'w') as serial:
                serial.write('01')

        ca_files = glob(os.path.join(local.env['KEY_DIR'], 'ca.*'))
        server_files = glob(os.path.join(local.env['KEY_DIR'], 'server.*'))

        if ca_files:
            print('Root CA exists, skipping')
        else:
            pkitool.run('--initca', retcode=0, stderr=sys.stdout)

        if server_files:
            print('Server cert exists, skipping')
        else:
            pkitool.run(['--server', 'server'], retcode=0, stderr=sys.stdout)

        dh_pem = os.path.join(local.env['KEY_DIR'],
                              'dh' + local.env['KEY_SIZE'] + '.pem')
        if local.path(dh_pem).exists():
            print('DH param exists, skipping')
        else:
            openssl.run(['dhparam', '-out', dh_pem, local.env['KEY_SIZE']],
                        stderr=sys.stdout)
