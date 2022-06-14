import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sphere-interface',
    version='0.0.1',
    author='Sphere ',
    author_email='hello@thesphereapp.com',
    description='Sharing sphere functionality with the world',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/thesphereapp/sphere-interface',
    license='MIT',
    packages=['sphere-interface'],
    install_requires=['pydantic', 'python-dateutil'],
)
