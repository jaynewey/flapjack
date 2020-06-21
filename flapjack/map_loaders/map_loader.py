from abc import ABC, abstractmethod

from ..tilemap import TileMap


class MapLoader(ABC):
    """Generic class for loading maps into flapjack from different formats."""

    def load_map(self, filename, tileset, tile_properties=None, colorkey=None):
        """Generates a new map instance from the file given.

        :param filename: The name of the file
        :type filename: str
        :param tileset: The tileset image as a pygame Surface
        :type tileset: pygame.Surface
        :param tile_properties: The (optional) properties for tiles as a filename to be loaded
        :type tile_properties: str
        :param colorkey: The (optional) colorkey of the tileset for transparent blitting
        :type colorkey: tuple
        :return: The generated TileMap
        :rtype TileMap
        """
        map_dict = self.load_map_dict(filename)
        if tile_properties is None:
            tilemap = TileMap(map_dict, tileset, colorkey=colorkey)
        else:
            tilemap = TileMap(map_dict, tileset, self.load_tile_properties(tile_properties), colorkey)
        return tilemap

    @staticmethod
    @abstractmethod
    def load_map_dict(filename):
        """Converts and returns the map data into a formatted dictionary for a TileMap.

        :param filename: The map file you want to load
        :type filename: str
        :return: The map data in dict form
        :rtype: dict
        """
        pass

    @staticmethod
    @abstractmethod
    def load_tile_properties(filename):
        """Converts and returns the tile data into a formatted dictionary for a TileMap.

        :param filename: The tile data file you want to load
        :type filename: str
        :return: The tile data in dict form
        :rtype: dict
        """
        pass
