import pydap  
import xarray as xr  
from pydap.client import open_url  
from pydap.cas.get_cookies import setup_session


CASURL = 'https://cmems-cas.cls.fr/cas/login'
DATABASE = ['my', 'nrt']
SESSION = None


def init_session(usr=None, pwd=None, get_session=False):
    """
    Funcion para iniciar sesion en la red de copernicus. 
    usr = usuario de la web
    pwd = password
    get_session: nos devuelve la sesion en caso de que querramos. Esto nos
    sirve por si necesitamos multiples sesiones en paralelo.
    """

    session = setup_session(CASURL, usr, pwd)  
    session.cookies.set("CASTGC", session.cookies.get_dict()['CASTGC'])  
    if get_session:
        return session
    else:
        global SESSION
        SESSION = session
    return None


def get_datastore(dataset_id, session=None):
    """
    devuelve el datastore dado un dateset_id.
    """
    if not session:
        session = SESSION
    url = f'https://{DATABASE[0]}.cmems-du.eu/thredds/dodsC/{dataset_id}'
    try:
        data_store = xr.backends.PydapDataStore(open_url(url, session=session))
    except:
        url = f'https://{DATABASE[1]}.cmems-du.eu/thredds/dodsC/{dataset_id}'
        data_store = xr.backends.PydapDataStore(open_url(url, session=session))
    return  data_store


def dataset(user, pwd, dataset_id):
    """
    Funcion que inicia sesion y devuelve el dataset directamente. 
    """
    init_session(usr=user, pwd=pwd)
    data_store = get_datastore(dataset_id)
    return xr.open_dataset(data_store)