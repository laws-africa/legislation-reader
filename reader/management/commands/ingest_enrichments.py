import requests

from django.core.management.base import BaseCommand

from reader.models import Work, Expression, EnrichmentDataset, ProvisionEnrichment


class Command(BaseCommand):
    help = 'Ingest Enrichments'
    api_url = 'https://api.laws.africa/v3/enrichment-datasets/1.json'
    api_token = None

    def add_arguments(self, parser):
        parser.add_argument('api_token', type=str)

    def handle(self, *args, **options):
        self.api_token = options['api_token']
        resp = self.call_url_with_token(self.api_url).json()

        self.stdout.write(self.style.NOTICE(f"Creating or updating enrichment dataset {resp['name']}"))
        dataset, new = EnrichmentDataset.objects.update_or_create(
            name=resp['name'],
            taxonomy=resp['taxonomy']
        )

        # clear out existing enrichments
        dataset.enrichments.all().delete()

        # for each enrichment, create the relevant object
        for enrichment in resp['enrichments']:
            work = Work.objects.filter(frbr_uri=enrichment["work"]).first()
            if work:
                self.stdout.write(self.style.NOTICE(f"    Enrichment created for {enrichment['work']} -- {enrichment['provision_id']}"))
                ProvisionEnrichment.objects.create(
                    work=work,
                    dataset=dataset,
                    provision_id=enrichment["provision_id"],
                    taxonomy_topic=enrichment["taxonomy_topic"]
                )
            else:
                self.stdout.write(self.style.WARNING(f"Work does not exist: {enrichment['work']}"))

    def call_url_with_token(self, url):
        self.stdout.write(self.style.NOTICE(f'Making a call to: {url}'))
        resp = requests.get(url, headers={'Authorization': f'token {self.api_token}'})
        resp.raise_for_status()
        self.stdout.write(self.style.NOTICE(f'    Response: {resp.status_code}'))
        return resp
