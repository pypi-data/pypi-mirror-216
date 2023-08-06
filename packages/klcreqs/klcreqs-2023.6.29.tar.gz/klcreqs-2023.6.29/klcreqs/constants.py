from datetime import *
from multiprocessing import Process, Pool
from multiprocessing.pool import *
from time import sleep
import json
import math
import numpy as np
import pandas as pd
import requests
import sys
import time
import urllib
import urllib.parse
from tqdm import tqdm


requests.packages.urllib3.disable_warnings()
a = pd.read_csv(r'C:\KL_Capital Dropbox\Python\py4klc\a.csv')
user_serial = a.loc[2,'a']
key = a.loc[2,'b']
authorization = (user_serial, key)


class auth:
    a = pd.read_csv(r'C:\KL_Capital Dropbox\Python\py4klc\a.csv')
    auths = []
    for r in a.index: 
        auths.append(tuple(a.loc[r].to_list()))

    def __init__(self):
        self.n = 0
        self.auth = auth.auths[self.n]
        return 

    def __next__(self):
        if self.n < 3:
            self.n +=  1
        else:
            self.n = 0
        self.auth = auth.auths[self.n]
        return self.auth

# formula api config
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
ofdb_endpoint = "https://api.factset.com/analytics/ofdb/v1/database/"
cross_sectional_endpoint = 'https://api.factset.com/formula-api/v1/cross-sectional'
timeseries_endpoint = "https://api.factset.com/formula-api/v1/time-series"
status_endpoint = 'https://api.factset.com/formula-api/v1/batch-status'
result_endpoint = 'https://api.factset.com/formula-api/v1/batch-result'
intang_path = r'CLIENT:/GK_INDEXES/GLOBAL_INDEXES/MID-LARGE/AC/KLSUX_AC.OFDB'
uri = urllib.parse.quote(intang_path, safe="")
url = f'{ofdb_endpoint}{uri}/dates'
rebals_rtrv = json.loads(requests.get(url, auth=authorization, headers=headers).text)
# print(rebals_rtrv)
# with open(r'C:\\KL_Capital Dropbox\\Python\\py4klc\\py4klc\\rebals.txt', 'w') as f:
#     f.write(str(rebals_rtrv[0]))