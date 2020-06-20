import pygame


class TileMap:
    def __init__(self, tiles, map_dict, texture_atlas):
        self.tiles = tiles
        self.chunks = map_dict["chunks"]
        self.chunk_size = map_dict["chunk_size"]
        self.texture_atlas = texture_atlas

        self.tile_size = map_dict["tile_size"]

        self.chunk_surfaces = {chunk: self._render_chunk(chunk) for chunk in self.chunks}

    def _render_chunk(self, chunk):
        """Renders a whole chunk onto a surface.

        :param chunk: The chunk key
        :type chunk: str
        :return: The rendered chunk surface
        :rtype: pygame.Surface
        """
        surface = pygame.Surface((self.tile_size*self.chunk_size[0], self.tile_size*self.chunk_size[1]))
        chunk_x, chunk_y = (int(i) for i in chunk.split(","))
        for y in range(self.chunk_size[1]):
            for x in range(self.chunk_size[0]):
                tile = self._get_tile_at(chunk, x, y)
                if tile != {}:
                    tile_texture = self.texture_atlas.find_region(tile["texture"]).get_surface()
                    surface.blit(tile_texture, (x*self.tile_size, y*self.tile_size))
        return surface

    def _get_tile_at(self, chunk, x, y):
        """Gets the tile at the x,y coordinate in the chunk given.
        An empty dict if the tile isn't a recognised id e.g no tile at that location (usually denoted by -1).

        :param chunk: The chunk key
        :type chunk: str
        :param x: The x coordinate of the tile you want
        :type x: int
        :param y: The y coordinate of the tile you want
        :type y: int
        :return: The tile at the coordinate
        :rtype: dict
        """
        tile_id = str(self.chunks[chunk][y][x])
        return self.tiles[tile_id] if tile_id in self.tiles.keys() else {}

    def get_overlapping_tiles(self, rect, properties=()):
        """Get all the tiles that overlap the given rect that have the given properties set to true.
        Gets any overlapping tiles if no properties are specified.

        :param rect: The rectangle you want to check overlapping for
        :type rect: pygame.Rect
        :param properties: A list of properties that the tiles must declare to be true
        :type properties: tuple
        :return: A list of overlapping tile rectangles
        :rtype: list
        """
        overlapping_tiles = []
        for x, y in (rect.topleft, rect.topright, rect.bottomleft, rect.bottomright):
            chunk_x, chunk_y = self.get_chunk_at_position((x, y))
            chunk = str(chunk_x) + "," + str(chunk_y)
            real_chunk_x = self.chunk_size[0] * self.tile_size * chunk_x
            real_chunk_y = self.chunk_size[1] * self.tile_size * chunk_y
            relative_x = (x - real_chunk_x) // self.tile_size
            relative_y = (y - real_chunk_y) // self.tile_size
            if chunk in self.chunks.keys():
                tile = self._get_tile_at(chunk, relative_x, relative_y)
                if all(tile[p] if p in tile.keys() else False for p in properties):
                    overlapping_tiles.append(pygame.Rect(real_chunk_x + relative_x * self.tile_size,
                                                         real_chunk_y + relative_y * self.tile_size,
                                                         self.tile_size,
                                                         self.tile_size))
        return overlapping_tiles

    def get_chunk_at_position(self, position):
        """Gets the coordinate pair referencing the chunk location in the map that the position is inside.

        :param position: The position you want to find the chunk for
        :type position: tuple
        :return: The chunk that the position is inside
        :rtype: tuple
        """
        x, y = position
        return x // self.tile_size // self.chunk_size[0], y // self.tile_size // self.chunk_size[1]

    def get_chunk_position(self, chunk):
        """Gets the real position of the top left corner of the chunk

        :param chunk: The chunk key
        :type chunk: str
        :return: The position of the top left corner of the chunk
        :rtype: tuple
        """
        chunk_x, chunk_y = (int(i) for i in chunk.split(","))
        return self.chunk_size[0] * self.tile_size * chunk_x, self.chunk_size[1] * self.tile_size * chunk_y

    @staticmethod
    def load_from_file(tiles_file, map_file, texture_atlas):
        """Creates a TileMap instance from the given correctly formatted files.

        :param tiles_file: The json file containing tile id's and their textures
        :type tiles_file: str
        :param map_file: The json file containing map data
        :type map_file: str
        :param texture_atlas: The texture atlas containing the textures to be used
        :return: The generated tilemap
        :rtype TileMap
        """
        from flapjack.flapjack.asset_manager import AssetManager
        tiles = AssetManager.load_json(tiles_file)
        map_dict = AssetManager.load_json(map_file)
        return TileMap(tiles, map_dict, texture_atlas)

    def export_tiles(self, filename, columns=16):
        rows = len(self.tiles.keys()) // columns + 1
        tilemap = pygame.Surface((self.tile_size * columns, self.tile_size * rows))
        for tile_id, tile_data in self.tiles.items():
            tile_texture = self.texture_atlas.find_region(tile_data).get_surface()
            tilemap.blit(tile_texture, ((tile_id % columns) * self.tile_size, (tile_id // columns) * self.tile_size))
        pygame.image.save(tilemap, filename)
