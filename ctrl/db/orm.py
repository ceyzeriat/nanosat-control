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
from sqlalchemy import desc
from sqlalchemy import update
from param import param_category
from param import param_apid
from byt import Byt
from ..utils import core
from ..utils import ctrlexception
from ..ccsds import param_ccsds


__all__ = ['init_DB', 'get_column_keys', 'save_TC_to_DB', 'close_DB',
            'save_TM_to_DB', 'update_sent_TC_time']


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
    t = str(t)
    TC = TABLES['Telecommand']
    idx = DB.query(TC.id).filter_by(packet_id=pkid)\
            .order_by(desc('id')).limit(1).with_for_update()
    q = update(TC).values({'time_sent': t}).where(TC.id == idx.as_scalar())
    DB.execute(q)
    DB.commit()
    DB.flush()
    return idx.first()[0]


def get_TC_dbid_from_pkid(self, pkid):
    """
    Given a packet_id, returns a list of (id, timestamp) where
    id is the database id and timestamp is the time_sent
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    res = DB.query(TABLES['Telecommand']).filter_by(packet_id=int(pkid))\
            .order_by(desc('id'))
    return [(item.id, item.time_sent) for item in res]


def get_TC(self, pkid=None, dbid=None):
    """
    Given a pkid or a dbid, returns a TC
    """
    if not running:
        raise ctrlexception.NoDBConnection()
    TC = TABLES['Telecommand']
    res = DB.query(TC)
    if dbid is not None:
        res = res.filter_by(id=int(dbid))
    else:
        res = res.filter_by(packet_id=int(pkid))
    res = res.order_by(desc('id')).limit(1).first()
    if res is None:
        return None
    ret = {}
    for key in get_column_keys(TC):
        ret[key] = getattr(res, key, None)
    params = {}
    for item in res.telecommand_data_collection:
        thevalue = str(Byt(item.value))
        try:
            thevalue = eval(thevalue)
        except:
            pass
        params[str(Byt(item.param_key))] = thevalue
    return ret, params


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


def get_ack_TC(timestamp):
    """
    returns the DB id of the TC of which the input telemetry packet
    is the acknowledgement
    """
    
    ack_rec_id = getattr(
                    db.query(Telecommand)\
                        .filter_by(and_(
                                Telecommand.pid==param_apid.RECACKPACKETPID,
                                Telecommand.ack_reception_id==None,
                                #Telecommand.reqack_reception==1,
                                Telecommand.time_sent<=timestamp))\
                        .order_by(desc(Telecommand.time_sent))\
                        .limit(1),
                    'id', None)
    ack_fmt_id = None
