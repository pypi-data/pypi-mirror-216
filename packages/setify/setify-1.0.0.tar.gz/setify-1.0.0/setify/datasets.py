import pandas as pd
from setify import utils



def _get_server():
    # return 'https://setify-server.herokuapp.com'
    return 'http://159.223.176.152:8080'


def walmart_store_location():
    fpath = utils.load_data(
        _get_server() + "/walmart_store_location", 'walmart_store_location.h5')
    return pd.read_hdf(fpath)


def holiday_songs_spotify():
    fpath = utils.load_data(
        _get_server() + "/holiday_songs_spotify", 'holiday_songs_spotify.h5')
    return pd.read_hdf(fpath)


def titanic():
    fpath = utils.load_data(_get_server() + "/titanic", 'titanic.h5')
    return pd.read_hdf(fpath)



def wine_quality():
    fpath = utils.load_data(_get_server() + "/wine_quality", 'wine_quality.h5')
    return pd.read_hdf(fpath)



def iris():
    fpath = utils.load_data(_get_server() + "/iris", 'iris.h5')
    return pd.read_hdf(fpath)


def logic_gate_not():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_not", 'logic_gate_not.h5')
    return pd.read_hdf(fpath)


def logic_gate_and():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_and", 'logic_gate_and.h5')
    return pd.read_hdf(fpath)


def logic_gate_nand():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_nand", 'logic_gate_nand.h5')
    return pd.read_hdf(fpath)


def logic_gate_or():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_or", 'logic_gate_or.h5')
    return pd.read_hdf(fpath)


def logic_gate_nor():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_nor", 'logic_gate_nor.h5')
    return pd.read_hdf(fpath)


def logic_gate_xor():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_xor", 'logic_gate_xor.h5')
    return pd.read_hdf(fpath)


def logic_gate_xnor():
    fpath = utils.load_data(
        _get_server() + "/logic_gate_xnor", 'logic_gate_xnor.h5')
    return pd.read_hdf(fpath)


def boston_housing():
    fpath = utils.load_data(
        _get_server() + "/boston_housing", 'boston_housing.h5')
    return pd.read_hdf(fpath)