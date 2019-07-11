#! ../env/bin/python
# -*- coding: utf-8 -*-

from openvpn_cert_generator.utils.settings_dict import SettingsDict


class TestSettingsDict:
    def test_default_config(self):
        """ Tests if the default config loads correctly """

        env = SettingsDict()

        assert env['EASY_RSA'] == '/usr/share/easy-rsa/'
        assert env['OPENSSL'] == 'openssl'
        assert env['PKCS11TOOL'] == 'pkcs11-tool'
        assert env['GREP'] == 'grep'
        assert env['KEY_CONFIG'] == '/usr/share/easy-rsa/openssl-1.0.0.cnf'
        assert env['PKCS11_MODULE_PATH'] == 'dummy'
        assert env['PKCS11_PIN'] == 'dummy'

        assert env['KEY_SIZE'] == '4096'
        assert env['CA_EXPIRE'] == '3650'
        assert env['KEY_EXPIRE'] == '3650'
        assert env['KEY_COUNTRY'] == 'US'
        assert env['KEY_PROVINCE'] == 'CA'
        assert env['KEY_CITY'] == 'San Francisco'
        assert env['KEY_ORG'] == 'Fort-Funston'
        assert env['KEY_EMAIL'] == 'cert-admin@example.com'
        assert env['KEY_OU'] == 'MyOrgUnit'
        assert env['KEY_NAME'] == 'EasyRSA'
        assert env['ACTIVE_CLIENTS'] == 'client'
        assert env['REVOKED_CLIENTS'] == ''
        assert env['OPENVPN_DEV'] == 'tun'

    def test_value_passed_config(self):
        """ Tests if the value passed config loads correctly """

        env = SettingsDict(KEY_SIZE='2048', CA_EXPIRE='7300',
                           KEY_EXPIRE='7300', KEY_COUNTRY='UK',
                           KEY_PROVINCE='Avon', KEY_CITY='Bristol',
                           KEY_ORG='Hazel Brook',
                           KEY_EMAIL='concorde@bristolaero.org',
                           KEY_OU='Portishead', KEY_NAME='ACME',
                           ACTIVE_CLIENTS='devs',
                           REVOKED_CLIENTS='non-devs')

        assert env['KEY_SIZE'] == '2048'
        assert env['CA_EXPIRE'] == '7300'
        assert env['KEY_EXPIRE'] == '7300'
        assert env['KEY_COUNTRY'] == 'UK'
        assert env['KEY_PROVINCE'] == 'Avon'
        assert env['KEY_CITY'] == 'Bristol'
        assert env['KEY_ORG'] == 'Hazel Brook'
        assert env['KEY_EMAIL'] == 'concorde@bristolaero.org'
        assert env['KEY_OU'] == 'Portishead'
        assert env['KEY_NAME'] == 'ACME'
        assert env['ACTIVE_CLIENTS'] == 'devs'
        assert env['REVOKED_CLIENTS'] == 'non-devs'

    def test_environment_variable_config(self, monkeypatch):
        """ Tests if the environment variable config loads correctly """

        monkeypatch.setenv('HOME', '/abc')

        env = SettingsDict()

        assert env['KEY_SIZE'] == '4096'
        assert env['KEY_DIR'] == '/abc/easy-rsa-keys'
