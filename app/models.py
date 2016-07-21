#!/usr/bin/env python

from flask.ext.security import UserMixin, RoleMixin
from datetime import datetime
from app import db


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    # Flask Security basics
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    # Confirmation
    confirmed_at = db.Column(db.DateTime())
    # Flask Security tracking
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))
    login_count = db.Column(db.Integer)
    # Roles
    roles = db.relationship('Role',
                            secondary=roles_users,
                            backref=db.backref('users',
                                               lazy='dynamic'))


class ExportJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    status = db.Column(db.String(255))
    pid = db.Column(db.SmallInteger)
    dataset_name = db.Column(db.String(255))
    do_sampling = db.Column(db.Boolean)
    sample_percent = db.Column(db.SmallInteger)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           nullable=False,
                           server_default=db.text('0'))
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)


class ExportJobSelectVariable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer(), db.ForeignKey('export_job.id'))
    selected_variable = db.Column(db.String(255))


class ExportJobIncludeValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer(), db.ForeignKey('export_job.id'))
    variable_name = db.Column(db.String(255))
    variable_value = db.Column(db.String(255))


class Downloads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer(), db.ForeignKey('export_job.id'))
    ip = db.Column(db.String(45))
    downloaded_at = db.Column(db.DateTime())
