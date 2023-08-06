''' created 10/19/2022 '''

from .constants import *

class formula_api:
    http_headers = {"Content-type": "application/json", "Accept": "application/json"}
    time_series_url = 'https://api.factset.com/formula-api/v1/time-series'
    cross_sectional_url = 'https://api.factset.com/formula-api/v1/cross-sectional'
    batch_status_url = 'https://api.factset.com/formula-api/v1/batch-status'
    batch_results_url = 'https://api.factset.com/formula-api/v1/batch-result'
    def __init__(self, formulas, ep='cs', ids=None, uni=None, batch=False, dnames=None, bof=False, sof=False):
        # self.acount = 0
        self.auths = auth()
        self.authorization = self.auths.auth
        self.formulas = formulas
        self.ep = ep
        self.ids = ids
        self.uni = uni
        self.batch = batch
        self.dnames = dnames
        self.bof = bof
        self.sof = sof
        self.st = time.time()
        r = formula_api.__request_handling(self)

        # print(r.text)
        
        try:
            self.response = json.loads(r.text)
        except:
            self.response = r

    def __request_handling(self):
        # send request as defined
        req = formula_api.make_request(self)
        # print(req.status_code)

        # if request returns an error and bof is set to true, override endpoint, batch settings and resend as batch
        if req.status_code >= 408 and self.bof == True:
            self.ep = 'ts'
            self.batch = True
            # print('non-batch failed, batching')
            req = formula_api.make_request(self)

        # if error 429 is returned, override endpoint and batch settings, switch authorization, and resend
        if self.status_code == 429 and self.batch == True:
            self.ep = 'ts'
            self.batch = True
            formula_api.switch_auth(self)
            # print('batch failed, resubmitting with authswitch')
            req = formula_api.__request_handling(self)
            
        try:
            keys = json.loads(req.text)['data'].keys()
        except:
            keys = ['not']

        with open('log.txt', 'w') as f:
            f.writelines(req.text)

        # verifies the response status is in the usual format and calls batch processing function
        if self.batch == True and 'id' in keys: # and type(json.loads(req.text)['data']) == dict: this wouldnt work b/c 'data' is a list that holds dicts
           req = formula_api.__poll_return_batch(self, req)
        
        self.ft = time.time()
        return req 
        
    
    def __poll_return_batch(self, req):
        sleep(5)

        res = json.loads(req.text)
        try:
            batch_id = res['data']['id']
        except:
            return req



        batch_id_request_json = json.dumps({"data": {"id": batch_id}})

        while True:
            batch_status = requests.post(url=status_endpoint,
                                                  data=batch_id_request_json,
                                                  auth=self.authorization,
                                                  headers=headers,
                                                  verify=False)
            # print(batch_status.status_code)
            sleep(10)
            # print(type(batch_status.text))
            try:
                batch_status_response = json.loads(batch_status.text)
            except:
                # print(batch_status.text)
                print('failed batch_status_response load')
                print(batch_status.status_code)
                
            # print(batch_status_data['data']['status'])
            if batch_status_response['data']['status'] == 'DONE':
                batch_result = requests.post(url=result_endpoint,
                                                    data=batch_id_request_json,
                                                    auth=self.authorization,
                                                    headers=headers,
                                                    verify=False)
                
                if batch_result.status_code == 200:
                    return batch_result
                elif batch_result.status_code >= 400:
                    print('error retrieving batch_result_response')
                    print(batch_result.status_code)
                    # print(batch_result)
                    return
            elif batch_status_response['data']['status'] != 'DONE':
                pass

    def make_request(self):
        request_json = formula_api.__create_request_json(self)
        if self.ep in ['ts', 'time', 'timeseries', 'time_series', 'time series']:
            req = formula_api.time_series_request(
                self,
                request_json=request_json
            )
        elif self.ep in ['cs', 'cross', 'crosssectional', 'cross_sectional', 'cross sectional']:
            req =  formula_api.cross_sectional_request(
                self,
                request_json=request_json
            )
        else:
            raise Exception('Exception no valid endpoint provided, use \"ts\" or \"cs\"')
        self.status_code = req.status_code
        return req


    def time_series_request(self, request_json):
        return formula_api.__http_post(
            self,
            URL=formula_api.time_series_url,
            json_string=request_json
        )


    def cross_sectional_request(self, request_json):
        return formula_api.__http_post(
            self,
            URL=formula_api.cross_sectional_url,
            json_string=request_json
        )

    def __create_request_json(self):
        request = {
            "data": {
                "formulas": self.formulas,
                "flatten": "Y"
            }
        }
        if self.batch == True:
            request['data']['batch'] = 'Y'
        if self.dnames is not None:
            request['data']['displayName'] = self.dnames
        if self.ids is not None:
            request['data']['ids'] = self.ids
        elif self.uni is not None:
            request['data']['universe'] = self.uni
        elif self.uni == None and self.ids == None:
            request['data']['ids'] = ['dummy']
        return json.dumps(request)

    
    def __http_post(self, URL, json_string):
        try:
            r = requests.post(
                URL,
                auth=self.authorization,
                headers=formula_api.http_headers,
                data=json_string,
                verify=False,
            )
            return r
        except Exception as e:
            return False, str(e)

    def status_code(self):
        return self.status_code

    def df(self):
        # print(self.response.keys())
        if 'data' in list(self.response.keys()):
            df = pd.DataFrame(self.response['data'])
        else:
            print(self.response.keys())
            print(self.response)
        return df

        # try:
        #     self.df = pd.json_normalize(self.response['data'])
        # except:
        #     try:
        #         self.df = pd.DataFrame(self.response[0]['data'], index=range(math.ceil(len(list(self.response.values()))/len(list(self.response.keys())))))
        #     except:
        #         try:
        #             self.df = pd.DataFrame(self.response)
        #         except:
        #             with open('logee.txt', 'w') as f:
        #                 f.writelines(self.response)
                
        # return df
            

    @property
    def runtime(self):
        self.rt = (self.ft - self.st)
        return self.rt

    def switch_auth(self):
        self.authorization = next(self.auths)
        # print('ratelimit reached, switching')
        # print(self.authorization)
        return

    def generate_meta(self):
        df_log = pd.DataFrame()
        df_log['name'] = [self.dnames]
        df_log['form'] = [self.formulas]
        df_log['ep'] = [self.ep]
        df_log['size'] = [sys.getsizeof(self.df().iloc[0,1])]
        df_log['time'] = [self.runtime]
        df_log['time/id'] = [self.runtime/len(self.ids)]
        if self.ids != None:
            df_log['n_ids'] = len(self.ids)
        elif self.uni != None:
            df_log['n_ids'] = len(formula_api(formulas=[f'{self.uni}'], uni=self.uni, ep='ts').df())
        return df_log


        





