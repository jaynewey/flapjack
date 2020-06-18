import pygame

from .asset_manager import AssetManager
from .texture_region import TextureRegion


class TextureAtlas:
    """Class for storing textures from a spritesheet for easy retrieval with a key"""
    def __init__(self, name, image_filetype=".png"):
        """

        :param name: The name of the atlas you want to load without any file extension. The .json atlas file and the
            spritesheet image file must have the same name.
        :type name: str
        :param image_filetype: The file extension of your spritesheet image. .png by default.
        :type image_filetype: str
        """
        self._spritesheet = pygame.image.load(name + image_filetype)
        self._atlas = AssetManager.load_json(name + ".json")

    def find_region(self, spritename):
        """Find the texture region linked with the name given.

        :param spritename: The name of the sprite in the texture atlas
        :type spritename: str
        :return: The corresponding texture region of the sprite
        :rtype: TextureRegion
        """
        sprite = self._atlas[spritename]
        region = pygame.Rect(sprite["x"],
                             sprite["y"],
                             sprite["width"],
                             sprite["height"])
        return TextureRegion(region, self._spritesheet)
