from flask import request, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user


class AdminMixin:
    def is_accessible(self):

        if current_user.has_role('admin'):
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    form_excluded_columns = (
        'created_at', 'modified_at')
