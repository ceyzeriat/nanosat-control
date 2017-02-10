#!/bin/bash

REPONAME="segsol"
WHERESEGSOL="$HOME/Documents/lib/$REPONAME"
WHEREBINS="$HOME/Documents/bin"
WHEREPARAM="$HOME/.segsol"
WHEREDATA="$HOME/tm_data"
DESKTOP="$HOME/Desktop"

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
cd $WHEREBINS

echo '#!/bin/bash' > piccontrol
chmod a+x piccontrol
cp piccontrol piclisten
cp piccontrol picwatch
cp piccontrol picsave

echo "xterm -T 'Control' -bg black -fg lightgrey -fa 'Monospace' -fs 10 -geometry 80x24+30+400 -e '/home/kirk/anaconda3/bin/ipython -i /home/kirk/Documents/lib/segsol/control.py'" >> piccontrol

echo "xterm -T 'Listen' -bg black -fg lightgrey -fa 'Monospace' -fs 10 -geometry 80x10+30-50 -e '/home/kirk/anaconda3/bin/ipython -i /home/kirk/Documents/lib/segsol/listen.py'" >> piclisten

echo "xterm -T 'Watch' -bg black -fg lightgrey -fa 'Monospace' -fs 10 -geometry 150x12+30+150 -e '/home/kirk/anaconda3/bin/ipython -i /home/kirk/Documents/lib/segsol/watch.py'" >> picwatch

echo "xterm -T 'Save' -bg black -fg lightgrey -fa 'Monospace' -fs 10 -geometry 80x10-30+150 -e '/home/kirk/anaconda3/bin/ipython -i /home/kirk/Documents/lib/segsol/save.py'" >> picsave

# create the shortcuts on Desktop
cd $DESKTOP
echo '[Desktop Entry]' > PicControl.desktop
echo 'Version=1.0' >> PicControl.desktop
echo 'Type=Application' >> PicControl.desktop
chmod a+x PicControl.desktop
cp PicControl.desktop PicListen.desktop
cp PicControl.desktop PicSave.desktop
cp PicControl.desktop PicWatch.desktop

echo 'Name=PicControl' >> PicControl.desktop
echo 'Comment=' >> PicControl.desktop
echo 'Exec='"$WHEREBINS"'/piccontrol' >> PicControl.desktop
echo 'Icon='"$WHERESEGSOL"'/img/control.gif' >> PicControl.desktop
echo 'Path=' >> PicControl.desktop
echo 'Terminal=false' >> PicControl.desktop
echo 'StartupNotify=false' >> PicControl.desktop

echo 'Name=PicListen' >> PicListen.desktop
echo 'Comment=' >> PicListen.desktop
echo 'Exec='"$WHEREBINS"'/piclisten' >> PicListen.desktop
echo 'Icon='"$WHERESEGSOL"'/img/listen.gif' >> PicListen.desktop
echo 'Path=' >> PicListen.desktop
echo 'Terminal=false' >> PicListen.desktop
echo 'StartupNotify=false' >> PicListen.desktop

echo 'Name=PicSave' >> PicSave.desktop
echo 'Comment=' >> PicSave.desktop
echo 'Exec='"$WHEREBINS"'/picsave' >> PicSave.desktop
echo 'Icon='"$WHERESEGSOL"'/img/save.gif' >> PicSave.desktop
echo 'Path=' >> PicSave.desktop
echo 'Terminal=false' >> PicSave.desktop
echo 'StartupNotify=false' >> PicSave.desktop

echo 'Name=PicWatch' >> PicWatch.desktop
echo 'Comment=' >> PicWatch.desktop
echo 'Exec='"$WHEREBINS"'/picwatch' >> PicWatch.desktop
echo 'Icon='"$WHERESEGSOL"'/img/watch.gif' >> PicWatch.desktop
echo 'Path=' >> PicWatch.desktop
echo 'Terminal=false' >> PicWatch.desktop
echo 'StartupNotify=false' >> PicWatch.desktop
