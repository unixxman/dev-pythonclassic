import os
import pygit2
from contextlib import contextmanager
from proftest import logger
from proftest.config import Config
from . import CREDENTIALS


class Gitflow:
    def __init__(self, repo_local, feature_name):
        self.repo_local = repo_local
        self.feature_name = feature_name
        self.repo = None
        self.callbacks = pygit2.RemoteCallbacks(credentials=CREDENTIALS)

    def set_local_branch(self):
        if os.path.exists(self.repo_local + '/.git'):
            self.repo = pygit2.Repository(self.repo_local)
            self.pull()
        else:
            self.repo = pygit2.clone_repository(
                Config.REPO_REMOTE, self.repo_local, callbacks=self.callbacks)
        try:
            ref = self.repo.lookup_reference(f'refs/heads/{self.feature_name}')
        except KeyError:
            branch = self.create_branch(self.feature_name)
            ref = self.repo.lookup_reference(branch.name)
        self.repo.checkout(ref)
        logger.info(f'switched to branch {self.feature_name}')

    @contextmanager
    def flow(self):
        try:
            yield self.repo
            self.push(self.feature_name)
        except Exception as e:
            self.repo.reset(self.repo.head.target, pygit2.GIT_RESET_HARD)
            logger.error(f'error occurs, changes discarded: {e}')
            raise
        finally:
            self.repo.checkout(self.repo.lookup_reference('refs/heads/master'))

    def pull(self):
        origin = self.repo.remotes['origin']
        origin.fetch(callbacks=self.callbacks)
        remote_master_id = self.repo.lookup_reference(
            'refs/remotes/origin/master').target
        merge_result, _ = self.repo.merge_analysis(remote_master_id)

        if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
            logger.info('up to date with branch master')
            return
        elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
            self.repo.checkout_tree(self.repo.get(remote_master_id))
            master_ref = self.repo.lookup_reference('refs/heads/master')
            master_ref.set_target(remote_master_id)
            self.repo.head.set_target(remote_master_id)
            logger.info('fetched remote changes')
        elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
            self.repo.merge(remote_master_id)

            if self.repo.index.conflicts is not None:
                for conflict in self.repo.index.conflicts:
                    logger.warning(f'Conflicts found in: {conflict[0].path}')
                raise AssertionError('Conflicts')

            user = self.repo.default_signature
            tree = self.repo.index.write_tree()
            _ = self.repo.create_commit('HEAD',
                                        user,
                                        user,
                                        'merge remote',
                                        tree,
                                        [self.repo.head.target, remote_master_id])
            # We need to do this or git CLI will think we are still merging.
            self.repo.state_cleanup()
            logger.info('merged remote changes')
        else:
            raise AssertionError(
                f'Inappropriate merge analysis result: {merge_result}')

    def push(self, branch_name):
        origin = self.repo.remotes['origin']
        origin.push([f'+refs/heads/{branch_name}'], callbacks=self.callbacks)
        logger.info('changes pushed to remote')

    def create_branch(self, branch_name):
        commit = self.repo[self.repo.head.target]
        return self.repo.branches.local.create(branch_name, commit)
