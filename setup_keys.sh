#!/bin/sh

FILE=instance/app.cfg

SALT=`echo 'import uuid; print(uuid.uuid4().hex)' | python`
perl -pi -e "s?^SECURITY_PASSWORD_SALT.*?SECURITY_PASSWORD_SALT = '${SALT}'?" ${FILE}

KEY=`echo 'import os, base64; print(base64.urlsafe_b64encode(os.urandom(24)))' | python`
perl -pi -e "s?^SECRET_KEY.*?SECRET_KEY= '${KEY}'?" ${FILE}
