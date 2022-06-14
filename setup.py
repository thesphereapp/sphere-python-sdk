import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sphere-python-sdk',
    version='0.0.2',
    author='Sphere developers',
    author_email='hello@thesphereapp.com',
    description='Sharing sphere functionality with the world',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/thesphereapp/sphere-python-sdk',
    license='MIT',
    packages=['sphere'],
    install_requires=[
        'pydantic',
        'python-dateutil',
        'pymongo',
        'setuptools'
    ],
)
