#!/bin/bash


REPONAME="segsol"
SCRIPTNAME="scripts"
DOCS=$(xdg-user-dir DOCUMENTS)
DESKTOP=$(xdg-user-dir DESKTOP)
WHERESEGSOL="$DOCS/lib/$REPONAME"
WHEREBDD="$DOCS/lib/bdd"
WHERESCRIPTS="$DOCS/$SCRIPTNAME"
WHEREBINS="$DOCS/bin"
WHEREPARAM="$HOME/.nanoctrl"
WHEREDATA="$HOME/nanoctrl/tm_data"
WHEREPYENV="$HOME/pynanoctrl"


######################################################


DOC="Use -s to install the libraries and scripts, -d to install the desktop shortcuts, -b to install the local database, -a to install all"

if [[ $# -eq 0 ]] ; then
    echo $DOC
    exit 0
fi

# Reset in case getopts has been used previously in the shell.
OPTIND=1

# Initialize our own variables:
output_file=""
dobdd=0
doserver=0
dodesk=0

# parses the input commands
while getopts ":h?bsda" opt; do
    case "$opt" in
    h|\?)
        echo $DOC
        exit 0
        ;;
    b)  dobdd=1
        ;;
    s)  doserver=1
        ;;
    d)  dodesk=1
        ;;
    a)  dodesk=1
        dobdd=1
        doserver=1
        ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift


function clearterm {
    echo -e "\\033c"
    echo -e "\e[97m"
    echo -e "\e[48;5;16m"
    clear
    }

HIDECURSOR(){ echo -en "\033[?25l";}
SHOWCURSOR(){ echo -en "\033[?25h";}


sleep 0.5
clearterm
SHOWCURSOR


INITPWD=$(pwd)


echo "You're about to install the ground segment of PicSat."
echo "You will install:"
if [ "$doserver" ==  1  ]; then
    echo "- the python repositories, libraries and scripts"
fi
if [ "$dodesk" ==  1  ]; then
    echo "- the desktop shortcuts"
fi
if [ "$dobdd" ==  1  ]; then
    echo "- the local database"
fi


read -t 0.2 -n 10000 discard

echo ""
echo -n "Proceed? [y|N] "
read -r -n 1 newpython
if [ "$newpython" == "Y" ] || [ "$newpython" == "y" ]; then
    echo ""
else
    echo ""
    exit 0
fi

############################################

ALLPYTHONLIBS="ipython psycopg2 SQLAlchemy inflect pyserial byt hein pytz python-dateutil patiencebar paramiko pylatex"

if [ "$doserver" ==  1  ];then
    sleep 0.5
    clearterm
    SHOWCURSOR

    echo -n "Do you wish to install a separate python environment? [y|N] "
    read -r -n 1 newpython
    echo ""
    if [ "$newpython" == "Y" ] || [ "$newpython" == "y" ]; then
	sudo apt-get install python-dev python-pip libffi-dev virtualenv
	pip install virtualenv
	mkdir -p $WHEREPYENV
	cd $WHEREPYENV
	virtualenv -p /usr/bin/python2.7 venv
	source venv/bin/activate
	pip install $ALLPYTHONLIBS
	pip install --upgrade $ALLPYTHONLIBS
	IPY="$WHEREPYENV/venv/bin/ipython"
	sleep 0.5
	clearterm
	SHOWCURSOR
	echo "Do you wish to use this new python environment as default? [y|N] "
	read -r -n 1 prepend
    else
	# install and/or update python dependencies
	pip install $ALLPYTHONLIBS
	pip install --upgrade $ALLPYTHONLIBS
	IPY=$(which ipython)
    fi
    
    echo "Create directories"
    mkdir -p $WHERESEGSOL
    mkdir -p $WHEREPARAM
    mkdir -p $WHEREDATA
    mkdir -p $WHEREBINS
    mkdir -p $WHERESCRIPTS
    mkdir -p $WHEREBDD
    mkdir -p "$HOME/seglog"

    # generate private/public key if not existing
    if [ ! -f $HOME/.ssh/id_rsa.pub ]; then
        echo "Generate private/public key"
        ssh-keygen -b 2048 -t rsa -f $HOME/.ssh/id_rsa -q -N ""
    fi

    # git user initialization
    if [ ! -f $HOME/.gitconfig ]; then
        echo "Git user initialization"
        git config --global user.name "nanoctrl"
        git config --global user.email "picsat.office@obspm.fr"
    fi

    # update paths
    echo "Update paths"
    echo '' >> $HOME/.bashrc
    echo '' >> $HOME/.bashrc
    echo '# nanoctrl append' >> $HOME/.bashrc
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

    echo "Init the git repo for libraries"
    git init
    git remote add origin git@gitlab.obspm.fr:picsat/segsol.git

    # grab code
    git pull origin master

    # make the copy of param_all to replicate parameters
    cp ./param/param_all_example.py ./param/param_all.py


    #echo "Move logging binaries"
    #chmod a+x bins/log*
    #cp bins/log* $WHEREBINS/


    echo "Compiling hmac library"
    cd $WHERESEGSOL/nanoctrl/utils/hmac/
    gcc -shared -o hmaclib.so -fPIC L0AppHmac.c L0AppSha256.c
    

    echo "Create parameter files"
    echo 'PICSAT' > $WHEREPARAM/callsign_destination
    echo 'ground' > $WHEREPARAM/callsign_source
    echo '0' > $WHEREPARAM/tc_packet_id
    echo 'postgresql://postgres:<pass>@localhost:5432/picsat' > $WHEREPARAM/db_server
    echo 'postgres' > $WHEREPARAM/artichaut
    echo 'You wish!' > $WHEREPARAM/perefouras
    echo '' > $WHEREPARAM/godsavesthequeen

    cd $WHERESCRIPTS
    echo "Init the git repo for scripts"
    git init
    git remote add origin git@gitlab.obspm.fr:picsat/scripts.git

    # grab code
    git pull origin master


    # create the binaries
    echo "Generate binaries"
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

    echo "    xterm -T 'Control' $BASICFONT -geometry 80x24-0+200 -e 'source $HOME/.bashrc;$IPY -i $WHERESEGSOL/control.py';" >> piccontrol
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

    echo ""
    echo "Done"
