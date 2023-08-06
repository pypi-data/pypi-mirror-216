from . import conf, dataProc
import pandas as pd

# 금감원과 이베스트 증권에서 관리하는 회사명이 다름

# 금감원 자료 처리시에 사용
def _GetShcodeDart(title):    
    filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"    
    stockItemList = dataProc.ReadPickleFile(filePathNm)    
               
    if stockItemList['회사명'].get(title):
        retVal = [ stockItemList['회사명'][title], title ]
    else:
        retVal = []
        
    return retVal

def _GetCmpnyNameDart(shCode):    
    filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"    
    stockItemList = dataProc.ReadPickleFile(filePathNm)    
    
    if stockItemList['종목코드'].get(shCode):
        retVal = [ shCode, stockItemList['종목코드'][shCode]  ]
    else:
        retVal = []
               
    return retVal

def _GetStockItemListDart(srchItem):
    itemList = _GetCmpnyNameDart(srchItem)
    if len(itemList) == 0:
        itemList = _GetShcodeDart(srchItem) 
    
    return itemList


# 회사명, 종목코드 추출 시 기본적으로 ebest 데이터 사용
def _GetShcode(title, gb=''):    
    retVal = []
    
    filePathNm = conf.stockInfoPath + "/stockitem_info.pkl"    
    stockItemList = dataProc.ReadPickleFile(filePathNm)    

    if gb =='LIKE':
        for shCode in stockItemList['data'].keys():
            if title in stockItemList['data'][shCode]['hName']:
                retVal.append([shCode, stockItemList['data'][shCode]['hName']])
    else:
        for shCode in stockItemList['data'].keys():
            if title == stockItemList['data'][shCode]['hName']:
                retVal = [shCode, stockItemList['data'][shCode]['hName']]
                break
    
    return retVal

def _GetCmpnyName(shCode):    
    filePathNm = conf.stockInfoPath + "/stockitem_info.pkl"    
    stockItemList = dataProc.ReadPickleFile(filePathNm)    
    
    if stockItemList['data'].get(shCode):
        retVal = [ shCode, stockItemList['data'][shCode]['hName']  ]
    else:
        retVal = []
               
    return retVal

def _GetStockItemList(srchItem):
    stockItem = _GetCmpnyName(srchItem)
    if len(stockItem) == 0:
        stockItem = _GetShcode(srchItem) 
    
    return stockItem


def _GetStockItemListAll():   
    """
    종목명 return
    """
    filePathNm = conf.stockInfoPath + "/stockitem_info.pkl"
    currData = dataProc.ReadPickleFile(filePathNm)

    retVal = []
    for key, _ in currData['data'].items():
        if currData['data'][key].get('hName'):
            retVal.append([key, currData['data'][key]['hName']])                      

    retVal = pd.DataFrame(retVal, columns=['종목코드','종목명'])

    return retVal    