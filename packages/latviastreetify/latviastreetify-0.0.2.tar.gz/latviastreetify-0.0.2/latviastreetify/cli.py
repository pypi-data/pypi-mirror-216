""" module for CLI on latviastreetify
"""

from pprint import pprint

import typer

from latviastreetify.resolvers import Language, SteetsAndNeighborhoodsResolver

app = typer.Typer()


def generate_command(search_column_en, search_column_lav):
    def command(search_value: str, language: Language = Language.EN):
        search_value = search_value.lower()
        sr = SteetsAndNeighborhoodsResolver()
        gdf = sr.get_gdf(language=language)
        match language:
            case Language.EN:
                pprint(gdf[gdf[search_column_en].str.contains(search_value)])
            case Language.LAV | _:
                pprint(gdf[gdf[search_column_lav].str.contains(search_value)])

    return command


SEARCH_COLUMNS = {
    "address": ("Address", "adrese"),
    "name": ("Name", "Name"),
    "street": ("Street", "iela"),
    "number": ("Number", "Nr"),
    "code": ("Code", "Code"),
}

for search_name, (search_column_en, search_column_lav) in SEARCH_COLUMNS.items():
    command = generate_command(search_column_en, search_column_lav)
    app.command(name=f"search-by-{search_name}")(command)


@app.command()
def search_multiple(
    address: str = typer.Option(None),
    name: str = typer.Option(None),
    street: str = typer.Option(None),
    number: str = typer.Option(None),
    code: str = typer.Option(None),
    language: Language = Language.EN,
):
    search_values = {
        "address": address,
        "name": name,
        "street": street,
        "number": number,
        "code": code,
    }

    sr = SteetsAndNeighborhoodsResolver()
    gdf = sr.get_gdf(language=language)
    for search_name, search_value in search_values.items():
        if search_value:
            search_value = search_value.lower()
            match language:
                case Language.EN:
                    gdf = gdf[
                        gdf[SEARCH_COLUMNS[search_name][0]].str.contains(search_value)
                    ]
                case Language.LAV | _:
                    gdf = gdf[
                        gdf[SEARCH_COLUMNS[search_name][1]].str.contains(search_value)
                    ]
    pprint(gdf)


if __name__ == "__main__":
    app()
