import workbookapi
import datetime
import colorama
from colorama import Fore, Style
colorama.init()

MISSINGTHRESHOLD = 8
ASDept = 3
wb = workbookapi.wbSession(configfile='wb.ini')

#TODO  - Pull all the time, sum by employee, email it out

print("Getting last week's timesheets")
#Get last monday
today = datetime.datetime.today().date()
lastmonday = today - datetime.timedelta(days=(today.weekday()+7))
thispastmonday = today - datetime.timedelta(days=(today.weekday()))
startdate = lastmonday.isoformat()
enddate = thispastmonday.isoformat()
print(f'Pulling timesheets for the week of {startdate} to {enddate}')
rawtime = wb.raw_time(start_date=startdate, end_date=enddate)
employees = wb.employees()

empdict = {emp['Id']:{'name':emp['EmployeeName'],'mgrid':emp['ManagerResourceId'], 'hours':0, 'dept':emp['DepartmentId'], 'active':emp['Active']} for emp in employees}
for emp in empdict:
    empdict[emp]['mgrname'] = empdict[empdict[emp]['mgrid']]['name']

for time in rawtime:
    if 'Hours' in time:
        empdict[time['ResourceId']]['hours'] += time['Hours']
# PRINT IT ALL OUT - THIS CAN BE REPLACED BY AN EMAIL
#empdict = sorted(empdict.items(), key=lambda item: item[1]['mgrname'])
emplist = list(empdict.values())
emplist = sorted(emplist, key=lambda k: k['mgrname'])
lastmgr = ""
for emp in emplist:
    if emp['dept'] == ASDept and emp['active']==True:
        if lastmgr != emp['mgrname']:
            print(f"{Fore.BLUE}{emp['mgrname']}{Style.RESET_ALL}")
            lastmgr = emp['mgrname']
        print(f"{Fore.RED if emp['hours'] < MISSINGTHRESHOLD else ''}{emp['name']}: {emp['hours']}{Style.RESET_ALL}")

#TODO - Use SES to e-mail out the results - https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
