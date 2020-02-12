import click

from scrapping.parser import ParserAuto

@click.command()
@click.argument("city", default="moscow")
@click.option("--car", "-c", multiple=True)
def create_dataset(city, car):
    parser = ParserAuto(city, car)
    parser.return_data()


if __name__ == '__main__':
    create_dataset()
