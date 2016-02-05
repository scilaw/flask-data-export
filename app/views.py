
import os
import subprocess
import datetime
from flask import Blueprint
from flask import request
from flask import render_template, url_for
from flask import send_from_directory, redirect

import datasets
import dataops
from app import app, db
from models import ExportJob, ExportJobSelectVariable, ExportJobIncludeValue
from models import Downloads
from security import find_or_create_user


views = Blueprint("views", __name__, template_folder="templates")


def launch_job(job):
    path = os.path.abspath(os.path.dirname(__file__))
    job_script = os.path.join(path, '..', 'manage.py')
    job.pid = subprocess.Popen([job_script, 'export_job', str(job.id)]).pid
    db.session.commit()


def make_job_from_form():
    user = find_or_create_user(request.form.get('email'))
    job = ExportJob()
    job.user_id = user.id
    job.dataset_name = request.form.get('dataset_name')
    job.do_sampling = int(request.form.get('do_sampling') == 'on')
    job.sample_percent = int(request.form.get('sample_percent'))
    job.status = 'new'
    db.session.add(job)
    db.session.commit()
    return job


def make_select_vars_from_form(job_id):
    for selected_variable in request.form.getlist('select_vars'):
        var_record = ExportJobSelectVariable()
        var_record.job_id = job_id
        var_record.selected_variable = selected_variable
        db.session.add(var_record)
    db.session.commit()


def make_filter_vars_from_form(job_id, dataset_name):
    for field in dataops.all_datasets_fields()[dataset_name]:
        key = "filter_vars_" + field
        app.logger.info("check for filter key: " + key)
        for value in request.form.getlist(key):
            app.logger.info("found value: " + value)
            val_record = ExportJobIncludeValue()
            val_record.job_id = job_id
            val_record.variable_name = field
            val_record.variable_value = value
            db.session.add(val_record)
    db.session.commit()


def note_download(job_id):
    download = Downloads()
    download.job_id = job_id
    download.ip = request.environ['REMOTE_ADDR']
    download.downloaded_at = datetime.datetime.utcnow()
    job = ExportJob().query.get(job_id)
    job.status = 'downloaded'
    db.session.add(job)
    db.session.add(download)
    db.session.commit()


@views.route('/')
def index():
    field_values = dataops.all_datasets_key_fields_unique_values()
    dataset_fields = dataops.all_datasets_fields()
    dataset_record_count = dataops.dataset_record_counts()
    first_dataset = datasets.datasets.items()[0][0]
    return render_template('index.html',
                           datasets=datasets.datasets,
                           field_values=field_values,
                           dataset_fields=dataset_fields,
                           dataset_record_count=dataset_record_count,
                           first_dataset=first_dataset)


@views.route('/download/<int:job_id>')
def download(job_id):
    zip_fname = 'export_' + str(job_id) + '.zip'
    directory = os.path.join(app.config['BASE_DIR'], 'exports')
    result = send_from_directory(directory, zip_fname, as_attachment=True)
    note_download(job_id)
    return result


@views.route('/submit_job', methods=['POST'])
def submit_job():
    job = make_job_from_form()
    make_select_vars_from_form(job.id)
    make_filter_vars_from_form(job.id, job.dataset_name)
    launch_job(job)
    return redirect(url_for('views.index'))
