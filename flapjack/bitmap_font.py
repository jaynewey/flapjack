import pygame


class BitmapFont:
    """Class for loading and rendering bitmap fonts."""
    def __init__(self, font_surface, chars, spacing=1, colorkey=None):
        """

        :param font_surface: A loaded pygame surface with the font's characters
        :type font_surface: pygame.Surface
        :param chars: The characters of the font surface in order
        :type chars: str
        :param colorkey: The (optional) colorkey of the font for transparent blitting
        :type colorkey: tuple
        """
        self._font_surface = font_surface
        self._chars = chars

        self.space_width = 0
        self.spacing = spacing

        char_surfarray = pygame.surfarray.pixels2d(font_surface)
        self.char_height = self._get_char_height(char_surfarray)
        self._char_rects = self._get_char_rects(char_surfarray)

    def _get_char_height(self, char_surfarray):
        height = 0
        separator_colour = char_surfarray[0][0]
        for i, pixel in enumerate(char_surfarray[1][1:]):
            if pixel == separator_colour:
                height = i
                break
        return height

    def _get_char_rects(self, char_surfarray):
        char_rects = {}
        separator_colour = char_surfarray[0][0]
        char_rows = len(char_surfarray[0]) // (self.char_height + 1)
        columns = len(char_surfarray)
        for row in range(1, char_rows * (self.char_height + 1), self.char_height + 1):
            line_queue = []
            for column in range(columns):
                pixel = char_surfarray[column][row]
                if pixel == separator_colour:
                    line_queue = [column] + line_queue
                    if len(line_queue) == 2:
                        x1, x2 = line_queue.pop() + 1, line_queue[0]
                        char_rects[self._chars[len(char_rects.keys())]] = pygame.Rect(x1, row, x2 - x1, self.char_height)
                        self.space_width += (x2 - x1)
        self.space_width //= len(self._chars)
        return char_rects

    def get_char_surface(self, char):
        """Return the surface of a given character.

        :param char: The character to get the surface for
        :type char: str
        :return: The character as a surface. None if the character is not in the font.
        :rtype pygame.Surface
        """
        return self._font_surface.subsurface(self._char_rects[char]) if char in self._char_rects.keys() else None

    def render(self, text, colour):
        """Get a surface with the rendered text on it.

        :param text: The text to be rendered
        :type text: str
        :param colour: The colour of the text
        :type colour: tuple
        :return: The rendered surface
        :rtype: pygame.Surface
        """
        surface = pygame.Surface(self.size(text))
        self.render_on(text, colour, surface, (0, 0))
        return surface

    def render_on(self, text, colour, surface, position):
        """Render the text directly onto a given surface.

        :param text: The string of text to be rendered
        :type text: str
        :param colour: The colour of the text
        :type colour: tuple
        :param surface: The surface to render the text on
        :type surface: pygame.Surface
        :param position: The (x,y) position at which to render the text
        :type position: tuple
        :return: None
        """
        x, y = position
        char_x = 0
        for char in text:
            if char in self._char_rects.keys():
                surface.blit(self.get_char_surface(char), (x + char_x, y + 0))
                char_x += self._char_rects[char].width + self.spacing
            else:
                char_x += self.space_width

    def size(self, text):
        """Determine size of the rendered surface when this text is rendered.

        :param text: The string of text
        :type text: str
        :return: The width, height
        :rtype: tuple
        """
        width, height = self.spacing * (len(text) - 1), self.char_height
        for char in text:
            if char in self._char_rects.keys():
                width += self._char_rects[char].width
            else:
                width += self.space_width
        return width, height
