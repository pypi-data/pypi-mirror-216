# klcreqs
library for streamlining requests to apis

# formula_api
to make a formula api request:
1. call the class with formula_api_request()
2. necessary arguments:
   * formulas -> list
   * ep (endpoint) -> string
        For time series requests accepted values are 'ts', 'time', 'timeseries', 'time_series', 'time series'
        For cross sectional requests accepted values are 'cs', 'cross', 'crossseectional', 'cross_sectional', 'cross sectional'
3. optional arguments:
   * ids -> list
   * uni (universe) -> string
        formulas must contain ofdb reference(s) if these are not included or the request will fail.
   * batch -> boolean
        set to True to submit the request as a batch - defaults to False
   * dnames -> tuple
        optional list of column names to be returned as headers for the requested data in place of messy default FS headers - defaults to None
   * bof (batch-on-fail) -> boolean
        set to True to automatically resubmit the request as a batch if the initial request fails - defaults fo False
4. thats it! call the .df() function on the request object to return requested data as a pandas DataFrame

# ofdb_api
call the ofdb_api class with path as the single required argument
call desired method on class in same line
must pass in date (d=) to methods as integer in YYYYMMDD format
symbols and paths args must be strings
any status_code >= 400 will prompt a print of response and response.text

methods:
1. get_dates()
    * returns list of dates in specified ofdb
2. delete_date(*d)
    * deletes specified date
    * returns nothing
3. delete_symbol(*symbol, **d)
    * deletes specified symbol, can specify date for more precision
    * returns nothing
4. delete_ofdb()
    * deletes ofdb at url passed in initialization of class
5. upload(*inp, *method, *parsed, **idx) 
    * inp can be either pandas DataFrame or dict, contains the data to upload, if DataFrame will automatically transform to dict on orient='index', required arg
    * method is either 'symbol' or 'date', required arg. Dataframe must have the method column (either symbol or date) as the index
    * parsed is Boolean, set to False if you want to pass in a dataframe and have the fxn parse inp itself. Set to True if you have already created a properly constructed dict to pass in as inp, requred arg
    * idx is the index for uploading pre-parsed input, must be either date or symbol value and sets the end-level location in path specification, required when parsed==True
    * returns response text value (r.text)

