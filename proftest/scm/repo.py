from threading import Thread
from proftest import logger
from .gitflow import Gitflow


class Repo:
    def __init__(self, user_id):
        self.feature_name = None
        self.worktree = None
        self._thread = Thread(target=self._apply_changes)

    def async_update(self, worktree, feature_name):
        self.worktree = worktree
        self.feature_name = feature_name
        self._thread.start()

    def _apply_changes(self):
        gitflow = Gitflow(self.worktree.repo_local, self.feature_name)
        gitflow.set_local_branch()
        with gitflow.flow() as repo:
            try:
                self.worktree.write()
                if repo.head_is_unborn:
                    parent = []
                else:
                    parent = [repo.head.target]
                repo.index.add_all()
                user = repo.default_signature
                tree = repo.index.write_tree()

                repo.create_commit('HEAD', user, user, 'message', tree, parent)
                repo.index.write()
            except Exception as e:
                logger.error(f'failed to write changes to {self.feature_name} {e}')
                self.worktree.clean()
