from django.db import models

class AlterField(models.Model):
    nickname = models.CharField(max_length=100)
    is_main = models.BooleanField(default=False)
