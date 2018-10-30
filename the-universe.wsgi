activate_this = '/var/www/the-universe/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import os, site, sys

site.addsitedir('/var/www/the-universe/env/lib/python2.7/site-packages')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))

sys.path.insert(0, '/var/www/the-universe')
sys.path.append('/var/www/the-universe/env/local/lib64/python2.7/site-packages')

def application(environ, start_response):
    for key in ['SQLALCHEMY_TRACK_MODIFICATIONS']:
        os.environ[key] = environ.get(key, '')

	from server import app as _application

    return _application(environ, start_response)
