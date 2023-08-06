from flask_mongoengine import Document
from mongoengine import GenericLazyReferenceField, ReferenceField, ListField, StringField, IntField, DictField, DateTimeField, BooleanField

from app.model.masterdata import DataSourceTypes, ApiTypes, FtpTypes, ScheduleTypes
import datetime
from app.model.user import User
from datetime import timezone
from mongoengine.errors import ValidationError, NotUniqueError , DoesNotExist
import bson
from flask import json,request
from json import dumps
from app.api.business.common import json_serial
import requests
from requests.auth import HTTPBasicAuth
from ftplib import FTP
import pandas as pd

class DataSource(Document):
    title = StringField(required=True)
    dst_id = ReferenceField(DataSourceTypes)
    datacollectiontype = IntField()
    apitype_id = ReferenceField(ApiTypes)
    ftptype_id = ReferenceField(FtpTypes)
    schedule_id = ReferenceField(ScheduleTypes)
    days = ListField()
    daynumber = IntField()
    time = DictField()

    hostname = StringField()
    username = StringField()
    password = StringField()
    path = StringField()
    apikey = StringField()
    dsfields = ListField()
    data = ListField()
    created = DateTimeField(default=datetime.datetime.now(timezone.utc))
    updated = DateTimeField(default=datetime.datetime.now(timezone.utc))
    lastrun = DateTimeField(default=datetime.datetime.now(timezone.utc))
    status = BooleanField(default=True)
    created_by = ReferenceField(User)
    def __str__(self):
        return str(self.id)
    
    
    def add_item(self,source_data):
        try:
            returnData ={
                            "message":'',
                            "error":'',
                            "result":{
                            "message":'',
                            "data":None
                            },
                            "response_status":200
                            }
            if 'editid' in source_data and source_data['editid']!=None:
                item = self.objects.get(id=source_data['editid'])
                item.title = source_data['title']
                dstid = source_data['dst_id']
                item.days= source_data['days']
                item.datacollectiontype= source_data['datacollectiontype']
                item.daynumber= source_data['daynumber']
                item.time= source_data['time']
                if 'schedule_id' in item and source_data['schedule_id']!=0:
                    item.schedule_id= source_data['schedule_id']
                item.dsfields= source_data['dsfields']
                item.path= source_data['path']
                if 'ftptype_id' in source_data and source_data['ftptype_id']!=None and source_data['schedule_id']!=0:
                    item.ftptype_id= FtpTypes.objects(id=source_data['ftptype_id']).first()
                if 'apitype_id' in source_data and source_data['apitype_id']!=None and source_data['schedule_id']!=0:
                    item.apitype_id= ApiTypes.objects(id=source_data['apitype_id']).first()
                if 'schedule_id' in source_data and source_data['schedule_id']!=None and source_data['schedule_id']!=0:
                    item.schedule_id= ScheduleTypes.objects(id=source_data['schedule_id']).first()
                
                item.username= source_data['username']
                item.password= source_data['password']
                item.apikey= source_data['apikey']
                item.title= source_data['title']
                item.hostname= source_data['hostname']
                item.dst_id= source_data['dst_id']
                item.dst_id = DataSourceTypes.objects(id=dstid).first()
                item.lastrun = datetime.datetime.utcnow()
                item.save()
            else:
                if 'editid' in source_data:
                    del source_data['editid']
                item = self(**source_data)
                dstid = source_data['dst_id']
                item.dst_id = DataSourceTypes.objects(id=dstid).first()
                item.lastrun = datetime.datetime.utcnow()
                item.save()
            returnData['result'] = item
            
            #return jsonify({"result": item})
        except ValidationError as e:
            returnData['error'] = 'Provide all required fields'
            returnData['message'] = e.message
            returnData['response_status'] = 500
            #return jsonify({"error": "Provide all required fields","message": e.message }), 500
        return returnData
    
    
    def get_details(self):
        try:
            body =  request.get_json()
            returnData ={
                            "message":'',
                            "error":'',
                            "result":{
                            "message":'',
                            "data":None
                            },
                            "response_status":200
                            }
            if '_id' not in body:
               returnData['result']['messag']='_id is required'
               
               
               #return jsonify({"result": { "message":"_id is required"}})
            
            page = 1
            perpage = 25
            if 'page' in body and body.get('page')>0:
                page = body.get('page')
            
                
            if 'perpage' in body and body.get('perpage') >0:
                perpage = body.get('perpage')   
            pipeline = [
                {
                '$match':{
                         '_id': bson.ObjectId(body.get('_id'))
                    }
                },
               {
                    '$lookup':
                    {
                        'from': "data_source_types",
                        'localField': "dst_id",
                        'foreignField': "_id",
                        'as': "DstDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$DstDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },{
                    '$lookup':
                    {
                        'from': "api_types",
                        'localField': "apitype_id",
                        'foreignField': "_id",
                        'as': "APITypeDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$APITypeDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },{
                    '$lookup':
                    {
                        'from': "ftp_types",
                        'localField': "ftptype_id",
                        'foreignField': "_id",
                        'as': "FTPTypeDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$FTPTypeDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                {
                    '$lookup':
                    {
                        'from': "user",
                        'localField': "created_by",
                        'foreignField': "_id",
                        'as': "UserDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$UserDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                {
                    '$lookup':
                    {
                        'from': "schedule_types",
                        'localField': "schedule_id",
                        'foreignField': "_id",
                        'as': "ScheduleDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$ScheduleDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                }
                
            ]
            pagination={
                        "$facet": {
                            "totalCount": [
                                {
                                    "$count": 'count'
                                }
                            ],
                            "docs": [{
                                "$skip": ((page - 1) * perpage)
                            },
                            {
                                "$limit": perpage
                            }]
                        }
                    }
            #pipeline.append(pagination)
            result = list(self.objects().aggregate(*pipeline))
            """Need to find best way to handle below to make common for all aggregations"""
            returnData['result'] =  dumps(result,default=lambda o:str(o))
            #//return jsonify({"result": dumps(result, default=lambda o: str(o))})
            #return jsonify({"result": pipeline})
        #Response(dumps(aresult, default=json_serial),  mimetype='application/json')
        except ValidationError as e:
            returnData['result']['message'] ='Provide all required fields'
            returnData['error']=str(e)
            returnData['response_status']=500

            #return jsonify({"result":{'message':"Provide all required fields" ,"error": str(e)} }), 500
        except DoesNotExist as e:
            returnData['result']['message'] = 'DataSource details are not found.'
            returnData['error'] = str(e)
            returnData['response_status'] = 500
            #return jsonify({"result":{"message": "DataSource details are not found.","error": str(e) }}), 500
        return returnData
    
    def run_data(self):
        try:
            body = request.get_json()
            returnData ={
                            "message":'',
                            "result":{
                            "error":'',
                            "message":'',
                            "data":None
                            },
                            "response_status":200
                            }
            
            datasourceItem = self.objects.get(id=body.get('_id'))
            if datasourceItem :
                datasourceItem.lastrun = datetime.datetime.utcnow()
                datasourceItem.updated = datetime.datetime.utcnow()
                print(datasourceItem)
                datasourceItem.save()
                msg = "Data Collection started successfully."
                returnData['result']['message'] = msg
                
                #return jsonify({"result":{"message":msg} })
            else:
                returnData['result']['message'] = 'Something went wrong.'
                #return jsonify({"result": {"message":"Something went wrong"}})                                
        except Exception as e:
            print(type(e))
            returnData['result']['error']= str(e)
            returnData['result']['message'] = "Something went wrong"
            returnData['response_status'] = 500
            #return jsonify({"result":{"error":str(e) ,"message":"Something went wrong" } }), 500
        return returnData
    
    def change_status(self):
        try:
            body = request.get_json()
            returnData ={
                            "message":'',
                            "result":{
                            "error":'',
                            "message":'',
                            "data":None
                            },
                            "response_status":200
                            }
            
            datasourceItem = self.objects.get(id=body.get('_id'))
            if datasourceItem and body.get('status'):
                datasourceItem.status = True   
                datasourceItem.updated = datetime.datetime.utcnow()
                msg = "Data Source is Activated successfully."
                datasourceItem.save()
                returnData['result']['message']=msg
                #return jsonify({"result":{"message":msg} })
            elif datasourceItem and body.get('status') == False:
                datasourceItem.status = False   
                datasourceItem.updated = datetime.datetime.utcnow()
                msg = "Data Source is Inactivated successfully."
                datasourceItem.save()
                returnData['result']['message']=msg
                #return jsonify({"result":{"message":msg} })
            else:
                returnData['result']['message']="Something went wrong."
                #return jsonify({"result": {"message":"Something went wrong"}})                                
        except Exception as e:
            print(type(e))
            returnData['result']['message'] ="Something went wrong."
            returnData['result']['error'] = str(e)
            returnData['response_status'] = 500
            #return jsonify({"result":{"error":str(e) ,"message":"Something went wrong" } }), 500
        return returnData
    
    def list_items(self):
        try:
            body = request.get_json()
            returnData ={
                            "message":'',
                            "error":'',
                            "result":{
                            "message":'',
                            "data":None
                            },
                            "response_status":200
                            }
            
            matchppipeline=[]
            
            page = 1
            perpage = 25
            status =[True]
            if 'page' in body and body.get('page')>0:
                page = body.get('page')
            if 'perpage' in body and body.get('perpage') >0:
                perpage = body.get('perpage')
            sorting = {
                        'updated': -1
                    }
           
            if "sortBy" in body:
                sorting = body.get('sortBy')     
            if 'title' in body and body['title']!= None:
                title ={'$regex' :  body['title'], '$options' : 'i'}
                title ={'$regex' :  '(\s+'+body['title']+'|^'+body['title']+')', '$options' : 'i'}
                matchppipeline = [{
                    '$match':{
                        'title': title 
                    }  
                }]
            if 'statusId' in body :
               
               q ={
                    "$match":{
                         'dst_id':{"$in":body.get('statusId')}
                    }
                }
            matchppipeline.append(q)     
            pipeline = [
                {
                   '$sort':{
                       '_id':-1
                   }  
                },
                {
                    '$lookup':
                    {
                        'from': "data_source_types",
                        'localField': "dst_id",
                        'foreignField': "_id",
                        'as': "DstDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$DstDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },{
                    '$lookup':
                    {
                        'from': "api_types",
                        'localField': "apitype_id",
                        'foreignField': "_id",
                        'as': "APITypeDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$APITypeDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },{
                    '$lookup':
                    {
                        'from': "ftp_types",
                        'localField': "ftptype_id",
                        'foreignField': "_id",
                        'as': "FTPTypeDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$FTPTypeDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                {
                    '$lookup':
                    {
                        'from': "user",
                        'localField': "created_by",
                        'foreignField': "_id",
                        'as': "UserDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$UserDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                {
                    '$lookup':
                    {
                        'from': "schedule_types",
                        'localField': "schedule_id",
                        'foreignField': "_id",
                        'as': "ScheduleDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$ScheduleDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                
                {
                    '$sort': sorting
                },
                {
                        "$facet": {
                            "totalCount": [
                                {
                                    "$count": 'count'
                                }
                            ],
                            "docs": [{
                                "$skip": ((page - 1) * perpage)
                            },
                            {
                                "$limit": perpage
                            }]
                        }
                    }
            ]
            finalpipe = matchppipeline+pipeline
            result = list(self.objects().aggregate(*finalpipe))
            """Need to find best way to handle below to make common for all aggregations"""
            returnData['result'] = dumps(result,default= json_serial)
            #//return jsonify({"result": dumps(result, default=json_serial)})
        #Response(dumps(aresult, default=json_serial),  mimetype='application/json')
        except ValidationError as e:
            returnData['message']=e.message
            returnData['error']="Error retrieving the list" 
            returnData['response_status']=500 
            #return jsonify({"error": "Error retrieving the list","message": e.message }), 500
        return returnData

    def test_connection(postdata):
        try:
            returnData ={
                            "message":'',
                            "error":'',
                            
                            "result":{
                            "message":'',
                            "data":None
                            },
                            "response_status":200
                            }
            if postdata["connection_type"]=="API":
                if ('hostname' in postdata and postdata["hostname"]!="") and ('apikey' in postdata and postdata["apikey"]!=""):
                    response = requests.get(postdata["hostname"], auth = HTTPBasicAuth('apikey', postdata["apikey"]))
                    if response.status_code != 200:
                        returnData['error']= "Unable to connect API. Enter valid details"
                        returnData['response_status'] = 500
                        return returnData

                        #return jsonify({"error": "Unable to connect API. Enter valid details" }), 500
                    data = response.text
                    parse_json = json.loads(data)
                    if 'path' in postdata:
                        parse_json=parse_json[postdata['path']]
                        
                    #return jsonify({"result": parse_json})
                    returnData["result"]= parse_json
                    return returnData
                elif ('hostname' in postdata and postdata["hostname"]!="") and ('username' in postdata and postdata["username"]!="") and ('password' in postdata and postdata["password"]!=""):
                    response = requests.get(postdata["hostname"], auth = HTTPBasicAuth(postdata["username"], postdata["password"]))
                    if response.status_code != 200:
                        logger.error("Unable to connect API.")  
                        returnData["error"]="Unable to connect API. Enter valid details"
                        returnData["response_status"] = 500
                        return returnData
                        #return jsonify({"error": "Unable to connect API. Enter valid details" }), 500
                    data = response.text
                    parse_json = json.loads(data)
                    if 'path' in postdata:
                        parse_json=parse_json[postdata['path']]
                    returnData['result'] = parse_json
                    return returnData
                    #return jsonify({"result": parse_json})
                elif ('hostname' in postdata and postdata["hostname"]!=""):
                    response = requests.get(postdata["hostname"], auth = HTTPBasicAuth('apikey', postdata["apikey"]))
                    if response.status_code != 200:
                        returnData["error"] = "Unable to connect API. Enter valid details."
                        returnData['response_status'] = 500
                        return returnData
                        #return jsonify({"error": "Unable to connect API. Enter valid details" }), 500
                    data = response.text
                    parse_json = json.loads(data)
                    if 'path' in postdata:
                        parse_json=parse_json[postdata['path']]
                    returnData['result'] = parse_json
                    return returnData
                    #return jsonify({"result": parse_json})
                
            if postdata["connection_type"]=="FTP":
                if ('hostname' in postdata and postdata["hostname"]!="") and ('username' in postdata and postdata["username"]!="") and ('password' in postdata and postdata["password"]!=""):
                    timeout = 15
                    ftp = FTP(postdata["hostname"], timeout=timeout)
                    try:
                        ftp.login(user=postdata["username"], passwd = postdata["password"])
                        ftp.cwd(postdata["path"])
                        names = []
                        for filename in ftp.nlst():
                            exts = ['.csv', '.xlsx']
                            if any(ext in filename for ext in exts):
                                names.append(filename)
                        latest_name=names[0]
                        with open("myfile.xlsx", "wb") as f:
                            ftp.retrbinary(f"RETR {latest_name}", f.write)
                        data_file = pd.read_csv("myfile.xlsx")
                        parse_json = json.loads(data_file.to_json(orient='records'))
                        returnData['result']= parse_json
                        #return jsonify({"result": parse_json })
                    except Exception as e:
                        print(e)
                        returnData['error']="Unable to connect FTP. Enter valid details"
                        returnData['response_status'] = 500
                        #return jsonify({"error": "Unable to connect FTP. Enter valid details" }), 500
                    data = response.text
                    parse_json = json.loads(data)
                    returnData['result'] = parse_json
                    return returnData
                    #return jsonify({"result": parse_json})
                elif ('hostname' in postdata and postdata["hostname"]!=""):
                    response = requests.get(postdata["hostname"], auth = HTTPBasicAuth('apikey', postdata["apikey"]))
                    if response.status_code != 200:
                        returnData['error']="Unable to connect API. Enter valid details"
                        returnData['response_status']=500
                        return returnData
                        #return jsonify({"error": "Unable to connect API. Enter valid details" }), 500
                    data = response.text
                    parse_json = json.loads(data)
                    returnData['result']=parse_json
                    return returnData
                    #return jsonify({"result": parse_json})

        except ValidationError as e:
            returnData["error"]="Error retrieving the list"
            returnData["message"] = e.message 
            returnData["response_status"] = 500 
            #return jsonify({"error": "Error retrieving the list","message": e.message }), 500
        return returnData
    


   
    


