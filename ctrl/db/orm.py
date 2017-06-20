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
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import update
from sqlalchemy import and_
#from sqlalchemy import or_
from param import param_category
from param import param_category_common as pcc
from param import param_apid
from byt import Byt
from ..utils import core
from ..utils import ctrlexception
from ..ccsds import param_ccsds


__all__ = ['init_DB', 'get_column_keys', 'save_TC_to_DB', 'close_DB',
            'save_TM_to_DB', 'update_sent_TC_time', 'get_TC_dbid_from_pkid',
            'get_TC', 'get_RACK_TCid', 'get_TM_dbid_from_pkid', 'get_TM',
            'get_ACK_TCid', 'get_TMid_answer_from_TC', 'get_tcanswer_TCid']


running = False
DB = None
TABLES = {}


def init_DB():
    """
    Opens the database connection
    """
    global running
    global DB
    global TABLES
    if running:
        return
    Base = automap_base()
    engine = create_engine(core.DBENGINE)
    Base.prepare(engine, reflect=True)
    TABLES = {}
    for k in Base.classes.keys():
        nk = core.camelize_singular(k)
        if nk is False:
            print("The table '{}' was given a name without plurals. "\
                  "This is wrong and it will probably crash".format(k))
        TABLES[nk] = Base.classes[k]
        globals()[nk] = Base.classes[k]
    DB = Session(engine)
    running = True


def close_DB():
    """
    Opens the database connection
    """
    global running
    DB.close()
    running = False


def get_column_keys(tbl):
    """
    Returns the column names of the table ``tbl``
    """
    return tbl.__table__.columns.keys()


def save_TC_to_DB(hd, hdx, inputs):
    """
    Saves the TC values (header) and inputs (data)
    to the database

    Args:
      * hd (dict): the keys-values of the CCSDS prim/sec headers
      * hdx (dict): the keys-values of the CCSDS auxiliary header
      * inputs (dict): the keys-values of the input parameters (CCSDS data)
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    hd.pop('signature', '')
    TC = TABLES['Telecommand'](**hd)
    DB.add(TC)
    DB.flush()
    for k, v in inputs.items():
        DB.add(TABLES['TelecommandDatum'](telecommand_id=TC.id,
                                          param_key=k, 
                                          value=repr(v)))
    DB.commit()
    return TC.id


def update_sent_TC_time(pkid, t):
    """
    Updates the time_sent column in telecommands once the
    TC has been sent
    Returns the id of the updated TC

    Args:
      * pkid (int): the packet counter id
      * t (datetime): the sent time
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    t = str(t)
    TC = TABLES['Telecommand']
    idx = DB.query(TC.id)\
            .filter(getattr(TC, param_ccsds.PACKETID.name) == int(pkid))\
            .order_by(TC.time_sent.desc()).limit(1).first()
    if idx is None:
        return
    q = DB.query(TC).filter(TC.id == idx[0]).update({'time_sent': t})
    DB.commit()
    return idx[0]


def get_TC_dbid_from_pkid(pkid):
    """
    Gives list of (id, timestamp) where id is the database id and
    timestamp is the time_sent

    Args:
      * pkid (int): the packet counter id to investigate
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    res = DB.query(TC)\
            .filter(getattr(TC, param_ccsds.PACKETID.name) == int(pkid))\
            .order_by(TC.time_sent.desc())
    return [(item.id, item.time_sent) for item in res]


def get_TM_dbid_from_pkid(pkid):
    """
    Gives list of (id, timestamp) where id is the database id and
    timestamp is the time_sent

    Args:
      * pkid (int): the packet counter id to investigate
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TM = TABLES['Telemetry']
    res = DB.query(TM)\
            .filter(getattr(TM, param_ccsds.PACKETID.name) == int(pkid))\
            .order_by(TM.time_sent.desc())
    return [(item.id, item.time_sent) for item in res]


