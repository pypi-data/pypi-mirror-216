from DAPPkg.com.extend.Cast import ExtCast as Cast
from DAPPkg.com.extend.Sort import ExtSort as Sort
from DAPPkg.com.extend.Filter import ExtFilter as Filter
from DAPPkg.com.extend.Valid import ExtValid as Valid
from DAPPkg.com.extend.Http import ExtHttp

from DAPPkg.statistic.Pearsonr import Pearsonr
from DAPPkg.statistic.Statsmodels import Statsmodels

class DataManager :
    _data_type = None
    cast = None
    filter = None
    sort = None
    valid = None
    
    def __init__(self, data) -> None:
        self._data_type = type(data)
        self.cast = Cast(data)
        self.filter = Filter(data)
        self.sort = Sort(data)
        self.valid = Valid(data)
        
class StatManager : 
    pearsonr = None
    statsmodels = None
    
    def __init__(self) -> None:
        self.pearsonr = Pearsonr()
        self.statsmodels = Statsmodels()        
        
class HttpManager :
    http = None
    def __init__(self) -> None:
        self.http = ExtHttp()