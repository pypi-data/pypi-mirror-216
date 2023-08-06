from ..outerIO  import marketIndex as o_mi
from ..innerIO  import marketIndex as i_mi

def syncBalticIndex(sDate, eDate):
    indexList = ['BDI','BCI','BPI','BSI']

    newData = o_mi.GetBalticIndex(sDate, eDate)

    for i in range(len(indexList)):
        i_mi.SaveMarketIndex(indexList[i], [[data[0], data[i+1]]for data in newData])    