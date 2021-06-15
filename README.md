# help50

[![Build Status](https://travis-ci.org/cs50/help50.svg?branch=main)](https://travis-ci.org/cs50/help50)

`help50` is a command line tool that makes an effort to translate some of the more arcane error messages that other tools, such as `clang` or `valgrind`, sometimes spit out. In this way, it serves as a "virtual TF" of sorts, hopefully helping nudge students in the right direction, so that they needn’t wait for a staff member at office hours when a little bit of translation of the error message is really all that’s needed to move on.

### Installation

```
pip install help50
```

### Usage

* `help50 ./foo`
* `CC=clang help50 make foo`
* `help50 clang -o foo foo.c`
* `./foo |& help50`
* `CC=clang make foo |& help50`
* `clang -o foo foo.c |& help50`
