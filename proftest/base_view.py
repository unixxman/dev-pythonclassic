import traceback
from flask import jsonify, g
from flask_apispec.views import MethodResource
from proftest import logger


class BaseView(MethodResource):

    @classmethod
    def register(cls, blueprint, spec, url, name):
        blueprint.add_url_rule(url, view_func=cls.as_view(name))
        blueprint.register_error_handler(422, cls.handle_validation_error)
        blueprint.register_error_handler(Exception, cls.handle_internal_error)
        spec.register(cls, blueprint=blueprint.name)

    @staticmethod
    def handle_validation_error(err):
        headers = err.data.get('headers', None)
        messages = err.data.get('messages', ['Invalid Request.'])
        logger.warning(f'Invalid input params: {messages}')
        if headers:
            return jsonify({'message': messages}), 400, headers
        else:
            return jsonify({'message': messages}), 400

    @staticmethod
    def handle_internal_error(err):
        if isinstance(err, ValueError):
            status, log = 200, str(err)
        elif isinstance(err, PermissionError):
            status, log = 403, str(err)
        else:
            user_id = getattr(g, 'user_id', 'unknown')
            log = f'user:{user_id} request failed. {traceback.format_exc()}'
            status = 400
        logger.warning(log)
        return jsonify({'message': str(err), 'statusCode': 1}), status
