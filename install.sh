#!/bin/bash

REPONAME="segsol"
WHERESEGSOL="$HOME/Documents/lib/$REPONAME"
WHEREBINS="$HOME/Documents/bin"
WHEREPARAM="$HOME/.segsol"
WHEREDATA="$HOME/tm_data"

# create directories
mkdir -p $WHERESEGSOL
mkdir -p $WHEREPARAM
mkdir -p $WHEREDATA
mkdir -p $WHEREBINS

# update paths
echo '' >> $HOME/.bashrc
echo '' >> $HOME/.bashrc
echo '# segsol append' >> $HOME/.bashrc
echo "export PATH=$WHEREBINS:"'$PATH' >> $HOME/.bashrc
echo "export PYTHONPATH=$WHERESEGSOL:"'$PYTHONPATH' >> $HOME/.bashrc

cd $WHERESEGSOL

# init the git repo
git init
if [ ! -f $HOME/.gitconfig ]; then
    git config --global user.name "segsol"
    git config --global user.email "picsat.office@obspm.fr"
fi
git remote add origin https://git.obspm.fr/git/projets/Picsat/segsol

# grab code
git pull origin master

# create parameter files
echo "PICSAT" > $WHEREPARAM/callsign_destination
echo "ground" > $WHEREPARAM/callsign_source
echo "0" > $WHEREPARAM/tc_packet_id
echo "postgresql://postgres:<pass>@localhost:5432/picsat" > $WHEREPARAM/db_server
echo "postgres" > $WHEREPARAM/artichaut

# create the binaries

