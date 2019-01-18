#!/bin/bash -x

set -e

if [ ! -f setup.py ]; then
	echo "This script expects to be run in the toplevel source directory."
	exit 1
fi

rm -rf deb_dist
python setup.py --command-packages=stdeb.command sdist_dsc

cd deb_dist
cd $(/bin/ls -1 *.orig.tar.gz | sed -e 's/.orig.tar.gz//' | sed -e 's/_/-/')

cat >> debian/rules << EOF
override_dh_python2:
	dh_python2
	pycompile debian/python-*/usr/lib
	find debian/python-*/usr/lib -name \*.py -exec rm {} \;
EOF

fakeroot debian/rules binary
