from setuptools import setup

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='screen_cls',
  version='1.0.6',
  author='IgorMan (IgorMan2005)',
  author_email='igorman2005@gmail.com',
  description='Python script for clearing screen for any OS\'s: Windows, MAC, Linux',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/IgorMan2005/screen_cls',
  packages=['screen_cls'],
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python screen cls',
  project_urls={
    'Documentation': 'https://best-itpro.ru/news/screen_cls/',
  },
  python_requires='>=3.6'
)