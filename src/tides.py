"""
KHOA에서 제공받는 API데이터로 ArcGIS Online에 있는 데이터를 수정
"""
import os
import requests
import pandas as pd

from arcgis.gis import GIS
from arcgis.features import GeoAccessor, GeoSeriesAccessor, FeatureLayerCollection
from copy import deepcopy
from datetime import datetime
from dotenv import load_dotenv

# local
from arcgis_utils import connect_to_agol, get_flc_by_id
from config import *

load_dotenv()

KEY = os.getenv("KHOA_KEY")

class APIError(Exception):
    pass

def call_api(obs_code: str) -> requests.Response:
    res = requests.get(
        url="http://www.khoa.go.kr/api/oceangrid/obsWaveHight/search.do",
        params = {
            "ServiceKey": os.getenv("KHOA_KEY"),
            "DataType": "obsWaveHeight",
            "ObsCode": obs_code,
            "Date": f"{datetime.today:%Y%m%d}",
            "ResultType": "json",
        },
    )
    if res.status_code != 200:
        raise RuntimeError(res)
    return res

def get_obs_code() -> list:
    """
    KHOA가 제공하는 관측소 정보를 읽는다.
    """
    wave_stations = DATA_DIR / "wave_stations.csv"