import os
import inspect
from setuptools import setup

# The directory containing this file
this_script_dir = os.path.dirname(inspect.stack()[0][1])

# The text of the README file
with open(os.path.join(this_script_dir, "../README.md"), 'r') as readme_file:
    readme = readme_file.read()

# This call to setup() does all the work
setup(
    name="rcdb-web",
    version="0.9.1",
    description="RCDB Web - Run Conditions DataBase web interface",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/JeffersonLab/rcdb",
    author="Dmitry Romanov",
    author_email="romanov@jlab.org",
    license="MIT",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["rcdb_web"],
    include_package_data=True,
    setup_requires=["rcdb", "flask"],
    install_requires=["rcdb", "flask"],
    entry_points={
        "console_scripts": [
            "rcdbweb=rcdb_web:run_rcdb_web",
        ]
    },
)
