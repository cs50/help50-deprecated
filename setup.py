from setuptools import setup

setup(name="help50-client",
      version="2.0",
      description="This is help50, a command-line tool that helps students understand error messages.",
      url="https://github.com/cs50/help50",
      install_requires = ["argparse", "backports.shutil_get_terminal_size", "requests", "ptyprocess", "termcolor"])