class ofdb_api:
    def __init__(self, path):
        self.host = "https://api.factset.com/analytics/ofdb/v2/database/"
        self.path = path
        self.uri = urllib.parse.quote(self.path, safe="")
        return

    def get_dates(self):
        url = f'{self.host}{self.uri}/dates'
        r = requests.get(url, auth=authorization, headers=headers)
        if r.status_code >= 400:
            print(r)
            print(r.text)
            return
        sleep(5)
        response = json.loads(r.text)['data']
        return response
    
    

    def get_symbols_for_date(self, d):
        url = f'{self.host}{self.uri}/dates/{d}/symbols'
        r = requests.get(url, auth=authorization, headers=headers)
        if r.status_code >= 400:
            print(r)
            print(r.text)
            return
        sleep(5)
        response = json.loads(r.text)['data']
        return response



    def delete_date(self, d):
        url = f"{self.host}{self.uri}/dates/{d}"
        r = requests.delete(url, auth=authorization, headers=headers)
        if r.status_code >= 400:
            print(r)
            print(r.text)
        return

    def delete_symbol(self, symbol, d=None):
        if d is None:
            url = f'{self.host}{self.uri}/symbols/{symbol}'
        elif d is not None:
            url = f'{self.host}{self.uri}/dates/{d}/symbols/{symbol}'
        r = requests.delete(url, auth=authorization, headers=headers)
        if r.status_code > 204:
            print(r)
            print(r.text)
        return

    def delete_ofdb(self):
        url = f'{self.host}{self.uri}'
        conf = input(f'type \"confirm\" to confirm deletion of {url}: ')
        if conf != 'confirm':
            return
        else:
            r = requests.delete(url, auth=authorization, headers=headers)
            if r.status_code > 204:
                # print(r)
                # print(r.text)
                sleep(30)
                r = requests.delete
            return

    def get_fields(self):
        url = f'{self.host}{self.uri}/fields'
        r = requests.get(url, auth=authorization, headers=headers)
        return r



    @staticmethod
    def __parse(df, orient):
        if orient not in ['date', 'symbol']:
            raise Exception('invalid orient arg. acceptable values: date, symbol')
            return
        df.fillna(0, inplace=True)
        
        try:
            df.set_index(orient, drop=True, inplace=True)
        except:
            pass

        dct = df.to_dict(orient='index')
        bodies = []
        for i, j in dct.items():
            body = {'data': []}
            body['data'].append({orient: i})
            body['data'].append({'content': j})
            bodies.append(body)
        return bodies

    def upload(self, inp, method, parsed, idx):
        if method not in ['symbol', 'date']:
            raise Exception('invalid method arg. must be symbol or date')
        if type(inp) not in (pd.DataFrame, list):
            raise Exception('input data must be of type DataFrame, used with parsed=False, or list, used with parsed=True')
        
        parsed = parsed
        orient = method        
        url = f'{self.host}{self.uri}/{orient}s'

        if parsed == False:
            self.bodies = ofdb_api.__parse(inp, orient)
            for i in self.bodies:
                body = i
                body['data'][0]['content'] = [{k: None if v == 'nan' else v for k,v in i.items()} for i in body['data'][0]['content']]
                body = json.dumps(body)
                r = requests.post(url, auth=authorization, headers=headers, data=body)

                if r.status_code >= 400:
                    print('error in upload')
                    with open('json_dump.txt', 'w') as f:
                        f.writelines(body)
                    # print(body)
                    print(r.text)
                    return r

        elif parsed == True:
            if type(idx) not in (str, int):
                raise Exception('pre-parsed input must have only 1 index of type int or str')
            body = {'data': [{orient: idx, 'content': inp}]}
            
            body['data'][0]['content'] = [{k: None if v == 'nan' else v for k,v in i.items()} for i in body['data'][0]['content']]
            # body = {k: None if v=="nan" else v for k, v in body.items() }
            
            
            
            body = json.dumps(body)
            r = requests.post(url, auth=authorization, headers=headers, data=body)
            if r.status_code >= 400:
                print('error in upload')
                with open('json_dump.txt', 'w') as f:
                    f.writelines(body)
                # print(body)
                print(r)
                print(r.status_code)
                print(r.text)
        return r
    
    ''' in development '''

    # def change_date(self, d):
    #     url = f"{self.host}{self.uri}/dates/{d}"
    #     dates_in = self.get_dates(self)
    #     if d in dates_in:
    #         raise Exception('date already exists in ofdb')
    #     fields_in = self.get_fields(self)
    #     r = formula_api(

    #     )
        

    