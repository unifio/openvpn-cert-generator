from client_builder import ClientBuilder
from client_revoker import revoke_client  # NOQA

template_file = 'client.ovpn.j2'
shared_vars = {}


def build_client(client, settings):
    if not shared_vars.get('builder'):
        shared_vars['builder'] = ClientBuilder(template_file)

    shared_vars['builder'].build(client, settings)
