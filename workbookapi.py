#Module: WorkbookAPI
#Purpose: Helper functions for the Workbook API

#API Docs: https://{YourInstance}.workbook.net/api/metadata

import requests
import configparser

class wbSession:
    session = requests.session()
    workbookpath = "https://workbook.net/api/"

    def __init__(self, workbookpath="", username="", password="", configfile=""):
        if configfile != "":
            config = configparser.ConfigParser()
            config.read(configfile)
            workbookpath = config['credentials']['workbookpath']
            username = config['credentials']['username']
            print(f'username={username}')
            password = config['credentials']['password']
            print(f'username={password}')
        self.workbookpath = workbookpath
        print(f'username={username} password={password} path={self.workbookpath}')
        self._authenticate(username,password)    

    def _authenticate(self, username, password):
        payload = {"UserName":username, "Password":password, "RememberMe":False}
        authpath = 'auth/handshake'
        r = self._wb_post(authpath, payload)
        return r

    def jobs(self, keyfigures=False, jobids=[]):
        """Get a LIST of all the jobs in workbook as a DICT"""
        #https://freewheel.workbook.net/api/json/metadata?op=JobsRequest
        if keyfigures:
            endpoint = "json/reply/JobKeyFigureVisualizationRequest[]"
            if jobids:
                r = self._wb_postget(endpoint,jobids)
            else:
                r = self._wb_get(endpoint)

        else:
            endpoint = "jobs"
            r = self._wb_get(endpoint)
        return r

    def customers(self):
        authpath = "resource/customers"
        r = self._wb_get(authpath)
        return r

    def projects(self):
        endpoint = "projects"
        r = self._wb_get(endpoint)
        return r

    def employees(self):
        authpath = "resource/employees"
        r = self._wb_get(authpath)
        return r

    def teams(self):
        authpath = "resource/teams"
        r = self._wb_get(authpath)
        return r

    def teamresources(self, resourceids):
        authpath = "resource/team/resources"
        payload = {"ResourceIds":resourceids}
        r = self._wb_post(authpath, payload)
        return r

    def teamvisualization(self, resourceids):
        authpath = 'setup/teams/visualization/setup'
        payload = {"ResourceIds":resourceids}
        r = self._wb_post(authpath, payload)
        return r
    
    def departments(self):
        authpath = "core/departments"
        r = self._wb_get(authpath)
        return r

    def jobtypes(self):
        authpath = "settings/job/types"
        r = self._wb_get(authpath)
        return r

    def raw_time(self, start_date=None, end_date=None):
        """Get all the Raw Time Entries in WB - BIG QUERY"""
        #https://freewheel.workbook.net/api/json/metadata?op=RawTimeEntriesRequest
        endpoint = 	'personalexpense/timeentries/raw'
        args = {}
        if start_date is not None:
            args['Start'] = start_date
        if end_date is not None:
            args['End'] = end_date
        r = self._wb_get(endpoint,args)
        return r
    
    def dimensions(self):
        endpoint = "dimensions"
        r = self._wb_get(endpoint)
        return r
    
    def dimension_details(self):
        endpoint = 'settings/dimensions/details'
        return self._wb_get(endpoint)
    
    def projects(self):
        endpoint = 'Projects'
        return self._wb_get(endpoint)
    

    def task_matrix(self, interval, showtype, resourceids):
        endpoint = "schedule/visualization/taskmatrix"
        #this probably wont work without a list of resourceids
        # Intervalto see data in, if show type is 1 and interval is 7, we will see for 7 days
        #ShowType 1 = days, 2 = weeks and 3 = months
        payload = {"ResourceIds":resourceids, "Interval":interval, "ShowType":showtype}
        r = self._wb_post(endpoint, payload)

        tasklist = []
        #We're getting the table returned, but we need to make a new row for each taskdetails
        for task in r:
            taskdetails = task['Details']
            task.pop('Details',None)
            for tasktime in taskdetails:
                tasktime.pop('ResourceId',None)
                tasktime.pop('TaskId',None)
                tasktime.update(task)
                tasklist.append(tasktime)
            
        
        return tasklist
    
    def employee_positions(self):
        endpoint = "resource/employee/positions"
        return self._wb_get(endpoint)


    def segments(self):
        endpoint = "/settings/dimensions/segment"
        return self._wb_get(endpoint)

    def _wb_get(self, endpoint, args={}):
        if args:
            print(f"There were arguments:{args}")
            r = self.session.get(url=f"{self.workbookpath}{endpoint}",params=args)
        else:
            r = self.session.get(f"{self.workbookpath}{endpoint}")
        return r.json()



    def _wb_post(self, endpoint, payload):
        r = self.session.post(f"{self.workbookpath}{endpoint}",json=payload)
        return r.json()
    
    def _wb_postget(self, endpoint, payload):
        """This uses a POST but it tells the API that we are trying to GET"""
        headers = {'X-HTTP-Method-Override':'GET'}
        r = self.session.post(f"{self.workbookpath}{endpoint}",json=payload, headers=headers)
        return r.json()
    
