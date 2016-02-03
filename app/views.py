
import datasets
import dataops
from flask import Blueprint
from flask import request, render_template, redirect, url_for
# from flask.ext.security import login_required
# from models import User

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


@views.route('/submit_job', methods=['POST'])
def submit_job():
    dataset_fields = dataops.all_datasets_fields()
    select_vars = request.form['select_vars']
    do_sampling = request.form['do_sampling']
    sample_percent = request.form['sample_percent']
    email = request.form['email']
    dataset_name = request.form['dataset_name']
    for field in dataset_fields:
        key = "filter_vars_" + field
        field_values = request.form.getlist(key)
    redirect(url_for('index'))
