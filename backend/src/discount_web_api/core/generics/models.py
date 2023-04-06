from django.db import models


class TimeStampModel(models.Model):
    created_by = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
