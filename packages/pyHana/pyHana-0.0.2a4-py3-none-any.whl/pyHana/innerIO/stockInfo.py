import os, sys
import pandas as pd
import re

# here = os.path.dirname(__file__)
# sys.path.append(os.path.join(here, '..'))
from   ..common import conf, dataProc

# 증권사에서 조회한 데이터를 파일로 저장하여, 데이터 분석 시 사용 (분석 수행 시 증권사 IF 최소화)
# 화면별 저장할 컬럼 정의
saveColumns = {
    "t8410" : ['일자', '시가', '고가', '저가', '종가', '거래량', '거래대금'],
    "t3518" : ['일자', '종가'],
}

def _SaveStockTrade(trcode, shCode, newData):            
# data 분석 시 증권사 IF를 최소화 하기 위해, 증권사에서 조회한 데이터를 파일로 저장 
# 종목코드 + 거래일자 형태의 데이터만 저장
# 기존 + 신규 데이터 병합하여 저장.
# 중복 row가 있는 경우 기존 데이터는 제외 처리    
                
    # 신규 저장할 데이터, 내부적 연산 시 list형으로 통일 
    if type(newData) == type(pd.DataFrame([])):
        newData = newData.values.tolist()
    elif type(newData) != list:
        raise Exception('pyHana >> list형 또는 DataFrame 형태만 처리 가능')

    # 저장 파일명 구하기. 데이터가 큰 경우 shCode 값으로 파일 분할 처리
    # partNm = (lambda trcode, shCode: '_' + "%02d"%(int(re.sub("[^0-9]", "9", shCode)) % 99) if trcode in ["t8410"] else '')(trcode, shCode)
    filePathNm = conf.stockInfoPath + "/일별주가/" + shCode + ".pkl"            
    
    # 기존 데이터 Read
    currData = dataProc.ReadPickleFile(filePathNm)                 
    if not currData.get('columns'):
        currData['columns'] = saveColumns[trcode]
        
    if not currData.get(shCode):
        currData[shCode] = []

    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 sort후 dup 제거
    currData[shCode] = dataProc._MergeData(currData[shCode], newData) 
        
    dataProc.WritePickleFile(filePathNm, currData) 


def ReadStockTrade(shCode, trcode='t8410'):    
# data 분석 시 증권사 IF를 최소화 하기 위해, 증권사에서 조회한 데이터 저장한 파일에서 데이터 추출 

    # 저장 파일명 구하기. 데이터가 큰 경우 shCode 값으로 파일 분할 처리
    # partNm = (lambda trcode, shCode: '_' + "%02d"%(int(re.sub("[^0-9]", "9", shCode)) % 99) if trcode in ["t8410"] else '')(trcode, shCode)
    filePathNm = conf.stockInfoPath + "/일별주가/" + shCode + ".pkl"            

    currData = dataProc.ReadPickleFile(filePathNm)
        
    retVal = currData.get(shCode, [])

    retVal = pd.DataFrame(retVal, columns=currData.get('columns',''))

    return retVal


def ReadStockItemInfoDetail(shCode=''):   
    """
    종목 상세정보 return
    """    
    
    filePathNm = conf.stockInfoPath + "/stockitem_info.pkl"
    currData = dataProc.ReadPickleFile(filePathNm)

    retVal = []
    if shCode == '':
        for key, _ in currData['data'].items():
            if currData['data'][key].get('info'):
                retVal.append(currData['data'][key]['info'])        
    else:
        if currData['data'].get(shCode):
            retVal = [currData['data'][shCode].get('info','')]

    # retVal = pd.DataFrame(retVal, columns=currData.get('columns',''))
                # dfStock = dfStock.astype({'시가총액':'int64', '현재가':'int64', 'PER':'float64','EPS':'int64','PBR':'float64',
                #                         'ROA':'float64','ROE':'float64','EBITDA':'float64','EVEBITDA':'float64',
                #                         '액면가':'float64','SPS':'float64','CPS':'float64','BPS':'float64','T.PER':'float64',
                #                         'T.EPS':'float64','PEG':'float64','T.PEG':'float64',
                #                         '주식수':'int64','자본금':'int64','배당금':'int64','배당수익율':'float64','외국인':'float64' })    

    return retVal, currData.get('columns','')

def ReadEbestMarketIndexInfo(symbol):       
    filePathNm = conf.marketIndexPath + "/이베스트증권/" + symbol + ".pkl"
    currData = dataProc.ReadPickleFile(filePathNm)

    return currData    

def SaveEbestMarketIndexInfo(trcode, symbol, hname, nation, kind, newData):            
# data 분석 시 증권사 IF를 최소화 하기 위해, 증권사에서 조회한 데이터를 파일로 저장 
# 해외지수 + 기준일자 형태의 데이터만 저장
# 기존 + 신규 데이터 병합하여 저장.
# 중복 row가 있는 경우 기존 데이터는 제외 처리    
                
    # 신규 저장할 데이터, 내부적 연산 시 list형으로 통일 
    if type(newData) == type(pd.DataFrame([])):
        newData = newData.values.tolist()
    elif type(newData) != list:
        raise Exception('pyHana >> list형 또는 DataFrame 형태만 처리 가능')

    # 기존 데이터 Read
    filePathNm = conf.marketIndexPath + "/이베스트증권/" + symbol + ".pkl"
    currData = dataProc.ReadPickleFile(filePathNm)                 
    if not currData.get('columns'):
        currData['columns'] = saveColumns[trcode]

    currData['지수명']   = hname
    currData['국가']     = nation
    currData['종목종류'] = kind

        
    if not currData.get('data'):
        currData['data'] = []

    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 sort후 dup 제거
    currData['data'] = dataProc._MergeData(currData['data'], newData) 
        
    dataProc.WritePickleFile(filePathNm, currData) 