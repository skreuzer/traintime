import click
import requests
import pkg_resources
import os
import json
from dotenv import load_dotenv

load_dotenv()

@click.group()
def cli():
    """Next train"""


@cli.command()
def status():
    api_key = os.getenv("MTA_API_KEY")
    headers = {"x-api-key": api_key}
    r = requests.get(
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Flirr-alerts.json",
        headers=headers,
    )
    pretty_json = json.loads(r.text)
    print(json.dumps(pretty_json, indent=2))


@cli.command()
def version():
    version = pkg_resources.get_distribution("traintime").version
    click.echo(version)


if __name__ == "__main__":
    cli()
