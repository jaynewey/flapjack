class Animation:
    """Class for tracking animations and their keyframes."""
    def __init__(self, keyframes):
        """

        :param keyframes: A correctly formatted list of keyframes
        :type keyframes: list
        """
        self._current_frame = 0

        self._keyframes = keyframes
        self._keyframe = 0

    def update(self):
        """Updates the animation by a frame.

        :return: True if the animation changed keyframe with this update, false if not
        :rtype: bool
        """
        self._current_frame += 1
        self._current_frame %= self._keyframes[self._keyframe]["frames"]

        if self._current_frame == 0:
            self._keyframe += 1
            self._keyframe %= len(self._keyframes)
            return True
        return False

    def get_current_texture(self):
        return self._keyframes[self._keyframe]["texture"]

    def set_keyframes(self, keyframes):
        self._keyframes = keyframes
        self._keyframe = 0
        self._current_frame = 0
