from setuptools import setup, find_packages


setup(
    name='threed_optix',
    version='1.0',
    license='',
    author="",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/3doptix/3DOptix-Canvas-API',
    keywords='3dapi',
    install_requires=[
          'requests',
      ],

)
