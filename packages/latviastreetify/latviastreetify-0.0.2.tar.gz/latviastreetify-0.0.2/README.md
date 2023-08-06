# latvian_streets_neighborhoods

## install

`pip install latviastreetify`

or with CLI capabilities

`pip install latviastreetify[cli]`

## Usage examples

### Head of the dataframe

```python
from latviastreetify.resolvers import Language, SteetsAndNeighborhoodsResolver
from pprint import pprint

resolver = SteetsAndNeighborhoodsResolver()
gdf = resolver.get_gdf(language=Language.EN)
pprint(gdf.head())
```

```
    Number          X          Y                   Street                         Address                       geometry  index_right     Code    Name
0    2 k-1  24.100255  56.958924          elizabetes iela            elizabetes iela 2k-1  POINT (506097.000 312818.000)         33.0  lvrig34  centrs
1  147 k-3  24.134113  56.972871  krišjāņa valdemāra iela  krišjāņa valdemāra iela 147k-3  POINT (508153.000 314374.000)         50.0  lvrig51   brasa
2  147 k-1  24.134276  56.972457  krišjāņa valdemāra iela  krišjāņa valdemāra iela 147k-1  POINT (508163.000 314328.000)         50.0  lvrig51   brasa
3  147 k-2  24.133452  56.972045  krišjāņa valdemāra iela  krišjāņa valdemāra iela 147k-2  POINT (508113.000 314282.000)         50.0  lvrig51   brasa
4  143 k-3  24.132345  56.970582  krišjāņa valdemāra iela  krišjāņa valdemāra iela 143k-3  POINT (508046.000 314119.000)         50.0  lvrig51   brasa
```

## CLI Usage

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `search-by-address`
* `search-by-code`
* `search-by-name`
* `search-by-number`
* `search-by-street`
* `search-multiple`

## `search-by-address`

**Usage**:

```console
$ search-by-address [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-by-code`

**Usage**:

```console
$ search-by-code [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-by-name`

**Usage**:

```console
$ search-by-name [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-by-number`

**Usage**:

```console
$ search-by-number [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-by-street`

**Usage**:

```console
$ search-by-street [OPTIONS] SEARCH_VALUE
```

**Arguments**:

* `SEARCH_VALUE`: [required]

**Options**:

* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.

## `search-multiple`

**Usage**:

```console
$ search-multiple [OPTIONS]
```

**Options**:

* `--address TEXT`
* `--name TEXT`
* `--street TEXT`
* `--number TEXT`
* `--code TEXT`
* `--language [EN|LAV]`: [default: Language.EN]
* `--help`: Show this message and exit.
