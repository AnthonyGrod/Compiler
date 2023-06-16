from django.db import models
from datetime import datetime

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Catalog(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def return_nested_objects(self):
        catalogs = Catalog.objects.filter(parent=self)
        files = File.objects.filter(catalog=self)
        return [catalogs, files]
    
    def delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        for catalog in Catalog.objects.filter(parent=self):
            catalog.delete()
        for file in File.objects.filter(catalog=self):
            file.delete()
        self.save()

class File(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)


class SectionStatusData(models.Model):
    info = models.TextField(null=True, blank=True)
    info_start_line = models.IntegerField(null=True, blank=True)
    info_end_line = models.IntegerField(null=True, blank=True)


class Section(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_line = models.IntegerField()
    end_line = models.IntegerField()
    SECTION_TYPE_CHOICES = [
        ('prc', 'PROCEDURE'),
        ('cm', 'COMMENT'),
        ('dir', 'DIRECTIVES'),
        ('dec', 'DECLARATIONS'),
        ('as', 'ASSEMBLY'),
    ]
    SECTION_STATUS_CHOICES = [
        ('ok', 'OK'),
        ('err', 'ERROR'),
        ('warn', 'WARNING'),
    ]
    section_type = models.CharField(max_length=255, choices=SECTION_TYPE_CHOICES, default='prc')
    section_status = models.CharField(max_length=255, choices=SECTION_STATUS_CHOICES, default='ok')
    section_status_data = models.ForeignKey(SectionStatusData, on_delete=models.CASCADE, null=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
