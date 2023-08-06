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
    version='0.1.8',
    packages=['Generation_Image_Gaston'],
    install_requires=[
        'selenium',
        'undetected_chromedriver'
    ],
    author='Gaston Robé',
    author_email='gaston01.robe@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='GASTON PROCESSING COMPUTER VISION',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
)
