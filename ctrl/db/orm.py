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


from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import update
from param import param_category
from param import param_apid
from byt import Byt
from ..utils import core
from ..utils import ctrlexception
from ..ccsds import param_ccsds


__all__ = ['init_DB', 'get_column_keys', 'save_TC_to_DB', 'close_DB',
            'save_TM_to_DB', 'update_sent_TC_time', 'get_TC_dbid_from_pkid',
            'get_TC', 'update_RACK_id', 'get_TM_dbid_from_pkid', 'get_TM']


running = False
DB = None
TABLES = {}
TABLENAMES_REV = {}


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
        TABLENAMES_REV[nk] = k
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
      * pkid (int): the packet_id
      * t (datetime): the sent time
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    t = str(t)
    TC = TABLES['Telecommand']
    idx = DB.query(TC.id).filter(TC.packet_id == int(pkid))\
            .order_by(TC.id.desc()).limit(1).with_for_update()
    q = update(TC).values({'time_sent': t}).where(TC.id == idx.as_scalar())
    DB.execute(q)
    DB.commit()
    DB.flush()
    return idx.first()[0]


def get_TC_dbid_from_pkid(pkid):
    """
    Gives list of (id, timestamp) where id is the database id and
    timestamp is the time_sent

    Args:
      * pkid (int): the packet_id to investigate
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    res = DB.query(TC).filter(TC.packet_id == int(pkid))\
            .order_by(TC.id.desc())
    return [(item.id, item.time_sent) for item in res]


def get_TM_dbid_from_pkid(pkid):
    """
    Gives list of (id, timestamp) where id is the database id and
    timestamp is the time_sent

    Args:
      * pkid (int): the packet_id to investigate
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TM = TABLES['Telemetry']
    res = DB.query(TM).filter(TM.packet_id == int(pkid))\
            .order_by(TM.id.desc())
    return [(item.id, item.time_sent) for item in res]


def get_TC(pkid=None, dbid=None):
    """
    Gives a full TC object

    Args:
      * pkid (int): the packet_id of the TC to output
      * dbid (int) [alternative]: the DB id of the TC to output
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    thetc = DB.query(TC)
    if dbid is None:
        thetc = thetc.filter(TC.packet_id == int(pkid))
    else:
        thetc = thetc.filter(TC.id == int(dbid))
    thetc = thetc.order_by(TC.id.desc()).limit(1).first()
    if thetc is None:
        return None
    sqltc = {}
    for key in get_column_keys(TC):
        sqltc[key] = getattr(thetc, key, None)
    params = {}
    for item in thetc.telecommand_data_collection:
        # unicode to str for the key, eval on the value
        params[str(item.param_key)] = eval(item.value)
    return (thetc, sqltc), params


def get_TM(pkid=None, dbid=None):
    """
    Gives a full TM object

    Args:
      * pkid (int): the packet_id of the TC to output
      * dbid (int) [alternative]: the DB id of the TC to output
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TM = TABLES['Telemetry']
    thetm = DB.query(TM)
    if dbid is None:
        thetm = thetm.filter(TM.packet_id == int(pkid))
    else:
        thetm = thetm.filter(TM.id == int(dbid))
    thetm = thetm.order_by(TM.id.desc()).limit(1).first()
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
    cattbl = param_category.TABLECATEGORY[pldflag][catnum]
    dichdx = {}
    if cattbl is None:
        thehdx = None
    else:
        TMHDX = TABLES[cattbl]
        thehdx = getattr(thetm, TABLENAMES_REV[cattbl] + '_collection', [])
        if len(thehdx) > 0:
            # there can be only one
            thehdx = thehdx[0]
            for key in get_column_keys(TMHDX):
                dichdx[key] = getattr(thehdx, key, None)
        else:
            thehdx = None
    # deal with data
    # table name for data
    datatbl = param_category.TABLEDATA[pldflag][catnum]
    dicdata = []
    if datatbl is None:
        thedata = None
    else:
        TMDATA = TABLES[datatbl]
        thedata = getattr(thetm, TABLENAMES_REV[datatbl] + '_collection', [])
        if len(thedata) == 0:
            for dataline in thedata:
                dicdata.append({})
                for key in get_column_keys(TMDATA):
                    dicdata[key] = getattr(dataline, key, None)
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
    # save prim and sec headers
    # forced field
    hd['time_sent'] = core.stamps2time(hd['days_since_ref'],
                                        hd['ms_since_today'])
    # force default to now
    hd['time_saved'] = core.now()
    TM = TABLES['Telemetry'](**hd)
    DB.add(TM)
    DB.flush()
    catnum = int(hd[param_ccsds.PACKETCATEGORY.name])
    pldflag = int(hd[param_ccsds.PAYLOADFLAG.name])
    # saving the aux header
    tbl = param_category.TABLECATEGORY[pldflag][catnum]
    if tbl is not None:
        hdx = dict(hdx)
        hdx['telemetry_packet'] = TM.id
        DB.add(TABLES[tbl](**hdx))
    # saving the data
    if param_category.TABLEDATA[pldflag][catnum] is not None:
        tbl = param_category.TABLEDATA[pldflag][catnum]
        # if saving the data from TC answer
        if catnum == param_category.TELECOMMANDANSWERCAT:
            for k, v in data['unpacked'].items():
                DB.add(TABLES[tbl](telemetry_packet=TM.id,
                                    param_key=k,
                                    value=v))
        # if dealing with list of dict, i.e. science or payload hk
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


def update_RACK_id(dbid):
    """
    Updates a RACK TM with the id of the latest TC sent
    Returns the DB id of the TC

    Args:
      * dbid (int): the DB id of the RACK TM to update
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    TM = TABLES['Telemetry']
    # just grab the latest TC that was actually sent
    idx = DB.query(TC.id).filter(TC.time_sent != None).\
            order_by(TC.id.desc()).limit(1).with_for_update()
    # 
    q = update(TM).values({'telecommand_id': idx.as_scalar()})\
            .where(TM.id == int(dbid))
    DB.execute(q)
    DB.commit()
    DB.flush()
    return idx.first()[0]


def update_ACK_id(dbid, pkid):
    """
    Updates a EACK or FACK TM with the id of the latest TC whose
    packet_id is provided
    Returns the DB id of the TC

    Args:
      * dbid (int): the DB id of the RACK TM to update
      * pkid (int): the packet_id of the TC to which the FACK or EACK
        is replying
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    TM = TABLES['Telemetry']
    # just grab the latest TC that was actually sent
    idx = DB.query(TC.id).filter(and_(TC.time_sent != None,
                                      TC.packet_id == int(pkid))).\
            order_by(TC.id.desc()).limit(1).with_for_update()
    # 
    q = update(TM).values({'telecommand_id': idx.as_scalar()})\
            .where(TM.id == int(dbid))
    DB.execute(q)
    DB.commit()
    DB.flush()
    return idx.first()[0]
