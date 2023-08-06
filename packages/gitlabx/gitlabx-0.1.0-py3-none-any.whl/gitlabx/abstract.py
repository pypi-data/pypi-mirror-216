import gitlab
from abc import ABC

class AbstractGitLab(ABC):

    def __init__(self, personal_access_token):

        self.personal_access_token = personal_access_token
        self.gl = gitlab.Gitlab(url='https://gitlab.com/', private_token = personal_access_token)

    