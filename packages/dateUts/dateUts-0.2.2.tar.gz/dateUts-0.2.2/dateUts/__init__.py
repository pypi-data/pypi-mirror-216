from datetime import date, datetime, timedelta as td
from dateutil.relativedelta import relativedelta


class DateUts():
    date = None

    def __init__(self,date):
        self.date = date

    def is_weekend(self):
        return self.date.weekday() in [5, 6]
    
    def weekday(self):
        return self.date.weekday()

    def __repr__(self):
        return f"<DateUts {self.date.strftime('%Y-%m-%d %H:%M:%S')}>"


# output: True (2023-04-22 is a Saturday)


#========= USAGE ============
#Ex1:
# > sqlToDate('yyyy-MM-dd')
# > <datetime>

def sqlToDate(date_str:str):
    return DateUts(datetime.strptime(date_str,"%Y-%m-%d"))

#========= USAGE ============
#Ex1:
# > dateToSql(<datetime>)
# > 'yyyy-MM-dd'

def dateToSql(dt:date):
    return DateUts(dt.strftime(dt,"%Y-%m-%d"))

#========= USAGE ============
#Ex1:
# > now()  ,  now(fmt='%Y-%m-%d')   ,   now(fmt='sql')
# > <datetime>, 'yyyy-MM-dd',  'yyyy-MM-dd'

def now(fmt=None):
    v =  datetime.now()
    return fmtDate(v,fmt)

#========= USAGE ============
#Ex1:
# > today()  ,  today(fmt='%Y-%m-%d')   ,   today(fmt='sql')
# > <datetime>, 'yyyy-MM-dd',  'yyyy-MM-dd'

def today(fmt=None,addDays=0):
    v =  datetime.now().date()
    v =  v if not addDays else dateAdd(today(),addDays,'day')
    return fmtDate(v,fmt)

#========= USAGE ============
#Ex1:
# > yesterday()  ,  yesterday(fmt='%Y-%m-%d')   ,   yesterday(fmt='sql')
# > <datetime>, 'yyyy-MM-dd',  'yyyy-MM-dd'

def yesterday(fmt=None):
    v = today().date - td(1)
    return fmtDate(v,fmt)

def tomorrow(fmt=None):
    v = today().date + td(1)
    return fmtDate(v,fmt)

#========= USAGE ============
#Ex1:
# > start,end = <date:2022-05-23>,<date:2022-05-24>
# > dateRange(start,end) ,  dateRange('2022-05-23',1,'day',fmt='%Y-%m-%d')   ,   dateRange('2022-05-23',1,'day',fmt='sql')
# > [<datetime>,<datetime>], ['2022-05-23','2022-05-24'],  ['2022-05-23','2022-05-24']

def dateRange(start:date,end:date,fmt=None,filter_lbd:callable=None):
    start = start.date if isinstance(start,DateUts) else start
    end   = end.date if isinstance(end,DateUts) else end

    if start > end:
        dates = [dateAdd(start,x*-1) for x in range(0, (start-end).days + 1)]
    else:
        dates = [dateAdd(start,x) for x in range(0, (end-start).days + 1)]
    
    if filter_lbd:
        dates = list(filter(filter_lbd,dates))
    if fmt:
        dates = [fmtDate(x,fmt) for x in dates]
    
    return dates

#========= USAGE ============
#Ex1:
# > dateAdd('2022-05-23',1,'day') ,  dateAdd('2022-05-23',1,'day',fmt='%Y-%m-%d')   ,   dateAdd('2022-05-23',1,'day',fmt='sql')
# > <datetime>, '2022-05-24',  '2022-05-24'
#Ex2:
# > dateAdd('2022-05-23',-1,'day') ,  dateAdd('2022-05-23',-1,'day',fmt='%Y-%m-%d')   ,   dateAdd('2022-05-23',-1,'day',fmt='sql')
# > <datetime>, '2022-05-22',  '2022-05-22'

