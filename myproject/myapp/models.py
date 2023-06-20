from django.db import models

class Reporter(models.Model):
    name = models.CharField(max_length=255)

class BugType(models.Model):
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class SiteName(models.Model):
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    bug_type = models.ForeignKey(BugType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class OwnerName(models.Model):
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    bug_type = models.ForeignKey(BugType, on_delete=models.CASCADE)
    site_name = models.ForeignKey(SiteName, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
