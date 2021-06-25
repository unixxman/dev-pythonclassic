import pygit2
from proftest.config import Config

CREDENTIALS = pygit2.credentials.Keypair('git',
                                         Config.GIT_SSH_KEY_PUBLIC,
                                         Config.GIT_SSH_KEY_PRIVATE,
                                         None)
