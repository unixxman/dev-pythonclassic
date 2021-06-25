from flask import Blueprint, flash
from flask_admin.babel import gettext
from flask_admin.contrib.sqla.view import func
from proftest import admin, session
from proftest.admin_view import AdminView
from proftest.models import (
    Category, Question, Answer,
    Role, User, Superuser
)
from wtforms import TextAreaField

admin_panel = Blueprint(__name__, 'admin_panel')


class QuestionView(AdminView):
    form_excluded_columns = ('submissions',)
    form_choices = {
        'type': [
            ('coding', 'Задание с кодом'),
            ('choices', 'Выбор ответа')
        ]
    }
    form_overrides = {'code_placeholder': TextAreaField}

    def _type_formatter(view, context, model, name):
        types = {
            'coding': 'Задание с кодом',
            'choices': 'Выбор ответа'
        }
        return types[model.type]

    def create_model(self, form):
        try:
            question = Question(**form.data)
            question.save()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s',
                              error=str(ex)), 'error')
            self.session.rollback()
            return False

        return question


class AnswerView(AdminView):
    form_excluded_columns = ('submissions',)


class UserRoleView(AdminView):
    form_widget_args = {
        'superusers': {
            'disabled': True
        }
    }

    form_choices = {
        'type': [
            ('user_role', 'пользовательская роль'),
        ]
    }

    def get_query(self):
        return self.session.query(self.model).\
            filter(self.model.type == 'user_role')

    def get_count_query(self):
        return self.session.query(func.count('*')).\
            filter(self.model.type == 'user_role')

    def create_form(self):
        form = super(UserRoleView, self).create_form()
        form.type.data = 'user_role'
        return form


class ServiceRoleView(AdminView):
    form_widget_args = {
        'users': {
            'disabled': True
        },
    }

    form_choices = {
        'type': [
            ('service_role', 'сервисная роль'),
        ]
    }

    def get_query(self):
        return self.session.query(self.model).\
            filter(self.model.type == 'service_role')

    def get_count_query(self):
        return self.session.query(func.count('*')).\
            filter(self.model.type == 'service_role')

    def create_form(self):
        form = super(ServiceRoleView, self).create_form()
        form.type.data = 'service_role'
        return form


class UserView(AdminView):
    form_args = {
        'roles': {
            'query_factory': lambda: Role.query.filter_by(
                type='user_role'
            )
        }
    }


class SuperuserView(AdminView):
    form_args = {
        'roles': {
            'query_factory': lambda: Role.query.filter_by(
                type='service_role'
            )
        }
    }


admin.add_view(AdminView(Category, session, 'Категории'))
admin.add_view(QuestionView(Question, session, 'Вопросы'))
admin.add_view(AnswerView(Answer, session, 'Ответы'))
admin.add_view(UserRoleView(
    Role, session, 'Роли пользователя', endpoint='user-role'))
admin.add_view(ServiceRoleView(
    Role, session, 'Роли администратора', endpoint='service-role'))
admin.add_view(UserView(User, session, 'Пользователи'))
admin.add_view(SuperuserView(Superuser, session, 'Администраторы'))
