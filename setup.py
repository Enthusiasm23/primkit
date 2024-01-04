from setuptools import setup, find_packages

# Read dependencies in requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

# Configure additional installation options
extra_options = {
    'zip_safe': False,
    'include_package_data': True,
    'python_requires': '>=3.6',
    'project_urls': {
        'Documentation': 'https://primkit.readthedocs.io/',
        'Source': 'https://github.com/Enthusiasm23/primkit',
        'Tracker': 'https://github.com/Enthusiasm23/primkit/issues',
    },
    'extras_require': {
        'dev': ['check-manifest'],
        'test': ['coverage'],
    }
}


setup(
    name='primkit',
    version='0.1.4',
    author='LiBao Feng',
    author_email='lbfeng23@gmail.com',
    description='A primer design assistant tool for convenient and efficient primer design and result preprocessing.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Enthusiasm23/primkit',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=required,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    **extra_options
)
