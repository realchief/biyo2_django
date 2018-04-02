import os
from django.db import models
from django.conf import settings
from storage import InstallerStorage


def upload_to(self):
    return InstallerStorage()


def upload_to_f(instance, filename):
    return settings.STORAGE_ROOT


class ProjectVersion(models.Model):
    version = models.CharField(max_length=10)
    installer = models.FileField(storage=upload_to, upload_to=upload_to_f)
    password = models.CharField(max_length=20)

    def __unicode__(self):
        return u'Project version'

    def save(self, *args, **kwargs):
        for subdir, dirs, files in os.walk(settings.STORAGE_ROOT):
            for file in files:
                os.remove(os.path.join(settings.STORAGE_ROOT, file))
        super(ProjectVersion, self).save(*args, **kwargs)
