from flask_mongoengine import Document
from mongoengine import ReferenceField, ListField,ObjectIdField, StringField, IntField, DictField, DateTimeField, BooleanField, EmailField
from flask_bcrypt import generate_password_hash, check_password_hash
from app.model.masterdata import DataSourceTypes, ApiTypes, FtpTypes, Roles
from app.api.exceptions.common import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, InternalServerError
from mongoengine.errors import ValidationError, NotUniqueError, DoesNotExist
from flask_jwt_extended import create_access_token
from flask import Flask, json, request
from app import config as config
from app.api.services.mailservices import send_email
from app.api.business.common import json_serial ,getTokenDetails
from json import dumps
import secrets
import datetime
import bson
from datetime import timezone
from bson.objectid import ObjectId
#from app.model.basemodel import BaseModel

class UserDetails(Document):
    #_id = ObjectIdField(default=ObjectId, primary_key=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    middle_name = StringField(required=False)
    name = StringField(required=True)
    email = EmailField(required=True,unique=True)
    role_id = IntField()
    status = BooleanField(default=False)
    status_id = IntField(default=0) #0= Created , 1 Active ,2 Deleted
    email_verified = BooleanField(default=False)
    employee_id = StringField(required=False ,unique=True)
    modules = ListField(required=False)
    created_on = DateTimeField(default=datetime.datetime.now(timezone.utc))
    updated_on = DateTimeField(default=datetime.datetime.now(timezone.utc))
    password = StringField(required=False, min_length=8)
    
    def __str__(self):
        return str(self.id)
    
    def generate_name(self):
        self.name = ((self.first_name or '')+' '+(self.middle_name or '')+' '+(self.last_name or '')).replace('  ',' ')
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')

    def check_password(password, spassword):
        return check_password_hash(spassword, password)   
    
    def login(self):
        try:
            body = request.get_json()
            returnData = {
                "message": '',
                "result": {
                    "message": '',
                    "data": None,
                    "error": '',
                    'token':'',
                    'user':'',
                    'role_id':''
                },
                "response_status":200
            }

            userD = self.objects.get(email=body.get('email'))
            
            if userD.status_id ==0:
                returnData["message"] = "The email has not been verified yet"
                returnData["result"]["message"] = "The email has not been verified yet"
                returnData["response_status"] = 500
            elif userD.status_id == 2:
                returnData["message"] = "The account has been deleted"
                returnData["result"]["message"] = "The account has been deleted"
                returnData["response_status"] = 500
            elif userD.status_id ==3:
                returnData["message"] = "Your account is not yet activated or currently inactive"
                returnData["result"]["message"] = "Your account is not yet activated or currently inactive"
                returnData["response_status"] = 500    
            else:
                authorized = self.check_password(body.get('password'),userD.password)
                if not authorized:
                    raise UnauthorizedError
                #milliseconds=1000
                expires = datetime.timedelta(days=1)
                additional_claims ={ "userDetails":userD}
                userD['password']=''
                #userDetaild = dict(userD)
                #userDetaild.pop('password', None)
                access_token = create_access_token(identity=str(userD.id),additional_claims=additional_claims, expires_delta=expires)
                returnData["result"]["token"] = access_token
                returnData["result"]["user"] = userD
                returnData["result"]["role_id"] = userD['role_id']
                returnData["response_status"] = 200
                # return jsonify({"result": {'token':access_token,'user':userD,'role_id':userD['role_id']}}), 200
           
        except ValidationError as e:
            returnData["message"] = "Provide all required fields"
            returnData["result"]["message"] = "Provide all required fields"
            returnData["result"]["error"] = str(e)
            returnData["response_status"] = 500
            # return jsonify({"result":{'message': ,"error": str(e)} }), 500
        except (DoesNotExist):
            returnData["message"] = "Account does not exist"
            returnData["result"]["message"] = "Account does not exist"
            returnData["response_status"] = 500
            # return jsonify({"result":{"message": }}), 500
        except (UnauthorizedError):
            returnData["message"] = "Invalid credentials"
            returnData["result"]["message"] = "Invalid credentials"
            returnData["response_status"] = 500
            # return jsonify({"result":{"message": }}), 500
        except Exception as e:
            returnData["message"] = "Something went wrong"
            returnData["result"]["message"] = "Something went wrong"
            returnData["result"]["error"] = str(e)
            returnData["response_status"] = 500
            # return jsonify({"result":{"message": "Something went wrong","error":str(e)}}), 500
        return returnData

    def set_password(self):
        try:
            body = request.get_json()
            resData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": ''
                },
                "response_status":200
            }
            
            if body['new_password'].__eq__(body['confirm_password']):
                tokenDetails = Token.objects.get(user_id = body.get('user_id'), key = body.get('key'))                                             
                if tokenDetails:
                    if tokenDetails.status ==False:
                        resData["message"] = 'Verification token is already used.'
                        resData["result"]["message"] = 'Verification token is already used.'
                        resData["response_status"] = 500
                        return resData  
                    
                    user = User.objects.get(id=body.get('user_id'))
                    if user:
                        userD = self.objects.get(id=str(user.details_id))
                        if tokenDetails.token_type =='new-user':
                            user.status = True
                            userD.status =True                     
                            user.activate_on = datetime.datetime.utcnow()
                            userD.email_verified = True
                            userD.status_id =1
                            tokenDetails.status = False
                            userD.password = generate_password_hash(body.get('new_password')).decode('utf-8')
                            tokenDetails.updated_on = datetime.datetime.utcnow()
                            resData["message"] = 'Account is activated.'
                            resData["result"]["message"] = 'Account is activated.'
                        if tokenDetails.token_type == 'forget-password':
                            if userD.status_id==0:
                                resData["message"] = 'You are yet to setup the password. Please check your email and setup the password.'
                                resData["result"]["message"] = 'You are yet to setup the password. Please check your email and setup the password.'
                                resData["response_status"] = 500
                            elif userD.status_id==2:
                                resData["message"] = 'Account is either deleted/inactive. Please contact the Administrator for help.'
                                resData["result"]["message"] = 'Account is either deleted/inactive. Please contact the Administrator for help.'
                                resData["response_status"] = 500
                            else:
                                userD.password = generate_password_hash(body.get('new_password')).decode('utf-8')
                                user.status = True
                                userD.status =True                     
                                user.activate_on = datetime.datetime.now(timezone.utc)
                                tokenDetails.status = False
                                tokenDetails.updated_on = datetime.datetime.now(timezone.utc)
                                resData["message"] = 'Password is updated successfully.'
                                resData["result"]["message"] = 'Password is updated successfully.'
                                resData["response_status"] = 200
                        userD.save()
                        user.save()
                        tokenDetails.save()
                    else:
                        resData["message"] = 'user is not found'
                        resData["result"]["message"] = 'user is not found'
                        resData["response_status"] = 500
                else:
                    resData["message"] = 'You login session seems expired. Please login again.'
                    resData["result"]["message"] = 'You login session seems expired. Please login again.'
                    resData["response_status"] = 500
                    # response = {"message":'You login session seems expired. Please login again.' }
            else:
                resData["message"] = 'Make sure new password and confirm password are same.'
                resData["result"]["message"] = 'Make sure new password and confirm password are same.'
                resData["response_status"] = 500
                # response = {"message":'Make sure new password and confirm password are same.'} 
                # return jsonify({"result": response}) ,500
    
        except ValidationError as e:
            resData["message"] = "Provide all required fields"
            resData["result"]["message"] = "Provide all required fields"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            # return jsonify({"result":{'message':"Provide all required fields" ,"error": str(e)} }), 500
            
        except DoesNotExist as e:
            resData["message"] = "Something went wrong"
            resData["result"]["message"] = "Something went wrong DoesNotExist"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            # return jsonify({"result":{'message':"Something went wrong" ,"error": str(e)} }), 500
        except Exception as e:
            resData["message"] = "Something went wrong"
            resData["result"]["message"] = "Something went wrong"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            # return jsonify({"result":{'message':"Something went wrong" ,"error": str(e)} }), 500
        return resData
    
    def forget_password(self):
        try: 
            body = request.get_json()
            resData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": ''
                },
                "response_status":200
            }
            
            userD = self.objects.get(email=body.get('email'))
            if userD:
                if userD.status_id==0:
                    resData["result"]['message'] = "You are yet to setup the password. Please check your email and setup the password."
                    resData["message"] = "You are yet to setup the password. Please check your email and setup the password."
                    resData["response_status"] = 500
                        # response = {"message":'You are yet to setup the password. Please check your email and setup the password.'}
                        # return jsonify({"result": response}) ,500
                elif userD.status_id==2:
                    resData["result"]['message'] = "Account is either deleted/inactive. Please contact the Administrator for help."
                    resData["message"] = "Account is either deleted/inactive. Please contact the Administrator for help."
                    resData["response_status"] = 500
                        # response = {"message":'Account is either deleted/inactive. Please contact the Administrator for help.'}
                        # return jsonify({"result": response}) ,500
                else:
                    user = User.objects.get(details_id=userD['id'])
                    tokenKey = generate_password_hash(secrets.token_urlsafe(8)).decode('utf-8')
                    newToken = Token(user_id=user.id, status = True, key=tokenKey, token_type = "forget-password")
                    newToken.save()
                    button_url=config.FRONT_END_URL+"set-password/"+str(user['id'])+'?key='+tokenKey
                    send_email(subject='Set Password', recipients=[userD['email']], button_url=button_url, text_body=tokenKey, templatePath= "/partial/forgotPassword.html", userDettails=userD)
                    resData["message"] = "An email with the link to reset password has been sent to your registered email account."
                    resData["result"]['message'] = "An email with the link to reset password has been sent to your registered email account."
            else:
                resData['message'] = "Email is not found."  
                resData["result"]['message'] = "Email is not found."
                resData["response_status"] = 500
            # return jsonify({"result": resData})
            
        except ValidationError as e:
            resData["message"] = "Provide all required fields"
            resData["result"]['message'] = "Provide all required fields"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
                # return jsonify({"result":{'message':"Provide all required fields" ,"error": } }), 500
        except DoesNotExist as e:
            resData["message"] = "User details are not found."
            resData["result"]['message'] = "User details are not found."
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
                # return jsonify({"result":{"message": "User details are not found.","error": str(e) }}), 500
        except Exception as e:
            resData["message"] = "Something went wrong"
            resData["result"]['message'] = "Something went wrong"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
                #return jsonify({"result":{"message": "Something went wrong","error": str(e) }}), 500   
        return resData
    
    def add_user(self, source_data):
        try:
            resData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": ''
                },
                "user": None,
                "response_status":200
            }
            tokenData=getTokenDetails(request)
            if not tokenData:
                resData["message"] = "Your access token is invalid."
                resData["result"]['message'] = "Your access token is invalid."
                resData["result"]['error'] = 'Access token error'
                resData["response_status"] = 500
                return resData
                    #return jsonify({"result":{'message':"Your access token is invalid." ,"error": 'Access token error'} }), 500
            elif tokenData['userDetails']['role_id'] !=1:
                resData["message"] = "You do not have access to complete this action."
                resData["result"]['message'] = "You do not have access to complete this action."
                resData["result"]['error'] = 'Permission error'
                resData["response_status"] = 500
                return resData
                    #return jsonify({"result":{'message':"You do not have access to complete this action." ,"error": 'Permission error'} }), 500
            
            password_length = 8
            source_data['password'] = secrets.token_urlsafe(password_length)
            source_data['email_verified'] =False
            
            user_details = self(**source_data)
            user_details.generate_name()
            user_details.hash_password()
            user_details.created_on = datetime.datetime.utcnow()
            user_details.updated_on = datetime.datetime.utcnow()
            user_details.save()
            userinfo = { 'role_id':source_data['role_id'],'details_id':user_details.id}
            user = User(**userinfo)
            
            user.created_on = datetime.datetime.utcnow()
            user.updated_on = datetime.datetime.utcnow()
            user.save()
            expires = datetime.timedelta(days=30)
            tokenKey = create_access_token(identity=str(user.id), expires_delta=expires)
            newToken = Token(user_id=user.id, status = True, key=tokenKey , token_type ='new-user')
            newToken.save()
            #sending mail to new user
            button_url=config.FRONT_END_URL+"set-password/"+str(user['id'])+'?key='+tokenKey
            send_email(subject='Set Password link', recipients=[user_details['email']], button_url=button_url, text_body=tokenKey, templatePath= "/partial/registerNewUser.html" ,userDettails=user_details )
            resData["message"] = "User account is created. An email will be sent with Activation Link."
            resData["result"]['message'] = "User account is created. An email will be sent with Activation Link."
            resData["user"] = user   
            #user details assigned to "user" key
            
            #res = { "message":"User account is created. An email will be sent with Activation Link.","user":user }
            # return jsonify({"result": res})

        except NotUniqueError as e:  
            resData["message"] = " Entered  Email/Employee Id is already in use. Please try with a different."
            resData["result"]['message'] = " Entered  Email/Employee Id is already in use. Please try with a different."
            resData["result"]['error'] = 'Permission error'
            resData["response_status"] = 500
            #return jsonify({"result":{"error": str(e) ,"message":" Entered  Email/Employee Id is already in use. Please try with a different."  }}), 500
        except ValidationError as e:  
            resData["message"] = "Provide all required fields"
            resData["result"]['message'] = "Provide all required fields"
            resData["result"]['error'] = 'Permission error'
            resData["response_status"] = 500
            #return jsonify({"result":{'message':"Provide all required fields" ,"error": str(e)} }), 500
        return resData
    
    def edit_user(self): 
        body = request.get_json()
        try:
            resData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": '',
                    "user": None
                },
                "response_status":200
            }
            user = User.objects.get(id=body.get('user_id'))
            if user:
                userD = self.objects.get(id=user['details_id'])
                userD.first_name = body.get('first_name')
                userD.middle_name = body.get('middle_name')
                userD.last_name = body.get('last_name')
                userD.employee_id = body.get('employee_id')
                userD.modules = body.get('modules')
                userD.updated_on = datetime.datetime.utcnow()
                userD.generate_name()
                userD.save()
                resData["result"] = userD   #userD assigned to "user" key
                #return jsonify({"result": userD})
            else:
                resData["message"] = "Something went wrong"
                resData["result"]['message'] = "Something went wrong"
                    #return jsonify({"result": {"message":"Something went wrong"}})                
                
        except ValidationError as e:
            resData["message"] = "Provide all required fields"
            resData["result"]['message'] = "Provide all required fields"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
                #return jsonify({"result":{'message':"Provide all required fields" ,"error": str(e)} }), 500
                
        except DoesNotExist as e:
            resData["message"] = "User details are not found."
            resData["result"]['message'] = "User details are not found."
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
                #return jsonify({"result":{"message": "User details are not found.","error": str(e)} }), 500
            
        except Exception as e:
            resData["message"] = "Something went wrong"
            resData["result"]['message'] = "Something went wrong"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            
            print(type(e))
                #return jsonify({"result":{"error":str(e) ,"message":"Something went wrong" } }), 500
        return resData
    
    def resend_activationlink(self):
        try:
            resData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": ''
                },
                "response_status":200
            }
            
            tokenData=getTokenDetails(request) #REquest //
            if not tokenData:
                resData["message"] = "Your access token is invalid."
                resData["result"]['message'] = "Your access token is invalid."
                resData["result"]['error'] = 'Access token error'
                resData["response_status"] = 500
                return resData 
                
            elif tokenData['userDetails']['role_id'] !=1:
                resData["message"] = "You do not have access to complete this action."
                resData["result"]['message'] = "You do not have access to complete this action."
                resData["result"]['error'] = 'Permission error'
                resData["response_status"] = 500
                return resData

            body = request.get_json()
            user = User.objects.get(id=body.get('user_id'))
            if user:
                userD = self.objects.get(id=user['details_id'])
                if 'userD' in userD and userD['status_id'] ==1:
                    resData["message"] = "User account is already in active staste."
                    resData["result"]['message'] = "User account is already in active staste."
                elif 'userD' in userD and userD['status_id'] ==2:
                    resData["message"] = "User account is Deleted."
                    resData["result"]['message'] = "User account is Deleted."
                    
                else:     
                    expires = datetime.timedelta(days=30)
                    tokenKey = create_access_token(identity=str(user.id), expires_delta=expires)
                    newToken = Token(user_id=user.id, status = True, key=tokenKey, token_type = "resend-activationlink")
                    newToken.save()
                    button_url=config.FRONT_END_URL+"set-password/"+str(user['id'])+'?key='+tokenKey
                    send_email(subject='Account Activation Link', recipients=[userD['email']], button_url=button_url, text_body='', templatePath= "/partial/resendActivationLink.html" ,userDettails=userD) #Dett -ails
                    resData["message"] = "An email with the link to reset password has been sent to your registered email account."
                    resData["result"]['message'] = "An email with the link to reset password has been sent to your registered email account."          
            else:
                resData["message"] = "Email is not found."
                resData["result"]['message'] = "Email is not found."          
            
        except ValidationError as e:
            resData["message"] = "Provide all required fields"
            resData["result"]['message'] = "Provide all required fields"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            # return jsonify({"result":{'message':"Provide all required fields" ,"error": str(e)} }), 500
        except DoesNotExist as e:
            resData["message"] = "User details are not found."
            resData["result"]['message'] = "User details are not found."
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            # return jsonify({"result":{"message": "User details are not found.","error": str(e) }}), 500
        except Exception as e:
            resData["message"] = "Something went wrong"
            resData["result"]['message'] = "Something went wrong"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            # return jsonify({"result":{"message": "Something went wrong","error": str(e) }}), 500    
            
        return resData
    
    def users_list(self): 
        try:   
            body = request.get_json()
            returnData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": ''
                },
                "user": None,
                "response_status":200
            }
            
            
            matchppipeline=[]  #spell mistake  ppipe
            page = 1
            perpage = 25
            status =[True]
            
            if 'page' in body and body.get('page')>0:
                page = body.get('page')
            
                
            if 'perpage' in body and body.get('perpage') >0:
                perpage = body.get('perpage')
            
            if 'status' in body:
                status = body.get('status')
            
            q ={
                    "$match":{
                         'UserDetails.status_id':{"$in":[1]}
                    }
                }
            
            if 'statusId' in body :
               
               q ={
                    "$match":{
                         'UserDetails.status_id':{"$in":body.get('statusId')}
                    }
                }
            sorting = {
                        'UserDetails.created_on': -1
                    }
            if "sortBy" in body:
             sorting = body.get('sortBy')  
               
            matchppipeline.append(q)   
            if 'title' in body and body['title']!= None:
                title ={'$regex' :  body['title'], '$options' : 'i'}
                title ={'$regex' :  '(\s+'+body['title']+'|^'+body['title']+')', '$options' : 'i'}
                print(title)
                titleQ = {
                        '$match':{                            
                             "$or": [
                                            { 'UserDetails.name': title },
                                            { 'UserDetails.email':title },
                                            
                                     ]                           
                        }  
                    }
                matchppipeline.append(titleQ)
                    
                
                
            pipeline = [
                
                {
                    '$lookup':
                    {
                        'from': "user_details",
                        'localField': "details_id",
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
                        'from': "roles",
                        'localField': "role_id",
                        'foreignField': "_id",
                        'as': "RoleDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$RoleDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                
                {
                    '$sort': sorting
                }
                # {
                #     "$match":{
                #         'UserDetails.status':{"$in":status}
                #     }
                # },
                
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
            finalpipe = pipeline+matchppipeline
            finalpipe.append(pagination)
            result = list(User.objects().aggregate(*finalpipe))   
            
            
            """Need to find best way to handle below to make common for all aggregations"""
            
            returnData['result'] = dumps(result, default=lambda o: str(o))
                #return jsonify({"result": dumps(result, default=lambda o: str(o))})
                #return jsonify({"result": pipeline})
        #Response(dumps(aresult, default=json_serial),  mimetype='application/json')
        
        except ValidationError as e:  
            returnData["message"] = "Provide all required fields"
            returnData["result"]['message'] = "Provide all required fields"
            returnData["result"]['error'] = str(e)
            returnData["response_status"] = 500
            
            # return jsonify({"result":{'message':"Provide all required fields" ,"error": str(e)} }), 500
        
        return returnData
    
    def get_user_details(self):
        try:
            body = request.get_json()
            resData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": ''
                },
                "response_status":200
            }
            
            if 'user_id' not in body:
                resData["message"] = "user id is required"
                resData["result"]['message'] = "user id is required"
                return resData
                #return jsonify({"result": { "message":"user is is required"}})
                
            pipeline = [
                {
                '$match':{
                         '_id': bson.ObjectId(body.get('user_id'))
                    }
                },
                {
                    '$lookup':
                    {
                        'from': "user_details",
                        'localField': "details_id",
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
                        'from': "roles",
                        'localField': "role_id",
                        'foreignField': "_id",
                        'as': "RoleDetails"
                    }
                },
                {
                    '$unwind': {
                        'path': '$RoleDetails',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                
            ]
            
            ##########
            result = list(User.objects().aggregate(*pipeline))
            """Need to find best way to handle below to make common for all aggregations"""
            
            resData['result'] = dumps(result, default=lambda o: str(o))
            #return jsonify({"result": dumps(result, default=lambda o: str(o))})
            #return jsonify({"result": pipeline})
        #Response(dumps(aresult, default=json_serial),  mimetype='application/json')
        
        except ValidationError as e:
            resData["message"] = "Provide all required fields"
            resData["result"]['message'] = "Provide all required fields"
            resData["result"]['error'] = 'Permission error'
            resData["response_status"] = 500  
        except DoesNotExist as e:
            resData["message"] = "User details are not found."
            resData["result"]['message'] = "User details are not found."
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
        return resData
    
    def change_user_status(self): 
        try:
            resData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": ''
                },
                "response_status":200
            }
            
            tokenData=getTokenDetails(request)
            if not tokenData:
                resData["message"] = "Your access token is invalid."
                resData["result"]['message'] = "Your access token is invalid."
                resData["result"]['error'] = 'Access token error'
                resData["response_status"] = 500
                return resData
                    #return jsonify({"result":{'message':"Your access token is invalid." ,"error": 'Access token error'} }), 500
            elif tokenData['userDetails']['role_id'] !=1:
                resData["message"] = "You do not have access to complete this action."
                resData["result"]['message'] = "You do not have access to complete this action."
                resData["result"]['error'] = 'Permission error'
                resData["response_status"] = 500
                    #return jsonify({"result":{'message':"You do not have access to complete this action." ,"error": 'Permission error'} }), 500
                return resData
            
            body = request.get_json()
            user = User.objects.get(id=body.get('user_id'))
            
            if user:
                userD = self.objects.get(id=user['details_id'])
                if userD.status_id == body.get('status_id'):
                    if userD.status_id==1:
                        resData["message"] = "Account is already in active staste."
                        resData["result"]['message'] = "Account is already in active state."
                        return resData
                        #return jsonify({"result":{"message":"Account is already in active staste."} })
                    else:
                        resData["message"] = "Account is already in In-Active staste."
                        resData["result"]['message'] = "Account is already in In-Active state."
                        return resData
                        #return jsonify({"result":{"message":"Account is already in In-Active staste."} })
                
                if body.get('status_id')==3:
                    userD.status = False
                    user.status =False
                    msg = "User account is inactivated successfully."
                    userD.status_id =3
                    resData["message"] = msg
                    resData["result"]['message'] = msg
                elif body.get('status_id')==1:
                    userD.status = True
                    user.status =True
                    userD.status_id =1
                    msg = "User account is activated successfully."
                    resData["message"] = msg
                    resData["result"]['message'] = msg
                else:
                    msg = "Invalid status."
                    resData["message"] = msg
                    resData["result"]['message'] = msg
                    # return jsonify({"result":{"message":msg} })   ###################
                            
                userD.updated_on = datetime.datetime.utcnow()
                userD.generate_name()
                userD.save()
                user.save()
                
                # return jsonify({"result":{"message":msg} })
            else:
                resData["message"] = "Something went wrong"
                resData["result"]["message"] = "Something went wrong"
                #return jsonify({"result": {"message":"Something went wrong"}})                
                
        except ValidationError as e:
            resData["message"] = "Provide all required fields"
            resData["result"]['message'] = "Provide all required fields"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            #return jsonify({"result":{'message':"Provide all required fields" ,"error": str(e)} }), 500
        except DoesNotExist as e:
            resData["message"] = "User details are not found."
            resData["result"]['message'] = "User details are not found."
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            #return jsonify({"result":{"message": "User details are not found.","error": str(e)} }), 500
            
        except Exception as e:
            resData["message"] = "Something went wrong"
            resData["result"]["message"] = "Something went wrong"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            print(type(e))
            #return jsonify({"result":{"error":str(e) ,"message":"Something went wrong" } }), 500
        return resData
    
    def change_password(self):        
        try:
            body = request.get_json()
            resData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": ''
                },
                "response_status":200
            }
            
            if body['new_password'].__eq__(body['confirm_password']):
                user = User.objects.get(id=body.get('user_id'))
                if user:
                    userD = self.objects.get(id=str(user.details_id))
                    userD.password = generate_password_hash(body.get('new_password')).decode('utf-8')
                    userD.status =True
                    userD.status_id =1
                    user.status = True
                    userD.save()
                    user.save()
                    
                    resData["message"] = 'Password updated successfully.'
                    resData["result"]["message"]='Password updated successfully.'
                    resData["response_status"] = 200
                        #response = {"message":'Password updated successfully.'}
                        #return jsonify({"result": response}) ,500
                else:
                    resData["message"] = 'user is not found'     
                    resData["result"]["message"] = 'user is not found'
                    resData["response_status"] = 500
                    #response = {"message":'user in not found'}
                    #return jsonify({"result": response}) ,500
            else:
                resData["message"] = 'Make sure new password and confirm password are same.'
                resData["result"]["message"] = 'Make sure new password and confirm password are same.'
                resData["response_status"] = 500
                #response = {"message":'Make sure new password and confirm password are same.'} 
                #return jsonify({"result": response}) ,500
                
        except ValidationError as e:
            resData["message"] = "Provide all required fields"
            resData["result"]["message"] = "Provide all required fields"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            #return jsonify({"result":{'message':"Provide all required fields" ,"error": str(e)} }), 500
        except DoesNotExist as e:
            resData["message"] = "Something went wrong DoesNotExist"
            resData["result"]["message"] = "Something went wrong"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            #return jsonify({"result":{'message':"Something went wrong" ,"error": str(e)} }), 500
        except Exception as e:
            resData["message"] = "Something went wrong"
            resData["result"]["message"] = "Something went wrong"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            #return jsonify({"result":{'message':"Something went wrong" ,"error": str(e)} }), 500
        return resData
    
