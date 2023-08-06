from pathlib import Path
from setuptools import setup, find_namespace_packages

# Contents of local files
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()


setup(
    name='ultraspy',
    version='1.1',
    author='Pierre Ecarlat',
    author_email='pierre.ecarlat@gmail.com',
    description='Ultrasound toolbox for GPU',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/pecarlat/ultraspy',
    project_urls={
        'Documentation': 'https://ultraspy.readthedocs.io/en/latest/',
        'Bug Tracker': 'https://gitlab.com/pecarlat/ultraspy/-/issues/',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='ultrasound, python, beamforming, doppler',
    python_requires='>=3.8, <3.11',

    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'scipy>=1.10.1',
        'matplotlib>=3.6.3',
        'easydict>=1.10',
        'numba>=0.56.4',
        'h5py>=3.8.0',
        'py7zr>=0.20.5',
    ],
)
