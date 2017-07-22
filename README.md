# help50

[![Build Status](https://travis-ci.org/cs50/help50.svg?branch=master)](https://travis-ci.org/cs50/help50)

`help50` is a command line tool that makes an effort to translate some of the more arcane error messages that other tools, such as `clang` or `valgrind`, sometimes spit out. In this way, it serves as a "virtual TF" of sorts, hopefully helping nudge students in the right direction, so that they needn’t wait for a staff member at office hours when a little bit of translation of the error message is really all that’s needed to move on.

### Installation

```
pip install help50
```

### Usage

#### English

* `help50 ./foo`
* `CC=clang help50 make foo`
* `help50 clang -o foo foo.c`
* `./foo |& help50`
* `CC=clang make foo |& help50`
* `clang -o foo foo.c |& help50`

#### Spanish

Same as above but prefix with `LANGUAGE=es `.

# Internationalizing

## Creating PO for language XX

```
xgettext -L Python submit50.py
sed -i -e '1,6d' messages.po
sed -i -e '3,10d' messages.po
sed -i 's/CHARSET/UTF-8/' messages.po
vim messages.po # translate strings to XX
msgfmt messages.po
mkdir -p locale/XX/LC_MESSAGES
mv messages.mo messages.po locale/XX/LC_MESSAGES/
```

## Updating PO for language XX

Source: https://stackoverflow.com/a/7497395

```
echo "" > messages.po
find . -type f -iname "*.py" | xgettext -j -f -
msgmerge -N locale/XX/LC_MESSAGES/messages.po messages.po > new.po
mv new.po messages.po
msgfmt messages.po
mv -f messages.mo messages.po locale/XX/LC_MESSAGES/
```

# Contributing

```
pip install -e .
```
