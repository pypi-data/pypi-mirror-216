from spidex.constants import DEPTH_URL, KLINE_URL, LATEST_TRADES_URL, MARKET_URL, POOL_INFO_URL,SPEC_URL,POOL_DETAIL_URL,\
    POOL_INCOME_URL,POOL_TRADES_URL,POOL_DEPOSITS_URL,POOL_WITHDRAWS_URL,POOL_SHARES_URL,POOL_USER_SHARE_URL





def get_depth(self, **kwargs):
    params = {**kwargs}
    return self.query(DEPTH_URL, params)

def get_kline(self, **kwargs):
    params = {**kwargs}
    return self.query(KLINE_URL, params)

def get_latest_trades(self, **kwargs):
    params = {**kwargs}
    return self.query(LATEST_TRADES_URL, params)

def get_market(self,**kwargs):
    params = {**kwargs}
    return self.query(MARKET_URL, params)

def get_specs(self):
    return self.query(SPEC_URL)

def get_pool_info(self):
    return self.query(POOL_INFO_URL)

def get_pool_detail(self,**kwargs):
    params = {**kwargs}
    return self.query(POOL_DETAIL_URL, params)

def get_pool_income(self,**kwargs):
    params = {**kwargs}
    return self.query(POOL_INCOME_URL, params)

def get_pool_trades(self, **kwargs):
    params = {**kwargs}
    return self.query(POOL_TRADES_URL, params)

def get_pool_deposits(self,**kwargs):
    params = {**kwargs}
    return self.query(POOL_DEPOSITS_URL, params)

def get_pool_withdraws(self,**kwargs):
    params = {**kwargs}
    return self.query(POOL_WITHDRAWS_URL, params)

def get_pool_shares(self,**kwargs):
    params = {**kwargs}
    return self.query(POOL_SHARES_URL, params)

def get_pool_user_share(self,**kwargs):
    params = {**kwargs}
    return self.query(POOL_USER_SHARE_URL, params)






