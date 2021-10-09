from django.db import models
import uuid


# Create your models here.

class Report(models.Model):
    title = models.CharField(max_length=255)
    report_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    file = models.FileField(upload_to="media/")
    description = models.TextField(null = True , blank = True)

    def __str__(self) -> str:
        return self.title+ "   "+ self.description

    def serialize(self):
        file =self.file
        return {
            "title" : self.title,
            "report_id" : self.report_id,
            "file" : str(file),
            "description" : self.description
        }
    


    