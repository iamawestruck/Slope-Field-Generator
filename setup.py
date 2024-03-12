import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="field-generator",
    version="0.1.2",
    author="EQIKE",
    author_email="lc20-0098@lclark.edu",
    packages=["field_generator"],
    description="A simple slope field generator",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamawestruck/Slope-Field-Generator",
    license='MIT',
    python_requires='>=3.8',
    install_requires=["matplotlib", "scipy"]
)