def get_TC(pkid=None, dbid=None):
    """
    Gives a full TC object

    Args:
      * pkid (int): the packet counter id of the TC to output
      * dbid (int) [alternative]: the DB id of the TC to output

    Returns:
      * (thetc, dictc): the TC as sqlalchemy object and the values
        as dict object
      * params: the input parameters of the TC
      * (rackid, fackid, eackid): the ids of the rack, fack and eack, 
        or None
      * ansid: the id of the answer if the telemetry generate is of
        tcanswer category, or None
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    thetc = DB.query(TC)
    if dbid is None:
        thetc = thetc.filter(
                    getattr(TC, param_ccsds.PACKETID.name) == int(pkid))
    else:
        thetc = thetc.filter(TC.id == int(dbid))
    thetc = thetc.order_by(TC.time_sent.desc()).limit(1).first()
    if thetc is None:
        return None
    dictc = {}
    for key in get_column_keys(TC):
        dictc[key] = getattr(thetc, key, None)
    params = {}
    for item in thetc.telecommand_data_collection:
        # unicode to str for the key, eval on the value
        params[str(item.param_key)] = eval(item.value)
    # get the DB id of the ACK
    if len(getattr(thetc, 'tmcat_rec_acknowledgements_collection', [])) > 0:
        rackid = thetc.tmcat_rec_acknowledgements_collection[0]\
                                                    .telemetry_packet
    else:
        # nothing received, set to None
        rackid = None
    if len(getattr(thetc, 'tmcat_fmt_acknowledgements_collection', [])) > 0:
        fackid = thetc.tmcat_fmt_acknowledgements_collection[0]\
                                                    .telemetry_packet
    else:
        # nothing received, set to None
        fackid = None
    if len(getattr(thetc, 'tmcat_exe_acknowledgements_collection', [])) > 0:
        eackid = thetc.tmcat_exe_acknowledgements_collection[0]\
                                                    .telemetry_packet
    else:
        # nothing received, set to None
        eackid = None
    # get the DB id of the Answer
    # basic tcanswer category
    if len(getattr(thetc, 'tmcat_tc_answers_collection', [])) > 0:
        ansid = thetc.tmcat_tc_answers_collection[0].telemetry_packet
    else:
        pkid = getattr(thetc, param_ccsds.PACKETID.name)
        cid = getattr(thetc, param_ccsds.TELECOMMANDID.name)
        ansid = get_TMid_answer_from_TC(cid=cid, pkid=pkid)
        # nothing received, set to None
    return (thetc, dictc), params, (rackid, fackid, eackid), ansid


def get_TM(pkid=None, dbid=None):
    """
    Gives a full TM object

    Args:
      * pkid (int): the packet counter id of the TM to output (will only
        return the most recent one)
      * dbid (int) [alternative]: the DB id of the TM to output
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TM = TABLES['Telemetry']
    thetm = DB.query(TM)
    if dbid is None:
        thetm = thetm.filter(
                    getattr(TM, param_ccsds.PACKETID.name) == int(pkid))
    else:
        thetm = thetm.filter(TM.id == int(dbid))
    thetm = thetm.order_by(TM.time_sent.desc()).limit(1).first()
    DB.commit()
    if thetm is None:
        return None
    dictm = {}
    for key in get_column_keys(TM):
        dictm[key] = getattr(thetm, key, None)
    # grab pld flag and category
    catnum = int(dictm[param_ccsds.PACKETCATEGORY.name])
    pldflag = int(dictm[param_ccsds.PAYLOADFLAG.name])
    # deal with header aux
    # table name for hdx
    cat = param_category.CATEGORIES[pldflag][catnum]
    dichdx = {}
    if cat.object_aux_name is None:
        thehdx = None
    else:
        TMHDX = TABLES[cat.object_aux_name]
        thehdx = getattr(thetm, cat.table_aux_name + '_collection', [])
        if len(thehdx) > 0:
            # there can be only one
            thehdx = thehdx[0]
            for key in get_column_keys(TMHDX):
                dichdx[key] = getattr(thehdx, key, None)
        else:
            thehdx = None
    # deal with data
    # table name for data
    dicdata = []
    if cat.object_data_name is None:
        thedata = None
    else:
        TMDATA = TABLES[cat.object_data_name]
        thedata = getattr(thetm, cat.table_data_name + '_collection', [])
        if len(thedata) > 0:
            for dataline in thedata:
                thedicline = {}
                for key in get_column_keys(TMDATA):
                    thedicline[key] = getattr(dataline, key, None)
                dicdata.append(thedicline)
        else:
            thedata = None
    return (thetm, dictm), (thehdx, dichdx), (thedata, dicdata)


