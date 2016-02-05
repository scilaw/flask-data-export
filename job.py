#!/usr/bin/env python

import os
import sys
import zipfile
from flask import render_template
from flask.ext.mail import Mail, Message
from tempfile import mkdtemp
from shutil import copyfile, move, rmtree

from app import datasets
from app import dataops
from app import get_db, get_app
from app.models import User
from app.models import ExportJob
from app.models import ExportJobSelectVariable
from app.models import ExportJobIncludeValue
from app.sample import stratified_random_sample


app = get_app()
db = get_db()
mail = Mail(app)


def get_filtered_data(data, filter_vars):
    for filter_var in filter_vars:
        variable_name = filter_var.variable_name
        variable_value = filter_var.variable_value
        mask = data[variable_name] == variable_value
        data = data[mask]
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


def export_zip(data, dataset_name):
    app.logger.info("Make zip")
    tempdir = mkdtemp(prefix='nexp')
    os.chdir(tempdir)
    fname = job.dataset_name + '.csv'
    zip_fname = 'export_' + str(job.id) + '.zip'
    app.logger.info("Write csv")
    data.to_csv(fname)
    zip_file = zipfile.ZipFile(zip_fname, mode='w')
    app.logger.info("Write csv to zip")
    zip_file.write(fname)
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
    html = render_template('job_complete_message.html',
                           user=user,
                           job=job,
                           dataset_name=job.dataset_name,
                           datasets=datasets.datasets,
                           select_vars=select_vars,
                           filter_vars=filter_vars)
    subject = 'Subject line'
    msg = Message(subject=subject, html=html, recipients=[user.email])
    mail.send(msg)
    return True


def job_complete(job, select_vars, filter_vars):
    user = User().query.get(job.user_id)
    notify_complete(user, job, select_vars, filter_vars)
    job.status = 'complete'


if __name__ == '__main__':
    pid = sys.argv[1]
    with app.app_context():
        job = ExportJob().query.get(pid)
        select_vars = ExportJobSelectVariable().query.filter_by(job_id=job.id)
        filter_vars = ExportJobIncludeValue().query.filter_by(job_id=job.id)
        data = get_data_export(job, select_vars, filter_vars)
        export_zip(data, job.dataset_name)
        job_complete(job, select_vars, filter_vars)
        db.session.commit()
