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
    description="This is help50, a command-line tool that helps students understand error messages.",
    install_requires=["argparse", "backports.shutil_get_terminal_size", "requests", "ptyprocess", "termcolor"],
    keywords="help50",
    name="help50",
    scripts=["help50"],
    url="https://github.com/cs50/help50",
    version="2.0.0"
)
