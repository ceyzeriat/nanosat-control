#!/bin/bash

# input can be "all", "server", "desk", "bdd"

REPONAME="segsol"
SCRIPTNAME="scripts"
WHERESEGSOL="$HOME/Documents/lib/$REPONAME"
WHEREBDD="$HOME/Documents/lib/bdd"
WHERESCRIPTS="$HOME/Documents/$SCRIPTNAME"
WHEREBINS="$HOME/Documents/bin"
WHEREPARAM="$HOME/.segsol"
WHEREDATA="$HOME/tm_data"
DESKTOP="$HOME/Bureau"
WHEREPYENV="$HOME/pythonsegsol"


function clearterm {
    echo -e "\\033c"
    echo -e "\e[97m"
    echo -e "\e[48;5;16m"
    clear
    }

PUT(){ echo -en "\033[${1};${2}H";}
HIDECURSOR(){ echo -en "\033[?25l";}
SHOWCURSOR(){ echo -en "\033[?25h";}


sleep 0.5
clearterm
SHOWCURSOR

if [ $# -eq 0 ];
  then DOINSTALL="server"
  else DOINSTALL="$1"
fi

INITPWD=$(pwd)


PUT 1 0
echo "You're about to install the ground segment of PicSat."
echo "You will install:"
if [ "$DOINSTALL" == "all" -o "$DOINSTALL" == "server" ]; then
    echo "- the python repositories, libraries and scripts"
fi
if [ "$DOINSTALL" == "all" -o "$DOINSTALL" == "desk" ]; then
    echo "- the desktop shortcuts"
fi
if [ "$DOINSTALL" == "all" -o "$DOINSTALL" == "bdd" ]; then
    echo "- the local database"
fi


read -t 0.2 -n 10000 discard
PUT 8 0


############################################


if [ "$DOINSTALL" == "all" -o "$DOINSTALL" == "server" ]; then

    echo -n "Do you wish to install a separate python environment? [y|N] "
    read -r -n 1 newpython
    echo ""
    if [ "$newpython" == "Y" ] || [ "$newpython" == "y" ]; then
	sudo apt-get install python-dev python-pip
	pip install virtualenv
	mkdir -p $WHEREPYENV
	cd $WHEREPYENV
	virtualenv -p /usr/bin/python2.7 venv
	source venv/bin/activate
	pip install ipython psycopg2 SQLAlchemy inflect pyserial byt hein pytz python-dateutil
	pip install --upgrade ipython psycopg2 SQLAlchemy inflect pyserial byt hein pytz python-dateutil
	IPY="$WHEREPYENV/venv/bin/ipython"
	sleep 0.5
	clearterm
	SHOWCURSOR
	echo "Do you wish to use this new python environment as default? [y|N] "
	read -r -n 1 prepend
    else
	# install and/or update python dependencies
	pip install ipython psycopg2 SQLAlchemy inflect pyserial byt hein pytz python-dateutil
	pip install --upgrade ipython psycopg2 SQLAlchemy inflect pyserial byt hein pytz python-dateutil
	IPY=$(which ipython)
    fi
    
    # create directories
    mkdir -p $WHERESEGSOL
    mkdir -p $WHEREPARAM
    mkdir -p $WHEREDATA
    mkdir -p $WHEREBINS
    mkdir -p $WHERESCRIPTS
    mkdir -p $WHEREBDD
    mkdir -p "$HOME/seglog"

    # generate private/public key if not existing
    if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
        ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N ""
    fi

    # git user initialization
    if [ ! -f $HOME/.gitconfig ]; then
        git config --global user.name "segsol"
        git config --global user.email "picsat.office@obspm.fr"
    fi

    # update paths
    echo '' >> $HOME/.bashrc
    echo '' >> $HOME/.bashrc
    echo '# segsol append' >> $HOME/.bashrc
    if [ "$prepend" == "Y" ] || [ "$prepend" == "y" ]; then
        echo "export PATH=$WHEREPYENV/venv/bin:"'$PATH' >> $HOME/.bashrc
    fi
    echo "export PATH=$WHEREBINS:"'$PATH' >> $HOME/.bashrc
    echo "export PYTHONPATH=$WHERESEGSOL:$WHERESCRIPTS"':$PYTHONPATH' >> $HOME/.bashrc

    read -t 0.2 -n 10000 discard
    echo ""
    echo ""
    echo "Before continuing, you will need to copy your public key shown below to the authorized keys of the user 'picsatdata' on gitlab.obspm.fr"
    echo "***"
    cat $HOME/.ssh/id_rsa.pub
    echo "***"
    echo "Press ENTER when done or ctrl-C to abort"
    read -r discard

    sleep 0.5
    clearterm
    SHOWCURSOR

    cd $WHERESEGSOL

    # init the git repo for segsol
    git init
    git remote add origin git@gitlab.obspm.fr:picsat/segsol.git

    # grab code
    git pull origin master

    # make the copy of param_all to replicate parameters
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

    cd $WHERESCRIPTS
    # init the git repo for scripts
    git init
    git remote add origin git@gitlab.obspm.fr:picsat/scripts.git

    # grab code
    git pull origin master


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

    echo "    xterm -T 'Spy' $BASICFONT -geometry 80x10+30-50 -e '$IPY -i $WHERESEGSOL/spy.py';" >> picspy
    echo "else" >> picspy
    echo "    $IPY -i $WHERESEGSOL/spy.py" >> picspy
    echo "fi" >> picspy    

    echo "xterm -T 'Chat' $BASICFONT -geometry 80x15-0+0 -e /bin/bash -l -c '$WHEREBINS/logdisp';" >> picchat
fi


############################################


if [ "$DOINSTALL" == "all" -o "$DOINSTALL" == "bdd" ]; then

    echo "Installing local BDD. Need first to install postgresql binaries"
    sudo apt-get install postgresql postgresql-client postgresql-contrib libpq-dev pgadmin3

    sudo -u postgres psql postgres -c "alter user postgres with password 'postgres';"

    sudo service postgresql restart

    cd $WHEREBDD
    # init the git repo for bdd init
    git init
    git remote add origin git@gitlab.obspm.fr:picsat/bdd.git

    # grab code
    git pull origin master

    # refresh db_server parameters to match the default local database
    echo 'postgresql://postgres:<pass>@localhost:5432/picsat' > $WHEREPARAM/db_server

    bash new_database.sh picsat
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
    cp PicControl.desktop PicSpy.desktop

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
