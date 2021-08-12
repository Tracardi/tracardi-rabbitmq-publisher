from setuptools import setup

with open("tracardi_rabbitmq_publisher/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-rabbitmq-publisher',
    version='0.1.2',
    description='The purpose of this plugin is publish payload to rabbitmq source.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Risto Kowaczewski',
    author_email='risto.kowaczewski@gmail.com',
    packages=['tracardi_rabbitmq_publisher'],
    install_requires=[
        'tracardi_plugin_sdk',
        'kombu~=5.1.0',
        'pydantic~=1.8.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)
