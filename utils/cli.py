import click

from scrapping.parser import ParserAuto


@click.command()
@click.argument("city", default="moscow")
@click.option("--cars", "-c",
              help="tuple of cars: ('bmw', 'volvo',)"
              # multiple=True
)
@click.option("--amount", "-a", default=370)
def create_dataset(city, cars, amount):
    parser = ParserAuto(city, cars, amount)
    parser.return_data()


if __name__ == '__main__':
    create_dataset()
