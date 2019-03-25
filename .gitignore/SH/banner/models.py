from __future__ import unicode_literals
from django.db import models
import django.utils.timezone

class Banner(models.Model):
    ip_str = models.CharField(max_length=50, null=True, blank=True, default='')
    #data = models.TextField(null=True, blank=True)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Table_IP_OS(models.Model):
    ip = models.GenericIPAddressField( unpack_ipv4=True, default='')
    os = models.CharField(max_length=50, null=True, blank=True, default='')

    def __str__(self):
        return self.ip

class Table_Port(models.Model):
    ip = models.ForeignKey(Table_IP_OS, on_delete = models.CASCADE)
    port = models.IntegerField(blank=True, default='')
    service = models.CharField(max_length=50, null=True, blank=True, default='')
    banner = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return self.ip.ip + ':' + str(self.port)



class DownloadProof(models.Model):  # Таблица proof - файлов завязанного на порт
    description = models.CharField(max_length=255, blank=True)    
    document = models.FileField(upload_to='documents/proof/')
    port = models.ForeignKey(Table_Port, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True) #default=django.utils.timezone.now
                                                            # preserve_default=False,
        
    def __str__(self):
        return self.description

