#coding=utf8
import os
from setuptools import setup, Command

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [
    'pyramid >= 1.5',
    ]

test_requires = [
    'pytest',
    'pytest-capturelog',
    'webtest',
    'deform',
    'colander',
    'formencode',
    'schema',
]

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(name='pyramid_restful_toolkit',
      version='1.0.3.1',
      description='Some toolkits for RESTful API development in Pyramid.',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Học .T Đỗ',
      author_email='hoc3010@gmail.com',
      url='https://github.com/tarzanjw/pyramid_restful_toolkit',
      keywords='web wsgi bfg pylons pyramid restful toolkit',
      packages=['pyramid_restful_toolkit', ],
      include_package_data=True,
      zip_safe=False,
      test_suite='pyramid_restful_toolkit',
      install_requires=requires,
      tests_require=requires + test_requires,
      cmdclass = {'test': PyTest},
      entry_points='',
      )
