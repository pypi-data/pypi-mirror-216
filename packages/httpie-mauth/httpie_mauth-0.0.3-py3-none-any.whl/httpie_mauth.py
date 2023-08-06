"""
MAuth Plugin for HTTPie
"""

from httpie.plugins import AuthPlugin
from mauth_client.requests_mauth import MAuth
import yaml
import os.path

class MAuthPlugin(AuthPlugin):

    name = 'MAuth auth'
    auth_type = 'mauth'
    description = 'Use MAuth to sign outgoing requests'
    auth_require = False

    def get_auth(self, username=None, password=None):
        env = self.get_config()
        uuid = env['app_uuid']
        priv_key_path = env['private_key_file']
        with open(priv_key_path) as f:
            privkey = f.read()
        return MAuth(uuid, privkey, 'v1,v2')

    def get_config(self):
        possible_files = [
            '~/.mauth_config.yml',
            './config/mauth.yml',
            './mauth.yml',
        ]

        for file_path in [os.path.expanduser(f) for f in possible_files]:
            if os.path.exists(file_path):
                with open(file_path) as f:
                    return yaml.safe_load(f.read())['development']
