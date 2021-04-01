import os
from app import app
from app.models import initialize_db

if __name__ == '__main__':
    if os.environ.get('INITIALIZE_DB') == 'true':
        print('Initializing database.')
        initialize_db()
        del os.environ['INITIALIZE_DB']
    app.run()

