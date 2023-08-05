import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="impoasdiff",
    version=os.environ.get("VER", "0.0.4"),
    author="Yash Thadani",
    author_email="yash.thadani@imperva.com",
    description="Open API diff tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    py_modules=["generate_diff", "file_handler", "diff_handler", "args_manager", "utils"], 
    data_files=['impoasdiff/templates/report_v3.html'],
    # package_dir={'':'src/imp-oasdiffgen'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    entry_points = {'console_scripts': ['impoasdiff = impoasdiff.generate_diff:main']},

     install_requires = [
        # "idna==2.10",
        "Jinja2==3.1.2",
        "macholib==1.16.2",
        "MarkupSafe==2.1.3",
        "pyinstaller==5.12.0",
        "pyinstaller-hooks-contrib==2023.3",
    ],
    include_package_data=True,
)
