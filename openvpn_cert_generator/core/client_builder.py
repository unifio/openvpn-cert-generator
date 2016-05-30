'''
Creates new client certs
'''
from plumbum import local
from plumbum.cmd import tar
from glob import glob
from jinja2 import Environment, PackageLoader
from distutils.util import strtobool
import hashlib
import os
import sys


class ClientBuilder(object):

    def __init__(self, template_file):
        self.template = self.init_template(template_file)

    def build(self, client, settings):
        with local.env(**settings):
            serial_file = os.path.join(local.env['KEY_DIR'], 'serial')
            index_file = os.path.join(local.env['KEY_DIR'], 'index.txt')

            # Do not continue without the serial file or index.txt
            if (not local.path(serial_file).exists()) or (not local.path(index_file).exists()):
                sys.exit("Index.txt or serial does not exist in KEY_DIR, aborting")

            self.build_client_certs(client, settings)
            self.build_client_ovpn_file(client, settings)
            self.tarball_client_files(client, settings)

    def init_template(self, template_file):
        environment = Environment(loader=PackageLoader('openvpn_cert_generator'))
        environment.filters['strtobool'] = strtobool
        return environment.get_template('client.ovpn.j2')

    def build_client_certs(self, client, settings):
        with local.env(**settings):
            pkitool = local[os.path.join(local.env['EASY_RSA'], 'pkitool')]
            client_files = glob(os.path.join(local.env['KEY_DIR'], client + '.*'))

            if client_files:
                print "Client {} certs already exist, skipping".format(client)
            else:
                pkitool.run(client, retcode=0, stderr=sys.stdout)

    def build_client_ovpn_file(self, client, settings):
        template_vars = settings.copy()
        template_vars.update(client=client)

        # Get md5 of current file if exists
        with local.env(**settings):
            existing_md5 = ''
            ovpn_file = os.path.join(local.env['KEY_DIR'], template_vars['client'] + '.ovpn')
            if local.path(ovpn_file).exists():
                with open(ovpn_file, 'rb') as f:
                    hasher = hashlib.md5()
                    hasher.update(f.read())
                    existing_md5 = hasher.hexdigest()

            new_ovpn_contents = self.template.render(template_vars)
            hasher = hashlib.md5()
            hasher.update(new_ovpn_contents)
            new_md5 = hasher.hexdigest()

            if existing_md5 != new_md5:
                with open(ovpn_file, "wb") as f:
                    f.write(self.template.render(template_vars))

    def tarball_client_files(self, client, settings):
        # Always regen the tarball
        with local.env(GZIP='-n', **settings):
            tar.run(['-czvf',
                     os.path.join(local.env['KEY_DIR'], client + '.tar.gz'),
                     '-C',
                     local.env['KEY_DIR'],
                     client + '.crt',
                     client + '.key',
                     client + '.ovpn',
                     'ca.crt',
                     ], retcode=0, stderr=sys.stdout)
