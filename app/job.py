#!/usr/bin/env python

import os
import zipfile
from flask import render_template
from flask_mail import Message
from tempfile import mkdtemp
from shutil import copyfile, move, rmtree
from datetime import datetime, timedelta

import datasets
import dataops
from app import db, mail, app
from models import User
from models import ExportJob
from models import ExportJobSelectVariable
from models import ExportJobIncludeValue
from sample import stratified_random_sample


def get_filtered_data(data, filter_vars):
    filters = {}
    for filter_var in filter_vars:
        var_name = filter_var.variable_name
        var_value = filter_var.variable_value
        if (var_name not in filters):
            filters[var_name] = []
        filters[var_name].append(var_value)
    for var_name in filters:
        values = filters[var_name]
        app.logger.info("Data where " + var_name + " is in " + str(values))
        data = data[data[var_name].astype(str).isin(values)]
        app.logger.info("Got " + str(len(data)) + " rows")
    return data


def get_sampled_data(data, dataset_name, percent):
    fields = datasets.datasets[dataset_name]['fields_of_interest']
    return stratified_random_sample(data, fields, percent / 100.0)


def get_select_fields(data, select_vars):
    columns = []
    for select_var in select_vars:
        columns.append(select_var.selected_variable)
    return data[columns]


def get_data_export(job, select_vars, filter_vars):
    dataset_name = job.dataset_name
    sample_percent = job.sample_percent
    app.logger.info("Load data")
    data = dataops.load_data(dataset_name)
    app.logger.info("Filter data")
    data = get_filtered_data(data, filter_vars)
    if (job.do_sampling):
        app.logger.info("Sample data")
        data = get_sampled_data(data, dataset_name, sample_percent)
    app.logger.info("Select columns")
    return get_select_fields(data, select_vars)


def export_description(job, select_vars, filter_vars):
    field_values = dataops.all_datasets_key_fields_unique_values()
    return render_template('export_description.txt',
                           job=job,
                           field_values=field_values,
                           dataset_name=job.dataset_name,
                           datasets=datasets.datasets,
                           select_vars=select_vars,
                           filter_vars=filter_vars)


def export_zip(data, job_id, dataset_name, description_text):
    app.logger.info("Make zip")
    tempdir = mkdtemp(prefix='nexp')
    os.chdir(tempdir)
    fname = dataset_name + '.csv'
    zip_fname = 'export_' + str(job_id) + '.zip'
    app.logger.info("Write csv")
    data.to_csv(fname, index=False)
    zip_file = zipfile.ZipFile(zip_fname, 'w', zipfile.ZIP_DEFLATED)
    app.logger.info("Write csv to zip")
    zip_file.write(fname)
    description_fname = "export_description.txt"
    with open(description_fname, "w") as text_file:
        text_file.write(description_text)
    zip_file.write(description_fname)
    add_file_path = os.path.join(app.config['BASE_DIR'], datasets.data_path)
    for add_file in datasets.include_always:
        source = os.path.join(add_file_path, add_file)
        dest = os.path.join(tempdir, add_file)
        copyfile(source, dest)
        zip_file.write(add_file)
    zip_file.close()
    app.logger.info("Zip file closed")
    zip_dest = os.path.join(app.config['BASE_DIR'], 'exports', zip_fname)
    move(zip_fname, zip_dest)
    rmtree(tempdir)


def notify_complete(user, job, select_vars, filter_vars):
    base_url = app.config['BASE_URL']
    html = render_template('job_complete_message.html',
                           base_url=base_url,
                           user=user,
                           job=job,
                           dataset_name=job.dataset_name,
                           datasets=datasets.datasets,
                           select_vars=select_vars,
                           filter_vars=filter_vars)
    subject = 'Scilaw Data Export'
    msg = Message(subject=subject, html=html, recipients=[user.email])
    mail.send(msg)
    return True


def notify_recent_jobs():
    admin_email = app.config['ADMIN_EMAIL']
    last_week = datetime.utcnow() - timedelta(weeks=1)
    query = db.session.query(ExportJob).join(User).add_column('email')
    jobs_emails = query.filter(ExportJob.created_at > last_week).all()
    html = render_template('recent_jobs.html', jobs_emails=jobs_emails)
    subject = 'Scilaw Data Export Jobs Report'
    msg = Message(subject=subject, html=html, recipients=[admin_email])
    mail.send(msg)
    return True


def job_complete(job, select_vars, filter_vars):
    user = User().query.get(job.user_id)
    notify_complete(user, job, select_vars, filter_vars)
    db.session.add(job)
    job.status = 'complete'
    db.session.commit()


def job_description_only(job_id):
    job = ExportJob().query.get(job_id)
    select_vars = ExportJobSelectVariable().query.filter_by(job_id=job.id)
    filter_vars = ExportJobIncludeValue().query.filter_by(job_id=job.id)
    return export_description(job, select_vars, filter_vars)


def run_export_job(job_id):
    job = ExportJob().query.get(job_id)
    select_vars = ExportJobSelectVariable().query.filter_by(job_id=job.id)
    filter_vars = ExportJobIncludeValue().query.filter_by(job_id=job.id)
    data = get_data_export(job, select_vars, filter_vars)
    description_text = export_description(job, select_vars, filter_vars)
    export_zip(data, job.id, job.dataset_name, description_text)
    job_complete(job, select_vars, filter_vars)
