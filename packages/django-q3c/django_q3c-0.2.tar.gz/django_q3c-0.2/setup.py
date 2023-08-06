from setuptools import find_packages, setup
import versioneer

DESCRIPTION_FILES = ["pypi-intro.rst"]

long_description = []
import codecs
for filename in DESCRIPTION_FILES:
    with codecs.open(filename, 'r', 'utf-8') as f:
        long_description.append(f.read())
long_description = "\n".join(long_description)


setup(
    name='django_q3c',
    version=versioneer.get_version(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'Django>=3.2',
        'psycopg2',
    ],
    python_requires = '>=3.7',
    author='James Tocknell',
    author_email='james.tocknell@mq.edu.au',
    description='Use q3c with django',
    long_description = long_description,
    license = "3-clause BSD",
    keywords = "astronomy q3c",
    url = "https://django-q3c.readthedocs.io",
    project_urls={
        'Documentation': 'https://django-q3c.readthedocs.io',
        'Source': 'https://dev.aao.org.au/datacentral/web/django-q3c/',
        'Tracker': 'https://dev.aao.org.au/datacentral/web/django-q3c/issues',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
    cmdclass=versioneer.get_cmdclass(),
    include_package_data=True,
)
