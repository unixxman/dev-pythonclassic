import json
from flask import Blueprint, request, jsonify
from proftest import logger
from proftest.models import Feedback

scm = Blueprint('scm', __name__)


@scm.route('/travisci', methods=['POST'])
def receive_notification():
    try:
        test_result = json.loads(request.form['payload'])
        branch = test_result['branch'].split('-')
        if branch == 'master':
            return jsonify({'msg': 'received'})
        user_id, feedback_id = [int(id) for id in branch[1:]]
        state = test_result['result_message'].upper().replace(' ', '_')

        feedback = Feedback.get(feedback_id, user_id)
        score = feedback.score + (50 if state in ('PASSED', 'FIXED') else 0)
        feedback.update(state=state, score=score)

        logger.info(
            f'user:{user_id} feedback:{feedback_id} test result received: {state}')
        return jsonify({'msg': 'received'})
    except Exception as e:
        logger.warning(f'failed to receive travis notification: {e}')
        return jsonify({'msg': 'bad request'}), 400
