import os

DB_NAME = os.environ.get('DB_NAME', 'zindarak')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 27017))
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
