#!/bin/bash

if [ $# -eq 0 ];
  then
    echo "You have to give an input parameter, being the name of the database to create"
  else
    sudo -u postgres psql postgres -c "CREATE DATABASE $1;"
    sudo -u postgres psql -d $1 -a -f init_telecommand_db.postgres
fi


