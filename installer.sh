#!/bin/bash

VIRTUAL_ENV=virtenv

mkdir $VIRTUAL_ENV

python -m pip install --user virtualenv
python -m virtualenv $VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate

pushd $VIRTUAL_ENV

cp ../pylucene-6.5.0-src.tar.gz .
pip install pylucene-6.5.0-src.tar.gz
tar -xzf pylucene-6.5.0-src.tar.gz

pushd pylucene-6.5.0/
python jcc/setup.py build
python jcc/setup.py install
cp ../../Makefile . 
make
sudo make install
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
