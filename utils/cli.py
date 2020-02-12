import click

from scrapping.parser import ParserAuto


@click.command()
@click.argument("city")
@click.option("--car", "-c", multiple=True)
def create_dataset(city, car):
    print("hello world")


if __name__ == '__main__':
    create_dataset()
