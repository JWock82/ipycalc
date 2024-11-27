import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipycalc",
    version="0.0.61",
    author="D. Craig Brinck, PE, SE",
    author_email="Building.Code@outlook.com",
    description="Clean looking engineering calculations for IPython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JWock82/ipycalc.git",
    packages=setuptools.find_packages(include=['ipycalc', 'ipycalc.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'jupyterlab',
        'nbconvert>=6.0',
    ],
    include_package_data=True,
    entry_points={
        'nbconvert.exporters': [
            'ipycalc = ipycalc:ipycalcExporter',
            ]
    }
)
