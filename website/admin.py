from django.contrib import admin
from .models import UserInput
# Register your models here.
@admin.register(UserInput)
class UserInputAdmin(admin.ModelAdmin):
    list_display = ('patient_id', "age","gender", "cp","trtbps","cholestrol","fbs","restecg","thalachh","exng","oldpeak", "slp", "caa", "thall", 'timestamp')
    search_fields = ('patient_id',)
    list_filter = ('timestamp', 'gender')