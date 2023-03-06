from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Update at'), auto_now=True)

    class Meta:
        abstract = True


class PersonBase(BaseModel):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    avatar = models.ImageField(upload_to="photos/avatar%Y%m%d/", blank=True, null=True)
    bio = RichTextField(blank=True, null=True)
    job_position = models.CharField(max_length=100, blank=True)
    phone = PhoneNumberField(blank=True)

    class Meta:
        abstract = True
