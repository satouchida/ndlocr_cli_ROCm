#!/bin/bash
set -ex

apt-get update
apt-get install -y libgl1-mesa-dev libglib2.0-0 zip git python3-pip wget g++ cmake curl build-essential libboost-dev libboost-filesystem-dev libboost-system-dev libboost-regex-dev libgeos-dev autoconf libtool

ln -sf /usr/bin/python3 /usr/bin/python

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

export PATH="/root/.cargo/bin:${PATH}"
export LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

wget http://www.phontron.com/kytea/download/kytea-0.4.7.tar.gz
tar xzvf kytea-0.4.7.tar.gz
cd kytea-0.4.7
./configure --prefix=/usr/local
make
make install
ldconfig