class User(Document):
    role_id = ReferenceField(Roles)
    details_id = ReferenceField(UserDetails)
    created_on = DateTimeField(default=datetime.datetime.now(timezone.utc))
    updated_on = DateTimeField(default=datetime.datetime.now(timezone.utc))
    activate_on = DateTimeField(default=datetime.datetime.now(timezone.utc))
    status = BooleanField()
    active = BooleanField()
    status_id = IntField()
    
    def __str__(self):
        return str(self.id)
    
    def delete_user(self): 
        try:
            resData = {
                "message": "",
                "result" :{
                    "message":'',
                    "data": None,
                    "error": ''
                },
                "response_status":200
            }
            
            tokenData=getTokenDetails(request)
            if not tokenData:
                resData["message"] = "Your access token is invalid."
                resData["result"]['message'] = "Your access token is invalid."
                resData["result"]['error'] = 'Access token error'
                resData["response_status"] = 500
                return resData
                        #return jsonify({"result":{'message':"Your access token is invalid." ,"error": 'Access token error'} }), 500
            elif tokenData['userDetails']['role_id'] !=1:
                resData["message"] = "You do not have access to complete this action."
                resData["result"]['message'] = "You do not have access to complete this action."
                resData["result"]['error'] = 'Permission error'
                resData["response_status"] = 500
                return resData
                        #return jsonify({"result":{'message':"You do not have access to complete this action." ,"error": 'Permission error'} }), 500
            
            body = request.get_json()
            user = self.objects.get(id=body.get('user_id'))
            
            if user:
                userD = UserDetails.objects.get(id=user['details_id'])
                print(userD)
                if userD.status_id == 2:
                    resData["message"] = "Account is already Deleted"
                    resData["result"]['message'] = "Account is already Deleted"
                    # return jsonify({"result":{"message":"Account is already Deleted"} })
                    # return resData
                else:
                    userD.status_id = 2
                    msg = "User account is Deleted successfully."
                    userD.updated_on = datetime.datetime.utcnow()
                    userD.generate_name()
                    userD.save()
                    user.save()
                    resData["message"] = msg
                    resData["result"]['message'] = msg
                    # return resData
                    # return jsonify({"result":{"message":msg} })
            else:
                resData["message"] = "Something went wrong"
                resData["result"]["message"] = "Something went wrong"
                #return jsonify({"result": {"message":"Something went wrong"}})                
                
        except ValidationError as e:
            resData["message"] = "Provide all required fields"
            resData["result"]['message'] = "Provide all required fields"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
                #return jsonify({"result":{'message':"Provide all required fields" ,"error": str(e)} }), 500
        except DoesNotExist as e:
            resData["message"] = "User details are not found."
            resData["result"]['message'] = "User details are not found."
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            #return jsonify({"result":{"message": "User details are not found.","error": str(e)} }), 500
            
        except Exception as e:
            resData["message"] = "Something went wrong"
            resData["result"]["message"] = "Something went wrong"
            resData["result"]['error'] = str(e)
            resData["response_status"] = 500
            print(type(e))
        print(resData)
            #return jsonify({"result":{"error":str(e) ,"message":"Something went wrong" } }), 500
        return resData
    

class Token(Document):
    user_id = ReferenceField(User)# From user Schema
    status = BooleanField(default= True)
    key = StringField(required=True, metadata={"description": "Random Key"})
    token_type = StringField(required=True, metadata={"description": "new-user OR forget-password"})
    created_on = DateTimeField(default=datetime.datetime.now(timezone.utc))
    updated_on = DateTimeField(default=datetime.datetime.now(timezone.utc))
    
    def __str__(self):
        return self.key