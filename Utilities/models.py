from django.db import models
import uuid
from accounts.models import Profile
from medbackend.settings import BASE_DIR, MEDIA_ROOT
from django.core.files.storage import FileSystemStorage


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
        path = str(BASE_DIR) +str(self.file)
        fs=FileSystemStorage()
        path = path.replace("/","\\")
        fs.delete(path)
        super().delete(*args, **kwargs)
    


    