DATABASE = os.environ.get(
    'DATABASE_URL', 'dbname=learning_journal'
)

ADMIN_USERNAME = os.environ.get(
    'ADMIN_USERNAME', 'admin'
)

ADMIN_PASSWORD = os.environ.get(
    'ADMIN_PASSWORD', pbkdf2_sha256.encrypt('admin')

)

SECRET_KEY = os.environ.get(
    'FLASK_SECRET_KEY', 'C\x93d\xd8\xe0wcK\xcb\xc3\xd0\xab\x04\xf0\xd0?\xba\xfd\xa0\xbc\xca\xe4a\xd1aE\xcb\x03\xd7T[\xf8'
)
