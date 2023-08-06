from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='mail-sender-1.0',
    version='1.0',
    author='AdanEinstein',
    author_email='adaneinstein@gmail.com',
    description = "Utility class for sending emails",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages()
)

