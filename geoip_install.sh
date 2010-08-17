apt-get install zlibc zlib1g-dev libssl-dev
wget http://www.maxmind.com/download/geoip/api/c/GeoIP-1.4.4.tar.gz
tar xvf GeoIP-1.4.4.tar.gz
cd GeoIP-1.4.4
./configure
make
make install


wget http://www.maxmind.com/download/geoip/api/python/GeoIP-Python-1.2.2.tar.gz
tar xvf GeoIP-Python-1.2.2.tar.gz
cd GeoIP-Python-1.2.2
python setup.py install

ldconfig