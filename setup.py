from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_packages():
    all_packages = find_packages()
    all_packages = [el for el in all_packages if el.startswith("tests") is False]
    return all_packages


setup(
    name='sphere-python-sdk',
    version='0.4.0',
    author='Sphere developers',
    author_email='hello@thesphereapp.com',
    description='Sharing sphere functionality with the world',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/thesphereapp/sphere-python-sdk',
    packages=get_packages(),
    install_requires=[
        'pydantic',
        'python-dateutil',
        'pymongo',
        'setuptools'
    ],
)