# Install with `pip install -e .`
# Run with `python -m amplrestapi`

from setuptools import find_packages, setup
import confuse


config = confuse.Configuration('amplrestapi', __name__)
version = config['version'].get()

install_requires = ['aiohttp==3.5.4',
                    'amplpy==0.6.7',
                    'asyncio==3.4.3',
                    'confuse==1.0.0',
                    'jsonschema==3.0.2']

setup(name='amplrestapi',
      version=version,
      description='Operative Search project combining Python and AMPL',
      platforms=['POSIX'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      zip_safe=False)
