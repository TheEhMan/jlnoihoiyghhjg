from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserInput(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE) # Link to the Django user model
    patient_id = models.CharField(max_length=20, unique=False)
    age = models.IntegerField()
    gender = models.IntegerField()
    cp = models.IntegerField()
    trtbps = models.IntegerField()
    cholestrol = models.IntegerField()
    fbs = models.IntegerField()
    restecg = models.IntegerField()
    thalachh = models.IntegerField()
    exng = models.IntegerField()
    oldpeak = models.IntegerField()
    slp = models.IntegerField()
    caa = models.IntegerField()
    thall = models.IntegerField()
    #risk = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Save the timestamp when the object is created
    def _str_(self):
        return self.patient_id