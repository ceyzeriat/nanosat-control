#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import desc
from ..utils import core
from ..utils import ctrlexception
from ..ccsds import param_category
from ..ccsds import param_ccsds
from ..param import param_apid


__all__ = ['init_DB', 'get_column_keys', 'save_TC_to_DB', 'close_DB',
            'save_TM_to_DB']


running = False
DB = None
TABLES = []


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
    TABLES = []
    for k in Base.classes.keys():
        nk = core.camelize_singular(k)
        TABLES.append(nk)
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
    TC = Telecommand(**hd)
    DB.add(TC)
    DB.flush()
    for k, v in inputs.items():
        DB.add(TelecommandDatum(id=TC.id, param_key=k, value=v))
    DB.commit()
    return TC.id


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
    # force DB default
    hd.pop('time_saved', '')
    TM = Telemetry(**hd)
    DB.add(TM)
    DB.flush()
    # saving the aux header
    tbl = param_category.TABLECATEGORY[hd[param_ccsds.PACKETCATEGORY.name]]
    tbl = globals()[tbl]
    hdx['telemetry_packet'] = TM.id
    DB.add(tbl(**hdx))
    DB.commit()
    # save the data

    return TM.id


def get_ack_TC(timestamp):
    """
    returns the DB id of the TC of which the input telemetry packet
    is the acknowledgement
    """
    
    ack_rec_id = getattr(
                    db.query(Telecommand)\
                        .filter_by(and_(
                                Telecommand.pid==param_apid.PACKETWRAPPERPID,
                                Telecommand.ack_reception_id==None,
                                Telecommand.reqack_reception==1,
                                Telecommand.time_sent<=timestamp))\
                        .order_by(desc(Telecommand.time_sent))\
                        .limit(1),
                    'id', None)
    ack_fmt_id = 