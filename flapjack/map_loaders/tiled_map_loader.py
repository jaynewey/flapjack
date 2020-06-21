from .map_loader import MapLoader
from ..asset_manager import AssetManager
from ..tilemap import TileMap


class TiledMapLoader(MapLoader):
    @staticmethod
    def load_map_dict(filename):
        source_data = AssetManager.load_json(filename)
        map_dict = TileMap.map_dict_format
        map_dict["tile_size"] = [source_data["tilewidth"], source_data["tileheight"]]
        for layer in source_data["layers"]:
            for chunk in layer["chunks"]:
                chunk_key = str(chunk["x"] // chunk["width"]) + "," + str(chunk["y"] // chunk["height"])
                if chunk_key not in map_dict["chunks"].keys():
                    map_dict["chunks"][chunk_key] = {"layers": []}
                map_dict["chunk_size"] = [chunk["width"], chunk["height"]]
                chunk["data"] = [i - 1 for i in chunk["data"]]
                tiles = [chunk["data"][i:i + chunk["width"]] for i in range(0, len(chunk["data"]), chunk["width"])]
                map_dict["chunks"][chunk_key]["layers"].append(tiles)
        return map_dict

    @staticmethod
    def load_tile_properties(filename):
        source_data = AssetManager.load_json(filename)
        tile_properties = {}
        for tile in source_data["tiles"]:
            if "properties" in tile.keys():
                tile_properties[str(tile["id"])] = {p["name"]: p["value"] for p in tile["properties"]}
        return tile_properties
