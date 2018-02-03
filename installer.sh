#!/bin/bash
#
# Requires ant: $ sudo apt-get install ant

ROOT=$(dirname $0)
VIRTUAL_ENV=virtenv

pip install virtualenv
mkdir $VIRTUAL_ENV
virtualenv $VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate

mkdir $VIRTUAL_ENV/tmp-lucene
cp pylucene-6.5.0-src.tar.gz $VIRTUAL_ENV/tmp-lucene

pushd $VIRTUAL_ENV/tmp-lucene
tar -xzf pylucene-6.5.0-src.tar.gz

pushd pylucene-6.5.0
cp ../../$ROOT/Makefile . 
make
sudo make install
popd

popd
rm -rf tmp-lucene

keys='TWITTER_KEY = ""
TWITTER_SECRET = ""
TWITTER_APP_KEY = ""
TWITTER_APP_SECRET = ""'

PRIVATE=private.py
if [ ! -f "$PRIVATE" ]
then 
    echo "$keys" > "$PRIVATE"
fi
