from django.db import models


# Create your models here.

class Master(models.Model):
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100, unique=True)
    port = models.IntegerField()
    token = models.CharField(max_length=100)
    env = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.ip


class Minion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip = models.TextField(default='none')
    kernel = models.CharField(max_length=100, blank=True)
    # accept_status=models.BooleanField(default=False)
    master = models.ManyToManyField(Master)

    def __unicode__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    salt_name = models.CharField(max_length=100)
    wmi_name = models.CharField(max_length=100, blank=True)
    ansible_name = models.CharField(max_length=100, blank=True)
    private_status = models.BooleanField(default=True, db_index=True)
    describe = models.TextField(default='it is a lazy boy,he did nothing')

    def __unicode__(self):
        return self.name


class Log(models.Model):
    host = models.CharField(max_length=100, db_index=True)
    module = models.CharField(max_length=100)
    arg = models.TextField(blank=True)
    action = models.CharField(max_length=100)
    result = models.TextField(default='no result')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.host

    class Meta:
        ordering = ['-created_date']
