
import datasets
import dataops
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from app import db
from models import ExportJob, ExportJobSelectVariable, ExportJobIncludeValue
from security import security


views = Blueprint("views", __name__, template_folder="templates")


@views.route('/')
def index():
    field_values = dataops.all_datasets_key_fields_unique_values()
    dataset_fields = dataops.all_datasets_fields()
    dataset_record_count = dataops.dataset_record_counts()
    # User().query.all()
    first_dataset = datasets.datasets.items()[0][0]
    return render_template('index.html',
                           datasets=datasets.datasets,
                           field_values=field_values,
                           dataset_fields=dataset_fields,
                           dataset_record_count=dataset_record_count,
                           first_dataset=first_dataset)


@views.route('/job_submitted')
def job_submitted():
    return render_template('job_submitted.html')


@views.route('/download_page')
def download_page():
    return render_template('download_page.html')


def find_or_create_user(email):
    user = security.datastore.find_user(email)
    if (user is None):
        user = security.datastore.create_user(email=email)
    return user


@views.route('/submit_job', methods=['POST'])
def submit_job():
    user = find_or_create_user(request.form['email'])
    job = ExportJob()
    job['user_id'] = user.id
    job['dataset_name'] = request.form['dataset_name']
    job['do_sampling'] = request.form['do_sampling']
    job['sample_percent'] = request.form['sample_percent']
    job['status'] = 'new'
    db.session.add(job)
    db.session.commit()
    for selected_variable in request.form.getlist('select_vars'):
        var_record = ExportJobSelectVariable()
        var_record['job_id'] = job.id
        var_record['selected_variable'] = selected_variable
        db.session.add(var_record)
    for field in dataops.all_datasets_fields():
        key = "filter_vars_" + field
        for value in request.form.getlist(key):
            val_record = ExportJobIncludeValue()
            val_record['job_id'] = job.id
            val_record['variable_name'] = field
            val_record['variable_value'] = value
            db.session.add(val_record)
    db.session.commit()
    redirect(url_for('index'))
