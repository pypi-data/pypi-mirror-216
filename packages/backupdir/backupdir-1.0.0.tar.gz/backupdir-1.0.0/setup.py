from setuptools import setup

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='backupdir',
  version='1.0.0',
  author='IgorMan (IgorMan2005)',
  author_email='igorman2005@gmail.com',
  description='Python script copies the source directory (with all files and subdirectories) to the specified location and zips it.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/IgorMan2005/backupdir',
  packages=['backupdir'],
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python backupdir backup foder zip archive',
  project_urls={
    'Documentation': 'https://best-itpro.ru/news/backupdir/',
  },
  python_requires='>=3.6'
)