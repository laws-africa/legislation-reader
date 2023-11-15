from django.db import models
from django.conf import settings

default_language_code = settings.READER_APP_SETTINGS['DEFAULT_LANGUAGE_CODE']


class Work(models.Model):
    frbr_uri = models.CharField(max_length=512, unique=True)
    title = models.CharField(max_length=512)
    metadata = models.JSONField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title} ({self.frbr_uri})'

    def default_expression(self):
        # first, try to get the latest expression in the default language
        expression = self.expressions.filter(language_code=default_language_code).first()
        # otherwise, get the latest expression in any other language
        if not expression:
            expression = self.expressions.first()

        return expression


class Expression(models.Model):
    # the expression inherits most of its metadata from its work
    work = models.ForeignKey(Work, related_name='expressions', on_delete=models.PROTECT)
    # the expression's FRBR URI is more specific than its work's
    frbr_uri = models.CharField(max_length=512, unique=True)
    # the expression's title may differ from its work's
    title = models.CharField(max_length=512)
    # the expression has a language, date, and content, which its work doesn't have
    language_code = models.CharField(max_length=3)
    date = models.DateField()
    content = models.TextField(null=True, blank=True)
    toc_json = models.JSONField()

    class Meta:
        # latest first
        ordering = ['-date']

    def __str__(self):
        return f'{self.title} ({self.frbr_uri})'


class EnrichmentDataset(models.Model):
    name = models.CharField(max_length=512, unique=True)
    taxonomy = models.JSONField()


class ProvisionEnrichment(models.Model):
    dataset = models.ForeignKey(EnrichmentDataset, related_name='enrichments', on_delete=models.CASCADE)
    work = models.ForeignKey(Work, related_name='enrichments', on_delete=models.CASCADE)
    provision_id = models.CharField(max_length=512)
    taxonomy_topic = models.CharField(max_length=1024)
