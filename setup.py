from setuptools import setup

setup(
    author="CS50",
    author_email="sysadmins@cs50.harvard.edu",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development"
    ],
    license="GPLv3",
    description="This is help50, a command-line tool that helps students understand error messages.",
    install_requires=["argparse", "requests", "pexpect", "termcolor"],
    keywords="help50",
    name="help50",
    scripts=["help50"],
    py_requires="3.6",
    url="https://github.com/cs50/help50",
    version="2.0.1"
)
