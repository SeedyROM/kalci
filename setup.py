import os

from distutils.core import setup

from kalci.settings import BASE_DIR


def get_package_deps(requirements_file='requirements.txt'):
    with open(os.path.join(BASE_DIR, requirements_file), 'r') as f:
        return [dep.split('==')[0] for dep in f.readlines() if dep]

setup(
    name = 'kalci',
    packages = ['kalci'], # this must be the same as the name above
    version = '0.1',
    description = 'A command line app for keeping track of things and calculating stuff.',
    author = 'Zack Kollar',
    author_email = 'zackkollar@gmail.com',
    url = 'https://github.com/SeedyROM/kalci', # use the URL to the github repo
    # download_url = 'https://github.com/peterldowns/kalci/archive/0.1.tar.gz', # I'll explain this in a second
    keywords = ['mundane', 'tasks', 'calcuation', 'day2day'], # arbitrary keywords
    classifiers = [],
    license = 'MIT',
    install_requires = get_package_deps()
)
