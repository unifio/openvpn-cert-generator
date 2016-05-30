'''
Parses easy-rsa's index.txt file into
a useful dictionary object
'''
from datetime import datetime
import re


def parse_index_file(index_file):
    with open(index_file) as file:
        rows = [line.split('\t') for line in file]

        if rows:
            client_hash = {}
            for row in rows:
                client_name = re.search('(?<=/CN=).*?/', row[5]).group(0)[:-1]
                is_valid = bool(row[0] == 'V')
                expiration_time = datetime.strptime(row[1], "%y%m%d%H%M%SZ").strftime("%Y-%m-%dT%H:%M:%SZ")
                revocation_time = ''
                if row[2]:
                    revocation_time = datetime.strptime(row[2], "%y%m%d%H%M%SZ").strftime("%Y-%m-%dT%H:%M:%SZ")
                serial_number = row[3]
                full_DN = row[5]

                client_hash[client_name] = {
                    'is_valid': is_valid,
                    'expiration_time': expiration_time,
                    'revocation_time': revocation_time,
                    'serial_number': serial_number,
                    'full_DN': full_DN,
                }
            return client_hash

        else:
            return {}
