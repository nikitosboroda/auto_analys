import click

from scrapping.parser import ParserAuto


@click.command()
@click.argument("city", default="moscow")
@click.option("--car", "-c", multiple=True)
@click.option("--amount", "-a", default=370)
def create_dataset(city, car, amount):
    parser = ParserAuto(city, car, amount)
    parser.return_data()


if __name__ == '__main__':
    create_dataset()
