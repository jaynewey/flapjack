class AssetManager:
    """A handy class for storing any kind of assets such as images, fonts, audio, etc."""

    def __init__(self):
        self.__assets = {}

    def add_asset(self, asset):
        """Adds an already loaded asset into the database.

        :param asset: The asset you want added
        :return: The added asset
        """
        asset_type = type(asset)
        if asset_type in self.__assets.keys():
            self.__assets[asset_type].add(asset)
        else:
            self.__assets[asset_type] = {asset}
        return asset

    def remove_asset(self, asset):
        """Removes a given asset from the database.

        :param asset: The asset you want removed
        :return: The removed asset. None if the asset was not found in the database
        """
        asset_type = type(asset)
        if asset_type in self.__assets.keys():
            return self.__assets[asset_type].discard(asset)
        return None

    def get_assets(self):
        """Returns the loaded assets from the database.

        :return: The assets loaded in this asset manager
        :rtype: dict
        """
        return self.__assets

    def get_assets_by_type(self, asset_type):
        """Returns the set of all assets in the database of a given type.

        :param asset_type: The type of assets you want
        :type asset_type: type
        :return: The set of assets of the given type. An empty set if no assets of that type exist in the database.
        :rtype: set
        """
        return self.__assets[asset_type] if asset_type in self.__assets.keys() else set()

    @staticmethod
    def load_json(filename):
        """Useful method for loading json data to a dict.

        :param filename: The .json file to load
        :return: The json data in dict format
        :rtype: dict
        """
        import json
        filename += "" if filename.endswith(".json") else ".json"
        with open(filename) as json_file:
            json_data = json.load(json_file)
        return json_data

    @staticmethod
    def save_json(dictionary, filename):
        import json
        filename += "" if filename.endswith(".json") else ".json"
        with open(filename, 'w') as json_file:
            json.dump(dictionary, json_file)
