from setuptools import setup, find_packages

requirements = [
    "requests",
    "websocket-client"
]

long_description ="""By: nxslayer\nInstall: pip install user_discord"""

setup(
    name="user_discord",
    license="MIT",
    author="nxSlayer",
    version="1.3.2",
    author_email="princediscordslay@gmail.com",
    description="Library for discord bots.",
    url="https://github.com/nxSlayer/user-discord",
    packages=find_packages(),
    long_description=long_description,
    install_requires=requirements,
    keywords=[
        'user_discord',
        'user-discord',
    ],
    python_requires='>=3.6',
)