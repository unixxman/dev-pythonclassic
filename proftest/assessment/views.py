from flask import Blueprint, g
from flask_jwt_extended import jwt_required
from flask_apispec import use_kwargs, marshal_with
from proftest import docs
from proftest.models import Assessment, Question
from proftest.models import Feedback
from proftest.users.utils import check_identity, set_claims
from proftest.scm.handlers import GitJobHandler
from .utils import get_proficiency

from proftest.schemas import (
    create_schema,
    AssessmentSchema,
    AssessmentDetailedSchema,
    SubmissionSchema
)
from proftest.base_view import BaseView

assessment = Blueprint('assessment', __name__)
ListSchema = create_schema(AssessmentSchema, many=True)
DetailedSchema = create_schema(AssessmentDetailedSchema)


class AssessmentListView(BaseView):
    @jwt_required
    @check_identity
    @set_claims
    @marshal_with(ListSchema)
    def get(self, *args):
        data = Assessment.query.filter(*Assessment.get_filters()).all()
        return {'data': data}


class AssessmentDetailedView(BaseView):
    @jwt_required
    @set_claims
    @marshal_with(DetailedSchema)
    def get(self, assessment_id):
        assessment = Assessment.get(assessment_id)
        return {'data': assessment}

    @jwt_required
    @set_claims
    @marshal_with(DetailedSchema)
    def put(self, assessment_id):
        assessment = Assessment.get(assessment_id)
        score = assessment.calculate_score(g.user_id)
        proficiency = get_proficiency(score)
        if assessment.feedback:
            raise Exception('Current result must be canceled')
        feedback = Feedback(
            candidate_id=g.user_id,
            assessment_id=assessment_id,
            score=score,
            proficiency=proficiency,
            state='PENDING'
        )
        feedback.save()
        GitJobHandler(assessment.id, feedback.id, g.user_id).run()
        return {'data': assessment}

    @jwt_required
    @set_claims
    def delete(self, assessment_id):
        assessment = Assessment.get(assessment_id)
        feedback = assessment.feedback
        if feedback:
            feedback.update(state='CANCELED')
        return '', 204


class SubmitView(BaseView):
    @jwt_required
    @set_claims
    @use_kwargs(SubmissionSchema(only=('value', 'answers', 'purpose')))
    @marshal_with(DetailedSchema)
    def post(self, assessment_id, question_id, **kwargs):
        assessment = Assessment.get(assessment_id)
        question = Question.get(question_id, assessment_id)
        question.submit(g.user_id, **kwargs)
        return {'data': assessment}


AssessmentListView.register(
    assessment, docs, '/assessment', 'assessmentlistview')
AssessmentDetailedView.register(
    assessment, docs, '/assessment/<int:assessment_id>',
    'assessmentdetailedview')
SubmitView.register(
    assessment, docs,
    '/assessment/<int:assessment_id>/questions/<int:question_id>',
    'submitview')
