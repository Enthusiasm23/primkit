from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='primertools',
    version='0.1.0',
    author='LiBao Feng',
    author_email='lbfeng23@gmail.com',
    description='A primer design assistant tool for convenient and efficient primer design and result preprocessing.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Enthusiasm23/primertools',
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False
)
