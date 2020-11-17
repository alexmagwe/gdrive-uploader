from flask import current_app
# from google.cloud import storage
from apiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
from .. import getuploadpath,getcredspath
import os.path
import mimetypes

SCOPES = ['https://www.googleapis.com/auth/drive.file']
# SERVICE_ACCOUNT_FILE = 'secrets.json'
SERVICE_ACCOUNT_FILE = getcredspath()


class FileUploader:
    MIMETYPES={}
    @staticmethod
    def getcreds():
        creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return creds


    def __init__(self,file,name,urls={},*args,**kwargs):

        self.file=file
        # self.unit=code
        self.name=name
        self.urls=urls
        self.mime=self.getMime()
        self.uploadpath=os.path.join(getuploadpath(),self.name)

    def getMime(self):
        return mimetypes.guess_type(self.name)[0] 

    def driveupload(self,creds):
        drive = build('drive', 'v3', credentials=creds)
        folder_id='1E8IWN4ROK2bICbOvwsc8GZw2bgj96wBy'
        file_metadata = {
            'name': self.name,
            'mimeType': self.mime,
            # 'unit':self.unit,
            'parents': [folder_id]

        }
        media = MediaFileUpload(f'{self.file}',
                                mimetype=self.mime,
                                resumable=True
                                )
        res=drive.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        if (id:=res.get('id')): 
            self.id=id
            return True
        else:
            return False



    def delete_file(self):
        file_path=self.uploadpath
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                print(sys.exec_info()[0])
                return False
        else:
            False
