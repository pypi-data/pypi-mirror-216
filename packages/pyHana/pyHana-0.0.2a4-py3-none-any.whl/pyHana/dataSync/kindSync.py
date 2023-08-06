# from   ..common   import conf, dataProc
from ..outerIO  import kind
from ..common   import conf, dataProc

def SyncDividendInfo(sYear, eYear, currentPageSize = 100, marketType='', settlementMonth='', selYearCnt = 3):
    filePathNm = conf.companyInfoPath + "/주식배당정보(한국거래소).pkl"

    for selYear in range(eYear, sYear-1, -1*selYearCnt):
        if selYear >= (sYear + selYearCnt):
            print(selYear, selYearCnt)
            yearCnt = selYearCnt
        else:
            print(selYear, selYear - sYear + 1)
            yearCnt = selYear - sYear + 1

        resData, columns = kind.GetDividendInfo(selYear, currentPageSize, marketType, settlementMonth, yearCnt)


        # 기존 데이터 read
        currData = dataProc.ReadPickleFile(filePathNm)

        if not currData.get('data'):
            currData['data'] = {}   
        currData['columns'] = columns


        for idx in range(len(resData)):
            shcode = resData[idx][0]

            if not currData['data'].get(shcode):
                currData['data'][shcode] = {}
            if not currData['data'][shcode].get('info'):
                currData['data'][shcode]['info'] = []
            currData['data'][shcode]['종목명'] = resData[idx][1]

# ['종목코드', '종목명','사업년도','결산월','업종','업종별배당율','주식배당','액면가','기말주식수',
#                '주당배당금','배당성향','총배당금액','시가배당율']            
            currData['data'][shcode]['info'] = dataProc._MergeData(currData['data'][shcode]['info'] , [resData[idx][2:]])

        dataProc.WritePickleFile(filePathNm, currData) 


# def SyncFinancialInfo(sYear, eYear, currentPageSize = 100):
#      filePathNm = conf.kindPath + "/financial_info.pkl"

#      for year in range(sYear, eYear+1):
#          for fiscalgubun in (['1_4', 'half', '3_4', 'accntclosing', 'conn']):
#             resData, columns = kind.GetFinancialInfo(year, fiscalgubun, currentPageSize)

#### 데이터 구조 고민 필요