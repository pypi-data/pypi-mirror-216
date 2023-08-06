import os

INSTALLED_APPS = [
    'django_q3c',
    'q3c_test',
]

# ---------------------- Database ----------------------
DATABASES = {
    'default': {
        'ENGINE': 'django_q3c.db',
        'HOST': os.environ.get('POSTGRES_HOST', ''),
        'PORT': os.environ.get('POSTGRES_PORT', ''),
        'NAME': 'q3c_' + os.environ.get('POSTGRES_DB', ''),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'TEST': {
            'NAME': 'test_q3c_' + os.getenv('POSTGRES_DB'),
        },
    },
}
