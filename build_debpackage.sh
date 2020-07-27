#!/bin/bash

mkdir -p packages/DEBIAN
mkdir -p packages/usr/local/bin/
mkdir -p packages/usr/share/hvl/projectx/

echo """#!/bin/bash
python3 /usr/share/hvl/projectx/src/tray.py""" > packages/usr/local/bin/projectx
cp -r images locale src apps.gsettings-projectx.gschema.xml packages/usr/share/hvl/projectx
mkdir -p packages/usr/share/hvl/projectx/logs
size=$(du -s ./ | cut -f 1)
version=$(date +'%Y%m%d-%H%M%S')
date=$(date +'%d/%m/%Y-%H:%M:%S')
echo """Package: projectx
Version: $version
Installed-Size: $size
Maintainer: Ridvan Tulemen <ridvantulemen@gmail.com>
Date : $date
Depends: python3-pil, python3-gi, graphicsmagick-imagemagick-compat
Architecture: amd64
Description: Projectx
""" > packages/DEBIAN/control

find ./ -type f ! -regex '.*?DEBIAN.*' -exec md5sum {} \; > packages/DEBIAN/md5sums
echo """chmod +x /usr/local/bin/projectx
cp /usr/share/hvl/projectx/apps.gsettings-projectx.gschema.xml /usr/share/glib-2.0/schemas/
glib-compile-schemas /usr/share/glib-2.0/schemas/""" > packages/DEBIAN/postinst
chmod +x packages/DEBIAN/postinst
version=$(date +'%Y%m%d-%H%M%S')
dpkg-deb -Zgzip --build ./packages projectx_$version.deb