fi


############################################


if [ "$dobdd" ==  1  ];then
    sleep 0.5
    clearterm
    SHOWCURSOR

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
    echo ""
    echo "Done"
fi


############################################


if [ "$dodesk" ==  1  ];then
    sleep 0.5
    clearterm
    SHOWCURSOR

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
    echo 'Icon='"$WHERESEGSOL"'/img/control.ico' >> PicControl.desktop
    echo 'Path='"$HOME" >> PicControl.desktop
    echo 'Terminal=false' >> PicControl.desktop
    echo 'StartupNotify=false' >> PicControl.desktop

    echo 'Name=PicListen' >> PicListen.desktop
    echo 'Comment=' >> PicListen.desktop
    echo 'Exec='"$WHEREBINS"'/piclisten gui' >> PicListen.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/listen.ico' >> PicListen.desktop
    echo 'Path='"$HOME" >> PicListen.desktop
    echo 'Terminal=false' >> PicListen.desktop
    echo 'StartupNotify=false' >> PicListen.desktop

    echo 'Name=PicSave' >> PicSave.desktop
    echo 'Comment=' >> PicSave.desktop
    echo 'Exec='"$WHEREBINS"'/picsave gui' >> PicSave.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/save.ico' >> PicSave.desktop
    echo 'Path='"$HOME" >> PicSave.desktop
    echo 'Terminal=false' >> PicSave.desktop
    echo 'StartupNotify=false' >> PicSave.desktop

    echo 'Name=PicWatch' >> PicWatch.desktop
    echo 'Comment=' >> PicWatch.desktop
    echo 'Exec='"$WHEREBINS"'/picwatch gui' >> PicWatch.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/watch.ico' >> PicWatch.desktop
    echo 'Path='"$HOME" >> PicWatch.desktop
    echo 'Terminal=false' >> PicWatch.desktop
    echo 'StartupNotify=false' >> PicWatch.desktop

    echo 'Name=PicShow' >> PicShow.desktop
    echo 'Comment=' >> PicShow.desktop
    echo 'Exec='"$WHEREBINS"'/picshow gui' >> PicShow.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/show.ico' >> PicShow.desktop
    echo 'Path='"$HOME" >> PicShow.desktop
    echo 'Terminal=false' >> PicShow.desktop
    echo 'StartupNotify=false' >> PicShow.desktop

    echo 'Name=PicSpy' >> PicSpy.desktop
    echo 'Comment=' >> PicSpy.desktop
    echo 'Exec='"$WHEREBINS"'/picspy gui' >> PicSpy.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/spy.ico' >> PicSpy.desktop
    echo 'Path='"$HOME" >> PicSpy.desktop
    echo 'Terminal=false' >> PicSpy.desktop
    echo 'StartupNotify=false' >> PicSpy.desktop    

    echo 'Name=PicChat' >> PicChat.desktop
    echo 'Comment=' >> PicChat.desktop
    echo 'Exec='"$WHEREBINS"'/picchat' >> PicChat.desktop
    echo 'Icon='"$WHERESEGSOL"'/img/chat.ico' >> PicChat.desktop
    echo 'Path='"$HOME" >> PicChat.desktop
    echo 'Terminal=false' >> PicChat.desktop
    echo 'StartupNotify=false' >> PicChat.desktop

    echo ""
    echo "Done"
fi

# got back where we were
cd "$INITPWD"

echo "You're good to go"