def save_TM_to_DB(hd, hdx, data):
    """
    Saves the TM headers and data to the database

    Args:
      * hd (dict): the keys-values of the CCSDS headers (prim and sec)
      * hdx (dict): the keys-values of the CCSDS auxiliary header
      * data (dict): the keys-values of the input parameters (CCSDS data)
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    DB.commit()
    # save prim and sec headers
    # forced field
    hd['time_sent'] = core.stamps2time(hd['days_since_ref'],
                                        hd['ms_since_today'])
    # force default to now
    hd['time_saved'] = core.now()
    TM = TABLES['Telemetry'](**hd)
    DB.add(TM)
    DB.commit()
    catnum = int(hd[param_ccsds.PACKETCATEGORY.name])
    pldflag = int(hd[param_ccsds.PAYLOADFLAG.name])
    # saving the aux header
    cat = param_category.CATEGORIES[pldflag][catnum]
    if cat.object_aux_name is not None:
        hdx = dict(hdx)
        hdx['telemetry_packet'] = TM.id
        DB.add(TABLES[cat.object_aux_name](**hdx))
        DB.commit()
    # saving the data
    tbl = cat.object_data_name
    if tbl is not None:
        # if saving the data from TC answer
        if catnum == param_category.TELECOMMANDANSWERCAT:
            for k, v in data['unpacked'].items():
                DB.add(TABLES[tbl](telemetry_packet=TM.id,
                                   param_key=k,
                                   value=v))
        # if dealing with list of dict, e.g. science or payload hk
        elif isinstance(data['unpacked'], (list, tuple)):
            for item in data['unpacked']:
                item = dict(item)
                item['telemetry_packet'] = TM.id
                DB.add(TABLES[tbl](**item))
        # standard case
        else:
            dt = dict(data['unpacked'])
            dt['telemetry_packet'] = TM.id
            DB.add(TABLES[tbl](**dt))
    # save changes
    DB.commit()
    return TM.id


def get_RACK_TCid():
    """
    Returns the DB id of the latest TC sent
    (to which the current RACK TM is supposely acknowledging the receipt)
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    # just grab the latest TC that was actually sent
    idx = DB.query(TC.id)\
            .filter(TC.time_sent != None)\
            .order_by(TC.time_sent.desc()).limit(1).first()
    DB.commit()
    if idx is None:
        return None
    else:
        return idx[0]


def get_ACK_TCid(pkid):
    """
    Gets the TC id to be recorded in a EACK or FACK TM, given the id of
    the latest TC whose packet counter id is provided
    Returns the DB id of the TC

    Args:
      * pkid (int): the packet counter id of the TC to which the FACK
        or EACK is replying
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    # grab the TC that was sent and to which we're replying
    idx = DB.query(TC.id)\
            .filter(getattr(TC, param_ccsds.PACKETID.name) == int(pkid))\
            .order_by(TC.time_sent.desc()).limit(1).first()
    DB.commit()
    # can't find the TC... wasn't saved?
    if idx is None:
        return None
    else:
        return idx[0]


def get_tcanswer_TCid(pkid=None, dbid=None):
    """
    Finds the latest dbid of a tcanswer TM, given a TC id

    Args:
      * pkid (int): the packet counter id of the TC to scan (will only
        return the most recent one)
      * dbid (int) [alternative]: the DB id of the TC to scan
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    thetc = DB.query(TC.id)
    if dbid is None:
        thetc = thetc.filter(getattr(TC, param_ccsds.PACKETID.name) == int(pkid))
    else:
        thetc = thetc.filter(TC.id == int(dbid))
    idx = thetc.order_by(TC.time_sent.desc()).limit(1).first()
    DB.commit()
    # can't find the TC... wasn't saved?
    if idx is None:
        return None
    else:
        return idx[0]


def get_TMid_answer_from_TC(cid=None, pkid=None, dbid=None):
    """
    Finds all the dbid of a TM-answer packet

    Args:
      * cid (int): the command id inside the TC
      * pkid (int): the packet counter id of the TC to scan
      * dbid (int) [alternative]: the DB id of the TC to scan
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    # need command id and packet id for later, so grab it if not given
    if cid is None or pkid is None:
        TC = TABLES['Telecommand']
        thetc = DB.query(TC)
        if dbid is None:
            thetc = thetc.filter(
                        getattr(TC, param_ccsds.PACKETID.name) == int(pkid))
        else:
            thetc = thetc.filter(TC.id == int(dbid))
        thetc = thetc.order_by(TC.time_sent.desc()).limit(1).first()
        # grab info
        pkid = getattr(thetc, param_ccsds.PACKETID.name)
        cid = getattr(thetc, param_ccsds.TELECOMMANDID.name)
        DB.commit()
    # iterate through all known packet categories to scan all SQL tables
    ids = []
    for pldflag in [0, 1]:
        for catnum, cat in param_category.CATEGORIES[pldflag].items():
            # we want answer, not an ack
            if (pldflag, catnum) in param_category.ACKCATEGORIES:
                continue
            # an answer must have an aux header to identify the TC
            if cat.aux_trousseau is None:
                continue
            # patch to allow partly designed DB and avoid error
            if cat.object_aux_name not in TABLES.keys():
                continue
            TMAUX = TABLES[cat.object_aux_name]
            cols = get_column_keys(TMAUX)
            # can only be answer if there is packet id mirror + tc id mirror
            if pcc.PACKETIDMIRROR.name not in cols or\
                    pcc.TELECOMMANDIDMIRROR.name not in cols:
                continue
            res = DB.query(TMAUX.telemetry_packet)\
                    .filter(getattr(TMAUX,
                                    param_ccsds.PACKETIDMIRROR.name)\
                                == int(pkid))\
                    .filter(getattr(TMAUX,
                                    param_ccsds.TELECOMMANDIDMIRROR.name)\
                                == int(cid))\
                    .order_by(TMAUX.id.desc())
            ids += [item[0] for item in res.all()]
            DB.commit()
    return ids
