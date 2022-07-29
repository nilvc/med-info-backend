from django.db import models
import uuid
from accounts.models import Profile
from medbackend.settings import BASE_DIR, MEDIA_ROOT
from django.core.files.storage import FileSystemStorage
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyATmGfiLkh8KAFGeUJnLsRpyqn7W66N2ns",
  "authDomain": "med-info-c0e1c.firebaseapp.com",
  "projectId": "med-info-c0e1c",
  "storageBucket": "med-info-c0e1c.appspot.com",
  "messagingSenderId": "1048853744839",
  "appId": "1:1048853744839:web:35d4bbbff66d6edcf882e2",
  "measurementId": "G-8VVEMKW7WL",
  "databaseURL" : ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

# Create your models here.


class Report(models.Model):
    title = models.CharField(max_length=255)
    report_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    file = models.FileField(upload_to=MEDIA_ROOT)
    description = models.TextField(null = True , blank = True)
    uploaded_by = models.ForeignKey(Profile , on_delete=models.SET_NULL , null=True , default= None)

    def __str__(self) -> str:
        return self.title+ "   "+ self.description

    def serialize(self):
        file =self.file
        uploaded_by = "Not found"
        if self.uploaded_by:
            uploaded_by = self.uploaded_by.first_name + " " + self.uploaded_by.last_name 
        return {
            "title" : self.title,
            "report_id" : self.report_id,
            "file" : str(file),
            "description" : self.description,
            "uploaded_by" : uploaded_by
        }
    
    def delete(self ,*args, **kwargs):
        # print("called delete")
        # print(self.file)
        # storage.child().delete(self.file)
        path = str(BASE_DIR) +str(self.file)
        fs=FileSystemStorage()
        path = path.replace("/","\\")
        fs.delete(path)
        super().delete(*args, **kwargs)
    


    