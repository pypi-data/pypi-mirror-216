from setuptools import setup

def readme():
      with open('README.rst') as f:
            return f.read()

setup(name="Funny Jokes",
      version='0.1',
      description='Joke of the day',
      long_description=readme(),
      author='K',
      author_email="k@Gmail.com",
      license='MIT',
      packages=['pjokes'],
      install_requires=[
            'markdown',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points = {
        'console_scripts': ['Funny Jokes=pjokes.command_line:main'],
    },
      include_package_data=True
      )