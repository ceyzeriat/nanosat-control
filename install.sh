#!/bin/bash
export $WHERESEGSOL = $HOME/Documents/lib/segsol
export $WHEREPARAM = $HOME/.segsol
export $WHEREDATA = $HOME/tm_data

mkdir -p $WHERESEGSOL
mkdir -p $WHEREPARAM
mkdir -p $WHEREDATA

cd $WHERESEGSOL

git init
if [ ! -f $HOME/.gitconfig ]; then
    git config --global user.name "segsol"
    git config --global user.email "picsat.office@obspm.fr"
fi
git add remote origin https://git.obspm.fr/git/projets/Picsat/segsol
git pull origin master

echo "PICSAT" > $WHEREPARAM/callsign_destination
echo "ground" > $WHEREPARAM/callsign_source
echo "0" > $WHEREPARAM/tc_packet_id
echo "postgresql://postgres:<pass>@localhost:5432/picsat" > $WHEREPARAM/db_server
echo "postgres" > $WHEREPARAM/artichaut


