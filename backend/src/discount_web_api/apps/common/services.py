import datetime
import logging

from apps.common.queries import fixedPromos, usergoes
from core.generics.exceptions import (EmptyObjectError,
                                      MissingRequestParamsError, NoDataError)
from core.generics.unit_of_work import AbstractUnitOfWork
from rest_framework import serializers

logger = logging.getLogger(__name__)


def get_languages(uow: AbstractUnitOfWork, uid: int):
    """Return the list of languages

    Parameters
    ----------
    uow
        Unit of work to get the data from the DB.
    uid
        Unique identifier for row if uid > 0. uid < 0 indicates to return all active records

    Returns
    -------
    list
        list of dicts if successful, empty list otherwise.

    """
    resp = {}
    with uow as unit_of_work:
        if uid == -1:
            resp = unit_of_work.repoObj.getAll(active=True)
        elif uid >= 0:
            resp = unit_of_work.repoObj.get(uid)
        else:
            raise MissingRequestParamsError("Not a valid parameter %s" % uid)
    if not resp:
        raise NoDataError("language id %s" % (uid))
    return resp


def add_languages(uow: AbstractUnitOfWork, data: serializers.ModelSerializer):
    """Add to the list of languages

    Parameters
    ----------
    uow
        Unit of work to post the data from the DB.
    data
        Data to insert to the DB.
    Returns
    -------
    string
        successful or failure message.

    """
    with uow as unit_of_work:
        unit_of_work.repoObj.add(data.data)
        unit_of_work.commit()


def update_languages(
    uow: AbstractUnitOfWork, uid: int, data: serializers.ModelSerializer
):
    """Update a lnaguage in the list of languages

    Parameters
    ----------
    uow
        Unit of work to get the data from the DB.
    uid
        Unique identifier for the row.
    data
        Data to update to the DB.
    Returns
    -------
    string
        successful or failure message.

    """
    with uow as unit_of_work:
        unit_of_work.repoObj.update(uid, data.initial_data)
        unit_of_work.commit()


def delete_languages(uow: AbstractUnitOfWork, uid: int):
    """Return the list of languages

    Parameters
    ----------
    uow
        Unit of work to get the data from the DB.
    uid
        Unique identifier for the row.
    Returns
    -------
    string
        successful or failure message.

    """
    with uow as unit_of_work:
        unit_of_work.repoObj.delete(uid)
        unit_of_work.commit()


def get_Items(uow: AbstractUnitOfWork, uid: int):
    """Return the list of rows from a model

    Parameters
    ----------
    uow
        Unit of work to get the data from the DB.
    uid
        Unique identifier for row if uid > 0. uid < 0 indicates to return all active records
    Returns
    -------
    list
        list of dicts if successful, empty list otherwise.

    """
    resp = {}
    with uow as unit_of_work:
        if uid == -1:
            resp = unit_of_work.repoObj.getAll(active=True)
            uid = "all"
        elif uid >= 0:
            resp = unit_of_work.repoObj.get(uid)
        else:
            raise MissingRequestParamsError("Not a valid parameter %s" % uid)
    if not resp:
        raise NoDataError("id %s" % (uid))
    return resp

def post_Items(uow: AbstractUnitOfWork, data: serializers.ModelSerializer):
    """Add to the list of items

    Parameters
    ----------
    uow
        Unit of work to post the data from the DB.
    data
        Data to insert to the DB.
    Returns
    -------
    string
        successful or failure message.

    """
    
    with uow as unit_of_work:
        unit_of_work.repoObj.add(data.data)
        unit_of_work.commit()

def update_items(
    uow: AbstractUnitOfWork, uid: int, data: serializers.ModelSerializer
):
    """Update item in the list of items

    Parameters
    ----------
    uow
        Unit of work to get the data from the DB.
    uid
        Unique identifier for the row.
    data
        Data to update to the DB.
    Returns
    -------
    string
        successful or failure message.

    """
    with uow as unit_of_work:
        unit_of_work.repoObj.update(uid, data.initial_data)
        unit_of_work.commit()


def delete_items(uow: AbstractUnitOfWork, uid: int):
    """Return the list of items

    Parameters
    ----------
    uow
        Unit of work to get the data from the DB.
    uid
        Unique identifier for the row.
    Returns
    -------
    string
        successful or failure message.

    """
    with uow as unit_of_work:
        unit_of_work.repoObj.delete(uid)
        unit_of_work.commit()

def get_promotypes(uow: AbstractUnitOfWork, uid: int):
    """Return the list of rows from a model

    Parameters
    ----------
    uow
        Unit of work to get the data from the DB.
    uid
        Unique identifier for row if uid > 0. uid < 0 indicates to return all active records
    Returns
    -------
    list
        list of dicts if successful, empty list otherwise.

    """
    resp = {}
    with uow as unit_of_work:
        if uid == -1:
            resp = unit_of_work.repoObj.getAll(active=True)
            uid = "all"
        elif uid >= 0:
            resp = unit_of_work.repoObj.get(uid)
        else:
            raise MissingRequestParamsError("Not a valid parameter %s" % uid)
    if not resp:
        raise NoDataError("id %s" % (uid))
    return resp
