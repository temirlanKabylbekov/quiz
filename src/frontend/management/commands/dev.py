import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run frontend and backend development servers"

    def npm(self, *args, run_async=False):
        flag = os.P_NOWAIT if run_async else os.P_WAIT

        os.chdir('./frontend')
        os.spawnvp(flag, 'npm', ['npm'] + list(args))
        os.chdir('../')

    def handle(self, *args, **options):
        if not os.path.exists('./frontend/static/js/dll/vendor.js'):
            print(self.style.HTTP_INFO('Dev vendor bundle not found, building one'))
            self.npm('run', 'build:dll')

        self.npm('run', 'dev', run_async=True)
        os.execvp('python', ['python', './manage.py', 'runserver'])
