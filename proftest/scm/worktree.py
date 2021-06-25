import os
from shutil import copyfile
from pathlib import Path
from proftest.models import Question
from proftest.config import Config


class Worktree:
    def __init__(self, assessment, user_id):
        self.assessment = assessment
        self.user_id = user_id
        self.repo_local = f'{Config.GIT_ROOT}/{self.user_id}/{Config.REPO_NAME}'

    def write(self):
        if not os.path.exists(self.repo_local):
            raise Exception('Local repository does not exist')

        self.init_packages()

        # write source code
        questions = Question.query.filter(
            Question.type == 'coding',
            Question.category.has(assessment_id=self.assessment.id)).all()
        for question in questions:
            try:
                modules = self.get_code(question)
                for module in modules:
                    self.write_module(module)
            except StopIteration:
                continue

        # copy conf files to the repo root
        # self.copy_conf()

    def init_packages(self):
        self.write_module(
            (f'{self.assessment.metainfo}/__init__.py', ''))
        for category in self.assessment.categories:
            init_module = (f'{self.assessment.metainfo}/{category.metainfo}/__init__.py', '')
            self.write_module(init_module)

    def get_code(self, question):
        modules = []
        code = next((sub.value['code'] for sub in question.submissions
                     if sub.purpose == 'source'
                     and sub.user_id == self.user_id))
        file_path = f'{self.assessment.metainfo}/{question.category.metainfo}'
        modules.append((file_path + f'/{question.file_name}', code))

        test_path = 'tests/' + f'{file_path}/test_{question.file_name}'
        modules.append((test_path, question.unit_tests[0].value['code']))
        return modules

    """def copy_conf(self):
        copyfile(
            f'{Path(__file__).parent}/travis-example.yml',
            self.repo_local + '/.travis.yml')
        copyfile(
            f'{Path(__file__).parent}/requirements-example.txt',
            self.repo_local + '/requirements.txt')"""

    def write_module(self, module):
        path, code = module
        location = self.repo_local + '/' + '/'.join(path.split('/')[:-1])
        if not os.path.exists(location):
            os.makedirs(location)
        with open(f'{self.repo_local}/{path}', 'w') as fileobj:
            fileobj.write(code)

    def clean(self):
        pass  # TODO: delete files
