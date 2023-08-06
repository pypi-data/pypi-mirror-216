from setuptools import setup, find_packages

setup(
    name='superagi_tools',
    version='1.0.1',
    description='A useful module for using tools from Superagi',
    author='superagi',
    author_email='mukunda@superagi.com',
    packages=find_packages(),
    install_requires=['pydantic', 'pyyaml'],
)
