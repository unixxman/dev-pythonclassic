from proftest import logger
from proftest.config import Config
from .gitflow import Gitflow


class Repo:
    def __init__(self, worktree):
        self._worktree = worktree
        self._url = Config.REPO_URL

    def push_new_branch(self, assessment, feature_name):
        self._apply_changes(assessment, feature_name)
        return self._worktree.head_url

    def _apply_changes(self, assessment, feature_name):
        gitflow = Gitflow(self._worktree.repo_local, feature_name)
        gitflow.set_local_branch()
        with gitflow.flow() as repo:
            try:
                self._worktree.write(assessment)
                if repo.head_is_unborn:
                    parent = []
                else:
                    parent = [repo.head.target]
                repo.index.add_all()
                user = repo.default_signature
                tree = repo.index.write_tree()

                repo.create_commit('HEAD', user, user, 'message', tree, parent)
                repo.index.write()
                self._worktree.head_url = f'{self._url}/tree/{feature_name}'
            except Exception as e:
                logger.error(f'failed to write changes to {feature_name} {e}')
                self._worktree.clean()
