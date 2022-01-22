from rq import Queue
from proftest import logger
from proftest.models import Assessment, Feedback
from .repo import Repo
from .worktree import Worktree


class GitJobHandler:
    def __init__(self, assessment_id, feedback_id, user_id):
        self._assessment_id = assessment_id
        self._feedback_id = feedback_id
        self.repo = Repo(Worktree(user_id))
        self.feature_name = f'assess-{user_id}-{feedback_id}'

    def execute(self):
        branch_url = self.repo.push_new_branch(
            Assessment.query.get(self._assessment_id),
            self.feature_name)
        Feedback.query.get(self._feedback_id).update(source_url=branch_url)

    def run(self):
        queue = Queue()
        job = queue.enqueue_call(self.execute, result_ttl=300)
        logger.info(f'Job {job.get_id()} queued')
