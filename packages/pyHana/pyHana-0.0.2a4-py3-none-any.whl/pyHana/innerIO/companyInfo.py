from ..common import conf, dataProc, code
import pandas as pd


def GetCmpnyFinInfo(srchItem , unit="억"):
    #acct_list = ['매출액','영업이익','당기순이익','총포괄손익']
    unit_list = {'천' : 1000, '만' : 10000, '백만' : 1000000, '천만' : 10000000, '억' : 100000000, '십억' : 1000000000, '조' : 1000000000000 }
    data = []

    if not unit_list.get(unit):
        print('유효하지 않은 금액단위 > ', unit)
        print('선택가능한 금액단위 > ', unit_list.keys())        
        unit = "억"

    itemList = code._GetStockItemListDart(srchItem)

    filePathNm = conf.companyInfoPath + "/재무정보(금감원).pkl"
    acntInfo = dataProc.ReadPickleFile(filePathNm)        
    
    if acntInfo['data'].get(itemList[0]) and acntInfo['data'][itemList[0]].get('info'):
        for x in acntInfo['data'][itemList[0]]['info']:
            data.append( itemList + x[0:3] + 
                            [  val if type(val) == str else int(round(val / unit_list[unit], 0)) for val in x[3:] ]
                        )
    
    return data, ['종목코드','종목명']+acntInfo['columns']


def GetDividendInfo(srchItem):
    data = []

    itemList = code._GetStockItemList(srchItem)

    filePathNm = conf.companyInfoPath + "/주식배당정보(한국거래소).pkl"
    acntInfo = dataProc.ReadPickleFile(filePathNm)        
    
    if acntInfo['data'].get(itemList[0]) and acntInfo['data'][itemList[0]].get('info'):
        for x in acntInfo['data'][itemList[0]]['info']:
            data.append( itemList + x )
    
    return data, ['종목코드','종목명']+acntInfo['columns']