import setuptools


VERSION = "1.0.1"

with open("README.md", "r", encoding="utf-8") as readme:
    DESC_LONG = readme.read()


setuptools.setup(
    name="serialdevicehandler",
    version=VERSION,
    author="Salliii",
    description="A python library to run commands on a device via serial port",
    long_description_content_type="text/markdown",
    long_description=DESC_LONG,
    url="https://github.com/Salliii/serialdevicehandler",
    packages=setuptools.find_packages(),
    install_requires=[],
    keywords=["python", "library", "serial device", "serial interface", "commands", "execute"]
)


"""
    Setup:
    python .\setup.py sdist bdist_wheel

    Upload to PyPi:
    twine upload .\dist\<packname>-<version>
"""