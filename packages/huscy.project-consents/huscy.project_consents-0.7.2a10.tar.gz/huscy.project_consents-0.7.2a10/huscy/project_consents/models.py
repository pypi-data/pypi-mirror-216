import uuid

from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from huscy.consents.models import AbstractConsent, AbstractConsentCategory, AbstractConsentFile
from huscy.projects.models import Project
from huscy.subjects.models import Subject


class ProjectConsentCategory(AbstractConsentCategory):
    pass


class ProjectConsentToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectConsent(AbstractConsent):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)


class ContactPerson(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)


def get_project_consent_file_upload_path(instance, filename):
    project_id = instance.consent.project.id
    return f'projects/{project_id}/consents/{filename}'


class ProjectConsentFile(AbstractConsentFile):
    consent = models.ForeignKey(ProjectConsent, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    filehandle = models.FileField(upload_to=get_project_consent_file_upload_path)

    class Meta:
        unique_together = 'consent', 'subject', 'consent_version'
