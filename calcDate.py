from datetime import datetime
from dateutil.relativedelta import relativedelta

class dateCalculator:
    def calcDatetime(self, dtNow, dtDiff):
        print(dtDiff)
        if '년 전' in dtDiff:
            idx=dtDiff.find('년')
            ds=dtDiff[idx-1:idx]
            #스트리밍 시간:~개월 이렇게 뜨는것 있어 형식 바꿈
            d = int(ds)
            dtPub=dtNow - relativedelta(years=d)
        elif '개월 전' in dtDiff:
            idx=dtDiff.find('개월')
            ds=dtDiff[idx-1:idx]
            d = int(ds)
            dtPub=dtNow - relativedelta(months=d)
        elif '주 전' in dtDiff:
            idx=dtDiff.find('주')
            ds=dtDiff[idx-1:idx]
            d = int(ds)
            dtPub=dtNow - relativedelta(weeks=d)
        elif '일 전' in dtDiff:
            idx=dtDiff.find('일')
            ds=dtDiff[idx-1:idx]
            d = int(ds)
            dtPub=dtNow - relativedelta(days=d)
        elif '시간 전' in dtDiff:
            idx=dtDiff.find('시간')
            ds=dtDiff[idx-1:idx]
            d = int(ds)
            dtPub=dtNow - relativedelta(hours=d)
        elif '분 전' in dtDiff:
            idx=dtDiff.find('분')
            ds=dtDiff[idx-1:idx]
            d = int(ds)
            dtPub=dtNow - relativedelta(minutes=d)
        elif '초 전' in dtDiff:
            idx=dtDiff.find('초')
            ds=dtDiff[idx-1:idx]
            d = int(ds)
            dtPub=dtNow - relativedelta(seconds=d)
            #최고공개일 넣어야하나?
        elif '최초 공개일' in dtDiff:
            dtPub=dtNow
        else:
            dtPub=dtNow
            
        return dtPub
    
