#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  CTRL - Ground-Segment software for Cube-Sats
#  Copyright (C) 2016-2017  Guillaume Schworer
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  For any information, bug report, idea, donation, hug, beer, please contact
#    guillaume.schworer@gmail.com
#
###############################################################################


import time
import os
import hein
import paramiko
from byt import Byt
from nanoutils import core
from nanoutils import ctrlexception
from nanoparam import param_all_processed as param_all
from nanoutils.report import REPORTS
from nanoctrl.telemetry import Telemetry
from nanoctrl.ccsds import CCSDSBlob
from nanoctrl.kiss import Framer


__all__ = ['init', 'close', 'report']



SAVE_TRANS = None
SAVE_REC_LISTEN = None
running = False
SERVER = [None, None]


class SaveTrans(hein.SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection is extablished
        """
        report('newTransConnection', rec=name)
        report('myPID', pid=core.get_pid())


class SaveRec(hein.SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        report('newRecConnection', port=self.portname)
        report('myPID', pid=core.get_pid())

    def process(self, key, data):
        """
        Saves the packet in the database and does 
        """
        # ignores the reporting
        if key == 'rpt':
            return
        report('receivedTM')
        if param_all.AX25ENCAPS:
            source, destination, blobish = Framer.decode_radio(data['data'])
            if len(source) > 0:
                report('receivedCallsignTM', source=source, ll=len(blobish),
                            destination=destination)
            else:
                report('junkFromRF')
        else:
            blobish = data['data']
            report('receivedRawTM', ll=len(blobish))
        blobparser = CCSDSBlob(blobish)
        start = 0
        pk = blobparser.grab_first_packet(start=start)
        while pk is not None:
            data['data'] = Byt(pk)
            process_incoming(**data)
            start += len(pk)
            pk = blobparser.grab_first_packet(start=start)
        return


def moveto_save_folder(sftp, t=None):
    """
    Given the sftp object, cd to the save folder after
    creating it if it didn't exist.

    Args:
      * t (datetime): if None, goes to the user_id save folder,
        otherwise to the user_id/YYYYMMDD save folder
    """
    path = param_all.TELEMETRYSAVEFOLDER.rstrip('/')\
                    .format(user_id=param_all.RECEIVERID)
    if t is None:
        path = path[:path.rfind('/')]  # server is linux
    else:
        path = t.strftime(path)
    try:
        sftp.chdir(path)  # Test if remote_path exists
    except IOError:
        sftp.mkdir(path)  # Create remote path
        sftp.chdir(path)  # cd there
    return sftp


def process_incoming(t, path, data, **kwargs):
    """
    A callback function that saves the package in the database after
    parsing it
    """
    global SERVER
    path = str(path)
    if not os.path.isfile(path):
        raise ctrlexception.PacketFileMissing(path)
    #f = open(path, mode='rb')
    #dd = Byt(f.read())
    #f.close()
    #if not dd == data:
    #    raise ctrlexception.PacketMismatch(path)
    t = core.strISOstamp2datetime(t)
    if not t == core.packetfilename2datetime(path):
        raise ctrlexception.PacketDateMismatch(path)
    # create tmp file to indicate on-going copy and saving
    open(path+'.tmp', 'w').close()
    # copy raw file to server
    if param_all.SAVERAWFILE:
        # determine folderw ith date, creates it if missing and goes into it
        SERVER[1] = moveto_save_folder(sftp=SERVER[1], t=t)
        SERVER[1].put(path, '.')
    # save TM to DB
    tm = Telemetry._fromPacket(data, time_received=t)
    # remove temp file after copy and DB saving successful
    os.remove(path+'.tmp')
    if param_all.REMOVERAWFILEAFTERSAVE:
        os.remove(path)
    ###report('savedTM', dbid=tm.id)


def report(*args, **kwargs):
    """
    Reports to watchdog
    """
    key = str(args[0])
    rp = REPORTS[key].pack(who=param_all.SAVINGNAME, **kwargs)
    SAVE_TRANS.tell_report(**rp)


def init():
    """
    Initializes the saving procedure
    """
    global SAVE_TRANS
    global SAVE_REC_LISTEN
    global running
    global SERVER
    if running:
        return
    SAVE_TRANS = SaveTrans(port=param_all.SAVINGPORT[0],
                            nreceivermax=len(param_all.SAVINGPORTLISTENERS),
                            start=True, portname=param_all.SAVINGPORT[1])
    SAVE_REC_LISTEN = SaveRec(port=param_all.LISTENINGPORT[0],
                                name=param_all.SAVINGNAME, connect=True,
                                connectWait=0.5,
                                portname=param_all.LISTENINGPORT[1])
    if param_all.SAVERAWFILE:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser( os.path.join("~", ".ssh",
                                                            "known_hosts")))
        ssh.connect(param_all.TELEMETRYSAVESERVER,
                    username=param_all.TELEMETRYSAVEUSER,
                    password=param_all.TELEMETRYSAVEPASS)
        sftp = ssh.open_sftp()
        # creates the root user-folder if missing and moves into it
        sftp = moveto_save_folder(sftp=sftp)
        SERVER = [ssh, sftp]
    running = True


def close():
    """
    Closes the saving procedure
    """
    global SAVE_TRANS
    global SAVE_REC_LISTEN
    global running
    global SERVER
    if not running:
        return
    running = False
    if param_all.SAVERAWFILE:
        SERVER[0].close()
        SERVER[1].close()
    SAVE_TRANS.close()
    SAVE_REC_LISTEN.stop_connectLoop()
    SAVE_REC_LISTEN.close()
    SAVE_TRANS = None
    SAVE_REC_LISTEN = None
