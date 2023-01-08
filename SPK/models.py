from django.db import models

class datamhs(models.Model):
     nim            = models.IntegerField(primary_key=True)
     nama           = models.CharField(max_length=100)
     ipk            = models.FloatField(max_length=18.2)
     penghasilan    = models.IntegerField()
     sertifikat     = models.IntegerField()
     tanggungan     = models.IntegerField()
     semester       = models.IntegerField()

class kriteria(models.Model):
     nim  = models.IntegerField(primary_key=True)
     nama = models.CharField(max_length=100)
     C1   = models.FloatField(max_length=18.2)
     C2   = models.FloatField(max_length=18.2)
     C3   = models.FloatField(max_length=18.2)
     C4   = models.FloatField(max_length=18.2)
     C5   = models.FloatField(max_length=18.2)
     
class normalisasi(models.Model):
     nim  = models.IntegerField(primary_key=True)
     nama = models.CharField(max_length=100)
     W1   = models.FloatField(max_length=18.2)
     W2   = models.FloatField(max_length=18.2)
     W3   = models.FloatField(max_length=18.2)
     W4   = models.FloatField(max_length=18.2)
     W5   = models.FloatField(max_length=18.2)

class result(models.Model):
     nim  = models.IntegerField(primary_key=True)
     nama = models.CharField(max_length=100)
     maxresult  = models.FloatField(max_length=4.2)
     
