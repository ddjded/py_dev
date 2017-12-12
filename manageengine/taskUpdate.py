#!/usr/bin/python
# -*- coding: utf-8 -*-
# Replace the serverURL and technicianKey

import requests
import json
import sys
import time

filename = str(sys.argv[1])
with open(filename) as data_file:
    data = json.load(data_file)

requestObj = data['request']

reqID = requestObj['WORKORDERID']
reqSite = requestObj['SITE']
reqTech = requestObj['TECHNICIAN']

# ***********MODIFY BELOW PARAMTERS TO MAKE THIS SCRIPT TO WORK WITH YOUR INSTALLATION***************

serverURL = 'http://servicedesk'  # update servername and portnumber

technicianKey = '0A298BDC-7C0A-4563-9129-E17F6A70F851'  # Replace this with the API Key"

# ***************************************************************************************************

resultjson = {}
found = None
checker = 0

with requests.Session() as s:
    r = s.get(serverURL + '/api/v3/request/' + reqID
              + '/tasks?TECHNICIAN_KEY=' + technicianKey)
			  
    if r.status_code == 200:
        taskData = r.json()
        if taskData['response_status']['status'] != 'failed':
            for i in taskData['tasks']:
                taskID = i['id']
                title = i['title']
                tr = s.get(serverURL + '/api/v3/tasks/' + str(taskID)+'?TECHNICIAN_KEY=' + technicianKey)
                if r.status_code == 200:
                    taskDetailsData = tr.json()
                    description = taskDetailsData['task']['description']
                    if description == None:
                        description = ''
                    for elem in requestObj.keys():
                        if str('$' + elem + '$') in description:
                            description = description.replace('$'
                                    + elem + '$', str(requestObj[elem]))
                            found = True
                        if str('$' + elem + '$') in title:
                            title = title.replace('$' + elem + '$',
                                    str(requestObj[elem]))
                            found = True
                        if 'resource' in requestObj:
                            for resources in requestObj['resource'
                                    ].keys():
                                for questions in requestObj['resource'
                                        ][resources].keys():
                                    if str('$' + questions + '$') \
    in title:
                                        found = True
                                        title = title.replace('$'
        + questions + '$', str(requestObj['resource'
        ][resources][questions][0]))
                                    if str('$' + questions + '$') \
    in description:
                                        found = True
                                        description = \
    description.replace('$' + questions + '$', str(requestObj['resource'
                        ][resources][questions][0]))

                if found:
                    checker += 1
                    taskurl = serverURL + '/api/v3/tasks/' + taskID
                    taskjson = {}
                    taskjson['task'] = []
                    taskinside = {}
                    taskinside['title'] = str(title)
                    taskinside['description'] = str(description)
                    if reqSite != 'Wroclaw':
                        taskinside['owner'] = reqTech
                    taskjson['task'].append(taskinside)
                    jsonData = json.dumps(taskjson)
                    data = {'INPUT_DATA': jsonData}
                    headers = {'technician_key': technicianKey}
                    r = s.put(taskurl, data, headers=headers)
            if checker > 0:
                if r.status_code == 200:
                    resultjson['result'] = 'success'
                    resultjson['message'] = 'Tasks Updated Successfully'
                    print(resultjson)
                else:
                    resultjson['result'] = 'success'
                    resultjson['message'] = 'Unable to update tasks ' \
                        + r.json()
                    print(resultjson)

            if checker == 0:
                resultjson['result'] = 'success'
                resultjson['message'] = 'Nothing to change'
                print(resultjson)
        else:
            resultjson['result'] = 'success'
            resultjson['message'] = 'No tasks to Update'
            print(resultjson)


			
