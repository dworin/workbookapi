from workbookapi import wbSession
from datetime import datetime, timedelta

#CompanyDepartmentId
DEPT = 3
#ProstatusId
ATRISKSTATUS = 4
#StatusId
ACTIVESTATUS = 1

def print_jobs(title, joblist, parenthetical=""):
    print(title)
    for job in joblist:
        if 'JobName' in job:
            if parenthetical == "":
                print(job['JobName'])
            else:
                printstring = f"{job['JobName']} ({job[parenthetical]})"
                print(printstring)
        else:
            print("Job had no name")

wb = wbSession(configfile='wb.ini')

jobs = wb.jobs()
atriskjobs = []
pastenddate = []
upcomingenddate = []
for job in jobs:
    #Make sure it's an active job and in the right department
    if job['CompanyDepartmentId'] == DEPT and job['StatusId'] == ACTIVESTATUS:
        #enddate = dateutil.parser.parse(job['EndDate'])
        
        #If it's at risk, add it to the At Risk List
        if 'ProstatusId' in job:
            if job['ProstatusId'] == ATRISKSTATUS:
                atriskjobs.append(job)
        #If End Date has passed, add it to the End Date Passed list
        enddate = datetime.strptime(job['EndDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if enddate <= datetime.now():
            pastenddate.append(job)
        #If End date is in the next 2 weeks
        if enddate < datetime.now() + timedelta(days=14) and enddate > datetime.now():
            upcomingenddate.append(job)


print_jobs('AT RISK JOBS', atriskjobs)
print_jobs('PAST END DATE', pastenddate, 'EndDate')
print_jobs('END DATE IN NEXT TWO WEEKS', upcomingenddate, 'EndDate')