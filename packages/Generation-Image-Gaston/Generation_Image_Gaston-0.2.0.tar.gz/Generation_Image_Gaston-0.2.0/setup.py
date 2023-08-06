from setuptools import setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
    name='Generation_Image_Gaston',
    version='0.2.0',
    packages=['Generation_Image_Gaston'],
    install_requires=[
        'selenium',
        'undetected_chromedriver'
    ],
    author='Gaston Robé',
    author_email='gaston01.robe@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Gaston Robe 13 ans',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
)
