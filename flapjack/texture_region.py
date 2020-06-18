class TextureRegion:
    """Class for tracking a region of a spritesheet"""
    def __init__(self, rect, spritesheet):
        """

        :param rect: The rectangular region of the sprite within the spritesheet
        :type rect: pygame.Rect
        :param spritesheet: The spritesheet surface
        :type spritesheet: pygame.Surface
        """
        self._region = rect
        self._spritesheet = spritesheet

    def get_surface(self):
        """Gets the sprite represented by this texture region

        :return: The sprite surface of this texture region
        :rtype: pygame.Surface
        """
        return self._spritesheet.subsurface(self._region)

    @property
    def get_region(self):
        """Gets the rectangle of this texture region.

        :return: The rectangle of this texture region
        :rtype: pygame.Rect
        """
        return self._region
