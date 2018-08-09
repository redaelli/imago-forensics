from setuptools import setup

setup(name='imago',
      version='1.0',
      description='Imago is a python tool that extract digital evidences from images. ',
      url='https://github.com/redaelli/imago-forensics',
      author='Matteo Redaelli',
      author_email='solventdev@gmail.com',
      install_requires=['exifread==2.1.2', 'python-magic==0.4.15','argparse==1.4.0','pillow==5.2.0','nudepy==0.4','imagehash==4.0'],
      license='MIT',
      scripts=['bin/imago'],
      packages=['imago'],
      zip_safe=False)
