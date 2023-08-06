from setuptools import setup, find_packages


setup(
    name='threed_optix',
    version='1.0.1',
    license='',
    author="Elika Ron",
    author_email='alikaron@3doptix.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/3doptix/3DOptix-Canvas-API',
    keywords='',
    install_requires=[
        'requests'
    ]
)
