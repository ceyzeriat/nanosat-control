#!/bin/bash

# input can be "all", "server", "desk"

if [ $# -eq 0 ];
  then DOINSTALL="server"
  else DOINSTALL="$1"
fi


REPONAME="segsol"
WHERESEGSOL="$HOME/Documents/lib/$REPONAME"
WHEREBINS="$HOME/Documents/bin"
WHEREPARAM="$HOME/.segsol"
WHEREDATA="$HOME/tm_data"
DESKTOP="$HOME/Desktop"
IPY=$(which ipython)
INITPWD=$(pwd)


############################################


if [ "$DOINSTALL" == "all" -o "$DOINSTALL" == "server" ]; then
    # create directories
    mkdir -p $WHERESEGSOL
    mkdir -p $WHEREPARAM
    mkdir -p $WHEREDATA
    mkdir -p $WHEREBINS
    mkdir -p "$HOME/seglog"

    # update paths
    echo '' >> $HOME/.bashrc
    echo '' >> $HOME/.bashrc
    echo '# segsol append' >> $HOME/.bashrc
    echo "export PATH=$WHEREBINS:"'$PATH' >> $HOME/.bashrc
    echo "export WHERESEGSOL=$WHERESEGSOL" >> $HOME/.bashrc
    echo 'export PYTHONPATH=$WHERESEGSOL:$PYTHONPATH' >> $HOME/.bashrc

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

    # make the copy of param_all
    cp ./param/param_all_example.py ./param/param_all.py

    # move binaries
    chmod a+x bins/*
    mv bins/log* $WHEREBINS/

    # create parameter files
    echo 'PICSAT' > $WHEREPARAM/callsign_destination
    echo 'ground' > $WHEREPARAM/callsign_source
    echo '0' > $WHEREPARAM/tc_packet_id
    echo 'postgresql://postgres:<pass>@localhost:5432/picsat' > $WHEREPARAM/db_server
    echo 'postgres' > $WHEREPARAM/artichaut
    echo 'You wish!' > $WHEREPARAM/perefouras

    # create the binaries
    cd $WHEREBINS

    echo '#!/bin/bash' > piccontrol
    chmod a+x piccontrol
    cp piccontrol picchat
    echo 'if [[ $1 == "gui" ]]' >> piccontrol
    echo 'then' >> piccontrol
    cp piccontrol piclisten
    cp piccontrol picwatch
    cp piccontrol picsave
    cp piccontrol picshow
    cp piccontrol picspy    

    BASICFONT="-bg black -fg lightgrey -fa 'Monospace' -fs 10"

    echo "    xterm -T 'Control' $BASICFONT -geometry 80x24-0+200 -e '$IPY -i $WHERESEGSOL/control.py';" >> piccontrol
    echo "else" >> piccontrol
    echo "    $IPY -i $WHERESEGSOL/control.py" >> piccontrol
    echo "fi" >> piccontrol

    echo "    xterm -T 'Listen' $BASICFONT -geometry 25x4+0+50 -e '$IPY -i $WHERESEGSOL/listen.py';" >> piclisten
    echo "else" >> piclisten
    echo "    $IPY -i $WHERESEGSOL/listen.py" >> piclisten
    echo "fi" >> piclisten

    echo "    xterm -T 'Watch' $BASICFONT -geometry 80x35+0+140 -e '$IPY -i $WHERESEGSOL/watch.py';" >> picwatch
    echo "else" >> picwatch
    echo "    $IPY -i $WHERESEGSOL/watch.py" >> picwatch
    echo "fi" >> picwatch

    echo "    xterm -T 'Save' $BASICFONT -geometry 25x4+210+50 -e '$IPY -i $WHERESEGSOL/save.py';" >> picsave
    echo "else" >> picsave
    echo "    $IPY -i $WHERESEGSOL/save.py" >> picsave
    echo "fi" >> picsave

    echo "    xterm -T 'Show' $BASICFONT -geometry 80x30+400+200 -e '$IPY -i $WHERESEGSOL/show.py';" >> picshow
    echo "else" >> picshow
    echo "    $IPY -i $WHERESEGSOL/show.py" >> picshow
    echo "fi" >> picshow

    echo "    xterm -T 'Spy' $BASICFONT -geometry 80x10+30-50 -e '$IPY -i $WHERESEGSOL/spy.py';" >> picshow
    echo "else" >> picspy
    echo "    $IPY -i $WHERESEGSOL/spy.py" >> picspy
    echo "fi" >> picspy    

    echo "xterm -T 'Chat' $BASICFONT -geometry 80x15-0+0 -e /bin/bash -l -c '$WHEREBINS/logdisp';" >> picchat
fi


############################################


if [ "$DOINSTALL" == "all" -o "$DOINSTALL" == "desk" ]; then
    # create directory
    mkdir -p $DESKTOP

    # create the shortcuts on Desktop
    cd $DESKTOP
    echo '[Desktop Entry]' > PicControl.desktop
    echo 'Version=1.0' >> PicControl.desktop
    echo 'Type=Application' >> PicControl.desktop
    chmod a+x PicControl.desktop
    cp PicControl.desktop PicListen.desktop
    cp PicControl.desktop PicSave.desktop
    cp PicControl.desktop PicWatch.desktop
    cp PicControl.desktop PicShow.desktop
    cp PicControl.desktop PicChat.desktop

    echo 'Name=PicControl' >> PicControl.desktop
    echo 'Comment=' >> PicControl.desktop
    echo 'Exec='"$WHEREBINS"'/piccontrol gui' >> PicControl.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/control.gif' >> PicControl.desktop
    echo 'Path='"$HOME" >> PicControl.desktop
    echo 'Terminal=false' >> PicControl.desktop
    echo 'StartupNotify=false' >> PicControl.desktop

    echo 'Name=PicListen' >> PicListen.desktop
    echo 'Comment=' >> PicListen.desktop
    echo 'Exec='"$WHEREBINS"'/piclisten gui' >> PicListen.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/listen.gif' >> PicListen.desktop
    echo 'Path='"$HOME" >> PicListen.desktop
    echo 'Terminal=false' >> PicListen.desktop
    echo 'StartupNotify=false' >> PicListen.desktop

    echo 'Name=PicSave' >> PicSave.desktop
    echo 'Comment=' >> PicSave.desktop
    echo 'Exec='"$WHEREBINS"'/picsave gui' >> PicSave.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/save.gif' >> PicSave.desktop
    echo 'Path='"$HOME" >> PicSave.desktop
    echo 'Terminal=false' >> PicSave.desktop
    echo 'StartupNotify=false' >> PicSave.desktop

    echo 'Name=PicWatch' >> PicWatch.desktop
    echo 'Comment=' >> PicWatch.desktop
    echo 'Exec='"$WHEREBINS"'/picwatch gui' >> PicWatch.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/watch.gif' >> PicWatch.desktop
    echo 'Path='"$HOME" >> PicWatch.desktop
    echo 'Terminal=false' >> PicWatch.desktop
    echo 'StartupNotify=false' >> PicWatch.desktop

    echo 'Name=PicShow' >> PicShow.desktop
    echo 'Comment=' >> PicShow.desktop
    echo 'Exec='"$WHEREBINS"'/picshow gui' >> PicShow.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/show.gif' >> PicShow.desktop
    echo 'Path='"$HOME" >> PicShow.desktop
    echo 'Terminal=false' >> PicShow.desktop
    echo 'StartupNotify=false' >> PicShow.desktop

    echo 'Name=PicSpy' >> PicSpy.desktop
    echo 'Comment=' >> PicSpy.desktop
    echo 'Exec='"$WHEREBINS"'/picspy gui' >> PicSpy.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/spy.gif' >> PicSpy.desktop
    echo 'Path='"$HOME" >> PicSpy.desktop
    echo 'Terminal=false' >> PicSpy.desktop
    echo 'StartupNotify=false' >> PicSpy.desktop    

    echo 'Name=PicChat' >> PicChat.desktop
    echo 'Comment=' >> PicChat.desktop
    echo 'Exec='"$WHEREBINS"'/picchat' >> PicChat.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/chat.gif' >> PicChat.desktop
    echo 'Path='"$HOME" >> PicChat.desktop
    echo 'Terminal=false' >> PicChat.desktop
    echo 'StartupNotify=false' >> PicChat.desktop
fi

# got back where we were
cd "$INITPWD"
