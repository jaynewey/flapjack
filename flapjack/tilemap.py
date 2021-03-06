import pygame

from flapjack.flapjack.animation import Animation


class TileMap:

    map_dict_format = {
        "chunks": {},  # "x,y": {"layers": []}
        "chunk_size": [],  # [width, height]
        "tile_size": [],  # [width, height]
    }

    def __init__(self, map_dict, tileset, tile_properties=None, colorkey=None):
        """Create a new TileMap with the given parameters.

        :param map_dict: The map data in dict form
        :type map_dict: dict
        :param tileset: The tileset image as a pygame Surface
        :type tileset: pygame.Surface
        :param tile_properties: The (optional) properties for tiles in dict form
        :type tile_properties: dict
        :param colorkey: The (optional) colorkey of the tileset for transparent blitting
        :type colorkey: tuple
        """
        self.tileset = tileset
        self.tile_properties = {} if tile_properties is None else tile_properties

        self.map_dict = map_dict
        self.chunks = map_dict["chunks"]
        self.chunk_width, self.chunk_height = map_dict["chunk_size"]
        self.colorkey = colorkey

        self.tile_width, self.tile_height = map_dict["tile_size"]

        self._chunk_surfaces = {}

        self._animations = {}
        for tile_id, properties in self.tile_properties.items():
            if "animation" in properties.keys():
                self._animations[tile_id] = Animation(properties["animation"])

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
        layer_region = (self.tile_width * self.chunk_width, self.tile_height * self.chunk_height)
        if self.colorkey is None:
            surface = pygame.Surface(layer_region, pygame.SRCALPHA)
        else:
            surface = pygame.Surface(layer_region)
            surface.fill(self.colorkey)
            surface.set_colorkey(self.colorkey)

        for y in range(self.chunk_height):
            for x in range(self.chunk_width):
                tile_id = layer[y][x]
                self._render_tile(x, y, tile_id, surface)
        return surface

    def _render_tile(self, x, y, tile_id, surface, remove=False):
        if tile_id >= 0:
            if str(tile_id) in self._animations.keys():
                tile_texture = self.get_tile_texture(self._animations[str(tile_id)].get_current_texture())
            else:
                tile_texture = self.get_tile_texture(tile_id)
            surface.blit(tile_texture, (x * self.tile_width, y * self.tile_height))
        elif remove:
            if self.colorkey is None:
                fill = (0, 0, 0, 0)
            else:
                fill = self.colorkey
            pygame.draw.rect(surface,
                             fill,
                             pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))

    def _render_animated_tiles(self, chunk, layer_index, layer_surface):
        layer = self.chunks[chunk]["layers"][layer_index]
        for y in range(self.chunk_height):
            for x in range(self.chunk_width):
                tile_id = layer[y][x]
                if str(tile_id) in self._animations.keys():
                    self._render_tile(x, y, tile_id, layer_surface)
        return layer_surface

    def get_chunk_surface(self, chunk):
        """Gets a rendered surface of the given chunk.

        :param chunk: The chunk key
        :type chunk: str
        :return: The chunk surface
        :type: pygame.Surface
        """
        if chunk in self._chunk_surfaces.keys():
            for layer_index, layer_surface in enumerate(self._chunk_surfaces[chunk]):
                self._render_animated_tiles(chunk, layer_index, layer_surface)
            return self._chunk_surfaces[chunk]
        else:
            self._chunk_surfaces[chunk] = self._render_chunk(chunk)
            return self._chunk_surfaces[chunk]

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
        columns = self.tileset.get_width() // self.tile_width
        column, row = tile_id % columns, tile_id // columns
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

    def get_chunks_in_region(self, corners):
        """Gets all chunks bounded by the corner coordinates given.

        :param corners: A list of corner coordinates [top_left, top_right, bottom_left, bottom_right]
        :type corners: list
        :return: A list of chunks bounded by the region given
        :rtype: list
        """
        corner_chunks = [self.get_chunk_at_position(corner) for corner in corners]
        region_chunks = []
        for x in range(corner_chunks[0][0], corner_chunks[1][0] + 1):
            for y in range(corner_chunks[0][1], corner_chunks[1][1] + 1):
                if str(x) + "," + str(y) in self.chunks.keys():
                    region_chunks.append((x, y))
        return region_chunks

    def get_chunk_position(self, chunk):
        """Gets the real position of the top left corner of the chunk

        :param chunk: The chunk key
        :type chunk: str
        :return: The position of the top left corner of the chunk
        :rtype: tuple
        """
        chunk_x, chunk_y = (int(i) for i in chunk.split(","))
        return self.chunk_width * self.tile_width * chunk_x, self.chunk_height * self.tile_height * chunk_y

    def set_tile(self, tile_id, chunk, layer_index, position):
        """Sets the tile at the given location, on the given layer, at the given chunk as the tile id given.
        This automatically updates the chunk surfaces of the tilemap.

        :param tile_id: The tile
        :type tile_id: int
        :param chunk: The chunk key
        :type chunk: str
        :param layer_index: The index of the layer you want to set the tile on
        :type layer_index: int
        :param position: The (x, y) location of the tile in the chunk
        :type position tuple
        :return: None
        """
        x, y = position
        self.chunks[chunk]["layers"][layer_index][y][x] = tile_id
        self._render_tile(x, y, tile_id, self._chunk_surfaces[chunk][layer_index], remove=True)

    def update_animations(self):
        """Updates all animated tiles in the tileset.

        :return: None
        """
        for animation in self._animations.values():
            animation.update()
