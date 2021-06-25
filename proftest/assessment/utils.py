from functools import wraps
from proftest.models import User


def get_proficiency(score):
    proficiency = ''
    if score < 30:
        proficiency = 'beginning'
    elif score < 70:
        proficiency = 'developing'
    else:
        proficiency = 'accomplished'
    return proficiency


def role_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        _, user_id = args
        if kwargs.get('purpose') == 'test':
            if not User.query.filter(User.id == user_id).\
                    join(User.roles, aliased=True).\
                    filter_by(name='qa').first():
                raise PermissionError(
                    'This user is not permitted to write tests')
        return fn(*args, **kwargs)
    return wrapper
