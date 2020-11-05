#/bin/bash
tar cjpvf filesystem.tar.bz2 --directory filesystem .
docker build --tag heimdall .
