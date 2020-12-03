import os

# *****************************
# Environment specific settings
# *****************************

# DO NOT use "DEBUG = True" in production environments
DEBUG = True

# DO NOT use Unsecure Secrets in production environments
# Generate a safe one with:
#     python -c "import os; print repr(os.urandom(24));"

#'This is an UNSECURE Secret. CHANGE THIS for production environments.'
SECRET_KEY = "\xc8$\xb2BiT\x13x\xd0\xdaq\xf1,^\x15b/\xa7 \xd4b'\xda\x1a\x8fh\xca.\xbd\xb0c\x25"

# SQLAlchemy settings
#TODO
SQLALCHEMY_DATABASE_URI = '/Users/am/caypt_dev_v3/app.sqlite'
#TODO
SQLALCHEMY_DATABASE_URI_LOCAL = '/Users/am/caypt_dev_v3/app.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids a SQLAlchemy Warning
CURRENT_EVENT = 2

# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'caypt.web@gmail.com'
MAIL_PASSWORD = 'CaYPTgogo2019'
MAIL_DEFAULT_SENDER = 'caypt.web@gmail.com'

# Sendgrid settings
SENDGRID_API_KEY='place-your-sendgrid-api-key-here'

WKHTMLTOPDF_BIN_PATH = r'C:\Program Files\wkhtmltopdf\bin' #path to your wkhtmltopdf installation.
# PDF_DIR_PATH =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'pdf')
PDF_DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'app', 'static', 'pdfs')

# Flask-User settings
USER_APP_NAME = "CaYPT - DEV"  # Shown in and email templates and page footers
USER_ENABLE_EMAIL = True  # Enable email authentication
USER_ENABLE_USERNAME = False  # Disable username authentication
USER_EMAIL_SENDER_NAME = USER_APP_NAME
USER_EMAIL_SENDER_EMAIL = "noreply@caypt.org"
USER_REQUIRE_RETYPE_PASSWORD = True  # Enable retype password

ADMINS = [
    '"Admin One" <admin1@gmail.com>',
    ]
