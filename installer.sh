#!/bin/bash
#
# Linux: might requires java, ant: sudo apt-get install openjdk-7-jre openjdk-7-jdk ant
# MacOSX: requires ant: sudo apt-get install ant

VIRTUAL_ENV=virtenv

python3 -m pip install --user virtualenv
mkdir $VIRTUAL_ENV
python3 -m virtualenv $VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate

pushd $VIRTUAL_ENV
cp ../pylucene-6.5.0-src.tar.gz .
pip install pylucene-6.5.0-src.tar.gz

tar -xzf pylucene-6.5.0-src.tar.gz
pushd pylucene-6.5.0/
python3 jcc/setup.py build
python3 jcc/setup.py install
cp ../../Makefile . 
make
make install
popd

python3 -m pip install -r ../requirements.txt

keys='
TWITTER_KEY = ""
TWITTER_SECRET = ""
TWITTER_APP_KEY = ""
TWITTER_APP_SECRET = ""
'
PRIVATE=private.py
if [ ! -f "$PRIVATE" ]
then 
    echo "$keys" > "$PRIVATE"
fi
