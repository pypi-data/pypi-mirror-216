"""
examples to get the head of the dataframe
"""
from pprint import pprint

from latviastreetify.resolvers import Language, SteetsAndNeighborhoodsResolver

resolver = SteetsAndNeighborhoodsResolver()
gdf = resolver.get_gdf(language=Language.EN)
pprint(gdf.head())
