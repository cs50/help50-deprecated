
if __import__("os").name == "nt":
    raise RuntimeError("submit50 does not support Windows directly. Instead, you should install the Windows Subsystem for Linux (https://docs.microsoft.com/en-us/windows/wsl/install-win10) and then install submit50 within that.")
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
    install_requires=["pexpect", "termcolor", "lib50>=1.1.10"],
    keywords="help50",
    name="help50",
    packages=["help50"],
    entry_points={
        "console_scripts": ["help50=help50.__main__:main"]
    },
    py_requires="3.6",
    url="https://github.com/cs50/help50",
    version="3.0.0"
)
