from django.db import models

class Lead(models.Model):
    first_name = models.CharField(max_lenght=20)
    last_name = models.CharField(max_lenght=20)
    age = model.IntegerField(defaulf=0)