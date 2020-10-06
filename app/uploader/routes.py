from flask import Flask,request,render_template
import requests
from .fileuploader import FileUploader
from . import uploader
import sys,os
from .. import getuploadpath
def find_file(name):
    api="https://uon-notes-api.herokuapp.com/api/exists"
    data={"name":name}
    resp=requests.post(api,json=data)
    return resp

def savefile(file,code='',toupload=False):
    if toupload:
        path=getuploadpath()
        try:
            path=os.path.join(path,file.filename)
            file.save(path)
            return {'path':path}
            print('saved file')
            print(path)
        except Exception as e:
            print(e)
            return {'error':sys.exc_info()[0]}
    return None
 
@uploader.route('/',methods=['GET'])
def upload_notes():
    return render_template('upload.html')


@uploader.route('/upload',methods=['POST'])
def upload():
    files=request.files.getlist('notes')
    if files:
        creds=FileUploader.getcreds()
        for file in files:
            res=savefile(file,toupload=True)
            if res.get('error'):
                return res,500
            if (path:=res.get('path')):
                obj=FileUploader(path,file.filename)
                exists=find_file(obj.name)
                if exists:
                    continue
                uploaded=obj.driveupload(creds)
                deleted=obj.delete_file()#add logging if file fail to delete
                if uploaded and deleted:
                    return{"name":obj.name,"gid":obj.id}
                  
                else:
                    return {'error':'an error occured try again later'}
    else:
        return {'error':'files no files present'}
    return {'success':'file(s) uploaded succesfully'}
    

