'''
Revokes client certs
'''
from plumbum import local
from plumbum.cmd import rm
from index_db_parser import parse_index_file
import os
import sys


def revoke_client(client, settings):
    # Do not continue without the serial file or index.txt
    with local.env(**settings):
        serial_file = os.path.join(local.env['KEY_DIR'], 'serial')
        index_file = os.path.join(local.env['KEY_DIR'], 'index.txt')
        client_hash = parse_index_file(index_file)

        if (not local.path(serial_file).exists()) or (not local.path(index_file).exists()):
            sys.exit("Index.txt or serial does not exist in KEY_DIR, aborting")

        if client_hash.get(client, {}).get('is_valid'):
            revoke_full = local[os.path.join(local.env['EASY_RSA'], 'revoke-full')]
            revoke_full.run(client, retcode=2, stderr=sys.stdout)
            rm.run(os.path.join(local.env['KEY_DIR'], 'revoke-test.pem'),
                   retcode=0)
