from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='primkit',
    version='0.1.0',
    author='LiBao Feng',
    author_email='lbfeng23@gmail.com',
    description='A primer design assistant tool for convenient and efficient primer design and result preprocessing.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Enthusiasm23/primkit',
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False
)
