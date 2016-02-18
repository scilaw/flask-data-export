#!/usr/bin/env python

from flask.ext.script import Manager
from flask_migrate import MigrateCommand

from app import create_app
from app.job import run_export_job, job_description_only
from app.lock import locked_run

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def export_job(job_id):
    def job_cb():
        run_export_job(job_id)
    locked_run(job_cb, '/tmp/export_job_lock_file')


@manager.command
def show_description(job_id):
    print(job_description_only(job_id))


if __name__ == '__main__':
    manager.run()
