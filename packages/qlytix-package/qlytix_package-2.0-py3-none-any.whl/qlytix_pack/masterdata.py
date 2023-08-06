from flask_mongoengine import Document
from mongoengine import ListField, StringField, IntField


class DataSourceTypes(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)
    def __str__(self):
        return(self.id)
    
    def list_items(self,postdata):
        returnData={
            "result":''
        }
        masterdata = postdata['name']
        db = self
        if masterdata == 'DataSourceTypes':
            db = self
        if masterdata == 'APITypes':
            db = ApiTypes
        if masterdata == 'FTPTypes':
            db = FtpTypes
        if masterdata == 'ScheduleTypes':
            db = ScheduleTypes
        if masterdata == 'Roles':
            db = Roles
        result = db.objects()
        returnData['result']= result
        return returnData

class FtpTypes(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)
    
class ApiTypes(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)    
    
class ScheduleTypes(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)    
    

class Roles(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)   