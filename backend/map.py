import json


def get_map_color_mapping():
    """
    Get the color mapping for different AI governance frameworks.

    Returns:
        dict: A dictionary mapping colors to framework names.
            - 'blue': US NIST AI RMF
            - 'violet': Hiroshima Process CoC
    """
    return {"blue": "US NIST AI RMF", "violet": "Hiroshima Process CoC"}


def load_map_data():
    """
    Load mapping data from the map.json file.

    This function reads the mapping information that relates different
    AI governance frameworks to each other.

    Returns:
        dict: The loaded mapping data from the JSON file.

    Raises:
        FileNotFoundError: If the map.json file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    with open("assets/map.json", "r") as f:
        return json.load(f)
