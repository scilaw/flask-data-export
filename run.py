#!/usr/bin/env python

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config.get('DEBUG'), host=app.config.get('HOST_IP'))
