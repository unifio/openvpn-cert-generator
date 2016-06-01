'''
A utility dictionary used to initialize values
from the following list, in order of precedence:
- value passed in while initializing class
- environment variable value
- defaults
'''

import os


class SettingsDict(dict):

    def __init__(self, *args, **kw):
        super(SettingsDict, self).__init__()

        self.update(self.defaults())
        self.update(os.environ.copy())

        self.update(*args)
        self.update(**kw)

    def defaults(self):
        # TODO: deb specific
        default = {}
        default['EASY_RSA'] = '/usr/share/easy-rsa/'
        default['OPENSSL'] = 'openssl'
        default['PKCS11TOOL'] = 'pkcs11-tool'
        default['GREP'] = 'grep'
        default['KEY_CONFIG'] = os.path.join(default['EASY_RSA'], 'openssl-1.0.0.cnf')
        default['PKCS11_MODULE_PATH'] = 'dummy'
        default['PKCS11_PIN'] = 'dummy'

        # TODO: Overrideable
        default['KEY_DIR'] = os.path.join(os.environ['HOME'], 'easy-rsa-keys')
        default['KEY_SIZE'] = '4096'
        default['CA_EXPIRE'] = '3650'
        default['KEY_EXPIRE'] = '3650'
        default['KEY_COUNTRY'] = 'US'
        default['KEY_PROVINCE'] = 'CA'
        default['KEY_CITY'] = 'San Francisco'
        default['KEY_ORG'] = 'Fort-Funston'
        default['KEY_EMAIL'] = 'cert-admin@example.com'
        default['KEY_OU'] = 'MyOrgUnit'
        default['KEY_NAME'] = 'EasyRSA'
        default['ACTIVE_CLIENTS'] = 'client'
        default['REVOKED_CLIENTS'] = ''
        default['OPENVPN_DEV'] = 'tun'
        default['OPENVPN_PROTO'] = 'tcp'
        default['OPENVPN_HOST'] = 'localhost'
        default['OPENVPN_RESOLV_RETRY'] = 'infinite'
        default['OPENVPN_COMP_LZO'] = 'yes'
        default['OPENVPN_VERB'] = '3'
        default['OPENVPN_USE_LDAP'] = 'no'
        default['OPENVPN_CLIENT_OPTIONS'] = ''
        default['FORCE_CERT_REGEN'] = 'false'
        default['S3_PUSH_DRYRUN'] = 'false'

        # TODO: move out of defaults
        default['S3_REGION'] = 'ap-northeast-1'
        default['S3_CERT_ROOT_PATH'] = "s3://tf-unifio-openvpn-cert/"
        default['S3_DIR_OVERRIDE'] = '20160319'

        return default
