from setuptools import setup

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='openai-image',
  version='1.0.4',
  author='IgorMan',
  author_email='igorman2005@gmail.com',
  description='Python script for generating image from text by Open AI',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/IgorMan2005/openai_image/',
  packages=['openai_image'],
  install_requires=['openai'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='openai image api open ai python',
  project_urls={
    'Documentation': 'https://best-itpro.ru/news/openai_image/',
  },
  python_requires='>=3.6'
)