def dateAdd(date:date,qtd:int,unit:str="day",fmt=None):
    date = date.date if isinstance(date,DateUts) else date
    if unit == 'day':
        v = date + td(qtd) if qtd > 0 else date - td(abs(qtd))
    elif unit == 'year':
        v = date.replace(year = date.year + qtd)
    elif unit == 'hour':
        v = date + td(hours=qtd)
    elif unit == 'minute':
        v = date + td(minutes=qtd)
    elif unit == 'second':
        v = date + td(seconds=qtd)
    elif unit == 'month':
        v = date + relativedelta(months=qtd)



    return fmtDate(v,fmt)

#========= USAGE ============ 
#Obs: Today is "2022-05-23"
#Ex1:
# > lastWorkingDate()  ,  lastWorkingDate(fmt='%Y-%m-%d')   ,   lastWorkingDate(fmt='sql')
# > <datetime>, '2022-05-20',  '2022-05-20'
#Ex2:
# > lastWorkingDate(ref=<date:'2022-03-24'>)  ,  lastWorkingDate(ref=<date:'2022-03-24'>,fmt='%Y-%m-%d')   ,   lastWorkingDate(ref=<date:'2022-03-24'>,fmt='sql')
# > <datetime>, '2022-05-23',  '2022-05-23'

def lastWorkingDate(ref:date=None,fmt=None): #IGNORE SATURDAY AND SUNDAY
    y = yesterday() if not ref else dateAdd(ref,-1,'day')
    if y.weekday() in [5,6]:
        return lastWorkingDate(y,fmt)
    return fmtDate(y,fmt)



def nextWorkingDate(ref:date=None,fmt=None): #IGNORE SATURDAY AND SUNDAY
    t = tomorrow() if not ref else dateAdd(ref,1,'day')
    if t.weekday() in [5,6]:
        return nextWorkingDate(t,fmt)
    return fmtDate(t,fmt)


#========= USAGE ============
#Ex1:
# > today()  ,  today(fmt='%Y-%m-%d')   ,   today(fmt='sql')
# > <datetime>, 'yyyy-MM-dd',  'yyyy-MM-dd'

def fmtDate(dt:date,fmt:str):
    fmt= fmt if not fmt else ("%Y-%m-%d" if fmt == "sql" else fmt)
    dt = dt.date if isinstance(dt,DateUts) else dt

    return DateUts(dt) if not fmt else dt.strftime(fmt)

def dateMatch(dt:str,fmt:str):
    fmt = "%Y-%m-%d" if fmt == "sql" else fmt

    try:
        datetime.strptime(dt,fmt)
    except ValueError:
        return False

    return True

def firstDay(sql_dte:date,fmt:str=None):
    dte = sql_dte if isinstance(sql_dte,date) or isinstance(sql_dte,DateUts) else sqlToDate(sql_dte)
    dte = fmtDate(dte,"%Y-%m-01")
    firstDay = sqlToDate(dte)
    return fmtDate(firstDay,fmt)

def lastDay(sql_dte:date,fmt:str=None):
    dte = sql_dte if isinstance(sql_dte,date) or isinstance(sql_dte,DateUts) else sqlToDate(sql_dte)
    dte = sqlToDate(dateAdd(dte,1,"month",fmt="%Y-%m-01"))
    dte = dateAdd(dte,-1,"day")
    return fmtDate(dte,fmt)



Fnc_noWeekends = lambda dt:dt.weekday() not in [5,6]


#a = fmtDate("202306","%Y%m")
#a = dateRange(firstDay(today()).date,lastDay(today()).date,filter_lbd = Fnc_noWeekends)
#a[0].weekday()
# a = DateUts(dt.now())
# print(a)
# a = lastWorkingDate(fmt="%Y-%m-%d")
# rng = dateRange(sqlToDate("2022-05-01"),sqlToDate("2022-05-10"))
# rng = dateRange(sqlToDate("2022-05-10"),sqlToDate("2022-05-01"))
# a=1