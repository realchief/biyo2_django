
# WARNING: this script describes the installation of the application from scratch to the CLEAN folder on webfaction server
# If the folder already have the application or other files - they will be corrupted or removed

# Execute these steps by hands step-by-step and change th values to corresponding (names, git branch, etc)

# Before this file make the app, website, domain and link them together

#
HOME_DIR=`dirname ~/tmp`
APPNAME=pulsewallet
APP_DIR=$HOME_DIR/webapps/$APPNAME
GIT_REPO="git@bitbucket.org:pulsepay/biyo-dashboard.git"
GIT_BRANCH='stable1.2.0'

cd $APP_DIR

# remove default stuff
rm -rf bin
rm -rf lib
rm -rf myproject

# get the code (to other directory first as this one is not empty, then move to current)
git clone $GIT_REPO ./repodir
mv repodir/* ./
mv repodir/.g* ./
rm -rf repodir

git checkout $GIT_BRANCH

APACHE_PORT=`cat apache2/conf/httpd.conf | grep Listen | sed -e s/Listen\ //`

cp -r ./config/apache/* apache2/conf/
# fix apache's port
sed -i -r s/Listen\ [0-9]+/Listen\ $APACHE_PORT/ apache2/conf/httpd.conf
# create directories for logs
ls -1 config/apache/vhosts/ | sed -r s/.vhost// | xargs -I {} mkdir -p "$HOME_DIR/logs/user/{}"

mkdir static
mkdir media
mkdir storage

sh config/buildenv.sh
sh ./make.sh

./apache2/bin/stop
./apache2/bin/start
