from setuptools import setup, find_packages

setup(
    name="homeserver",
    version="0.0.1",
    packages=find_packages(),
    description="Self-hosting for Python devs who love Matrix.",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author="Mo Balaa",
    author_email="balaa@fractalnetworks.co",
    license="AGPLv3",
    url="http://github.com/username/my_package",
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
