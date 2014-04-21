### required packages
yum install gcc*
yum install make
yum install curl*
yum install libcurl*
yum install openssl*
yum install expat-devel
yum install perl-ExtUtils-MakeMaker

## installation
./configure --prefix=$HOME --without-tcltk 
make
## make NO_CURL=1 NO_MSGFMT=YesPlease NO_TCLTK=YesPlease NO_GETTEXT=YesPlease prefix=/usr/local install
make install

## git
https://git-core.googlecode.com/files/git-1.9.0.tar.gz


