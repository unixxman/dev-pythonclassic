from .question import Question
from .answer import Answer
from .submission import Submission


class MultichoiceQuestion(Question):
    __mapper_args__ = {'polymorphic_identity': 'choices'}

    def submit(self, user_id, **kwargs):
        answers_ids = kwargs.get('answers')
        if not answers_ids:
            raise ValueError('Choose any answer')
        answers = [Answer.get(answer['id'], self.id)
                   for answer in answers_ids]
        purpose = kwargs.get('purpose')
        submission = Submission.query.filter(
            Submission.question_id == self.id,
            Submission.user_id == user_id,
            Submission.purpose == purpose
        ).first()
        if not submission:
            print('NO')
            submission = Submission(
                user_id=user_id,
                question_id=self.id,
                answers=answers,
                purpose=purpose
            )
            submission.save()
        else:
            submission.update(answers=answers)

    def get_candidate_solution(self, user_id):
        submission = Submission.query.filter(
            Submission.question_id == self.id,
            Submission.user_id == user_id
        ).first()
        if not submission:
            return False
        right_answer = next((answer for answer in self.answers
                             if answer.is_right), None)
        return right_answer in submission.answers
