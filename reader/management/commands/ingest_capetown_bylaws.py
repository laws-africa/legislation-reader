import requests

from django.core.management.base import BaseCommand

from reader.models import Work, Expression


class Command(BaseCommand):
    help = 'Ingest Cape Town By-laws'
    api_url = 'https://api.laws.africa/v3/akn/za-cpt/.json'
    api_token = None

    def add_arguments(self, parser):
        parser.add_argument('api_token', type=str)

    def handle(self, *args, **options):
        self.api_token = options['api_token']
        url = self.api_url

        # handle paginated results
        while url:
            resp = self.call_url_with_token(url).json()

            for result in resp.get('results', {}):
                self.create_work_and_expressions(result)

            url = resp['next']  # this is always present, but may be null

    def create_work_and_expressions(self, data):
        # for each result, create the Work object
        self.stdout.write(self.style.NOTICE(f"Creating or updating a Work for {data['frbr_uri']}"))
        work, new = Work.objects.update_or_create(
            frbr_uri=data['frbr_uri'],
            title=data['title'],
            metadata=data
        )
        self.stdout.write(self.style.NOTICE(f'    Work {"created" if new else "updated"}: {work}'))

        # for each work, create the relevant Expression objects
        for date in data['points_in_time']:
            for expression in date['expressions']:
                self.create_expression(expression, work)

    def create_expression(self, data, work):
        self.stdout.write(self.style.NOTICE(f"Creating or updating an Expression for {data['expression_frbr_uri']}"))
        expression, new = Expression.objects.update_or_create(
            work=work,
            frbr_uri=data['expression_frbr_uri'],
            title=data['title'],
            language_code=data['language'],
            date=data['expression_date'],
            content=self.call_url_with_token(f"{data['url']}.html").content.decode('utf-8'),
            toc_json=self.call_url_with_token(f"{data['url']}/toc.json").json(),
        )
        self.stdout.write(self.style.NOTICE(f'    Expression {"created" if new else "updated"}: {expression}'))

    def call_url_with_token(self, url):
        self.stdout.write(self.style.NOTICE(f'Making a call to: {url}'))
        resp = requests.get(url, headers={'Authorization': f'token {self.api_token}'})
        self.stdout.write(self.style.NOTICE(f'    Response: {resp.status_code}'))
        return resp
