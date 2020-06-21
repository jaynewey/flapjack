import pygame


class TileMap:

    map_dict_format = {
        "chunks": {},  # "x,y": {"layers": []}
        "chunk_size": [],  # [width, height]
        "tile_size": [],  # [width, height]
    }

    def __init__(self, map_dict, tileset, tile_properties={}, colorkey=None):
        self.tileset = tileset
        self.tile_properties = tile_properties

        self.map_dict = map_dict
        self.chunks = map_dict["chunks"]
        self.chunk_width, self.chunk_height = map_dict["chunk_size"]
        self.colorkey = colorkey

        self.tile_width, self.tile_height = map_dict["tile_size"]

        self.chunk_surfaces = {chunk: self._render_chunk(chunk) for chunk in self.chunks.keys()}

    def _render_chunk(self, chunk):
        """Returns a list of rendered layer surfaces for this chunk.

        :param chunk: The chunk key
        :type chunk: str
        :return: The rendered layers of the chunk
        :rtype: list
        """
        return [self._render_layer(layer) for layer in self.chunks[chunk]["layers"]]

    def _render_layer(self, layer):
        """Renders a chunk layer onto a surface.

        :param layer: The chunk layer you want to render
        :type layer: list
        :return: The rendered chunk surface
        :rtype: pygame.Surface
        """
        surface = pygame.Surface((self.tile_width * self.chunk_width, self.tile_height * self.chunk_height))
        print(layer)
        for y in range(self.chunk_height):
            for x in range(self.chunk_width):
                tile_id = str(layer[y][x])
                if tile_id in self.tile_properties.keys():
                    tile_texture = self.get_tile_texture(tile_id)
                    surface.blit(tile_texture, (x * self.tile_width, y * self.tile_height))
        if self.colorkey is not None:
            surface.set_colorkey(self.colorkey)
        return surface

    def _get_tile_data_at(self, layer, x, y):
        """Gets the tile at the x,y coordinate in the chunk given.
        An empty dict if the tile isn't a recognised id e.g no tile at that location (usually denoted by -1).

        :param layer: The list of tile ids
        :type layer: list
        :param x: The x coordinate of the tile you want
        :type x: int
        :param y: The y coordinate of the tile you want
        :type y: int
        :return: The tile at the coordinate
        :rtype: dict
        """
        tile_id = str(layer[y][x])
        return self.tile_properties[tile_id] if tile_id in self.tile_properties.keys() else {}

    def get_tile_texture(self, tile_id):
        """Gets the tile surface by id from the tileset.

        :param tile_id: The id of the tile.
        :return: The tile surface.
        :rtype: pygame.Surface
        """
        tile_id = int(tile_id)
        column, row = tile_id % self.tile_width, tile_id // self.tile_height
        region = pygame.Rect(column * self.tile_width, row * self.tile_height, self.tile_width, self.tile_height)
        return self.tileset.subsurface(region)

    def get_overlapping_tiles(self, rect, layer_index=0, properties=()):
        """Get all the tiles that overlap the given rect that have the given properties set to true.
        Gets any overlapping tiles if no properties are specified.

        :param rect: The rectangle you want to check overlapping for
        :type rect: pygame.Rect
        :param layer_index: The index of the layer you want to get the overlapping tiles on. Bottom layer by default.
        :type layer_index: int
        :param properties: A list of properties that the tiles must declare to be true
        :type properties: tuple
        :return: A list of overlapping tile rectangles
        :rtype: list
        """
        overlapping_tiles = []
        for x, y in (rect.topleft, rect.topright, rect.bottomleft, rect.bottomright):
            chunk_x, chunk_y = self.get_chunk_at_position((x, y))
            chunk = str(chunk_x) + "," + str(chunk_y)
            real_chunk_x = self.chunk_width * self.tile_width * chunk_x
            real_chunk_y = self.chunk_height * self.tile_height * chunk_y
            relative_x = (x - real_chunk_x) // self.tile_width
            relative_y = (y - real_chunk_y) // self.tile_height
            if chunk in self.chunks.keys():
                layer = self.chunks[chunk]["layers"][layer_index]
                tile = self._get_tile_data_at(layer, relative_x, relative_y)
                if all(tile[p] if p in tile.keys() else False for p in properties):
                    overlapping_tiles.append(pygame.Rect(real_chunk_x + relative_x * self.tile_width,
                                                         real_chunk_y + relative_y * self.tile_height,
                                                         self.tile_width,
                                                         self.tile_height))
        return overlapping_tiles

    def get_chunk_at_position(self, position):
        """Gets the coordinate pair referencing the chunk location in the map that the position is inside.

        :param position: The position you want to find the chunk for
        :type position: tuple
        :return: The chunk that the position is inside
        :rtype: tuple
        """
        x, y = position
        return x // self.tile_width // self.chunk_width, y // self.tile_height // self.chunk_height

    def get_chunk_position(self, chunk):
        """Gets the real position of the top left corner of the chunk

        :param chunk: The chunk key
        :type chunk: str
        :return: The position of the top left corner of the chunk
        :rtype: tuple
        """
        chunk_x, chunk_y = (int(i) for i in chunk.split(","))
        return self.chunk_width * self.tile_width * chunk_x, self.chunk_height * self.tile_height * chunk_y

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
        return TileMap(map_dict, texture_atlas, tiles)
