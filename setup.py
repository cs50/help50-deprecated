from glob import glob
from os import walk
from os.path import join, splitext
from setuptools import setup
from subprocess import call

def create_mo_files():
    """Compiles .po files in local/LANG to .mo files and returns them as array of data_files"""

    mo_files=[]
    for prefix in glob("locale/*"):
        for _,_,files in walk(prefix):
            for file in files:
                if file.endswith(".po"):
                    po_file = join(prefix, file)
                    mo_file = splitext(po_file)[0] + ".mo"
                    call(["msgfmt", "-o", mo_file, po_file])
                    mo_files.append((join("help50", prefix, "LC_MESSAGES"), [mo_file]))

    return mo_files

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
    data_files=create_mo_files(),
    url="https://github.com/cs50/help50",
    version="2.0.0"
)
