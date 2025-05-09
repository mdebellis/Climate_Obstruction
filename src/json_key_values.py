import json

def read_and_flatten_json(file_path, sep='.'):
    """
    Reads a JSON file, flattens any nested structures, and returns the resulting dictionary.

    Args:
        file_path (str): The path to the JSON file.
        sep (str, optional): The separator to use when flattening nested keys
            (e.g., 'address.street'). Defaults to '.'.

    Returns:
        dict: A flattened dictionary representing the JSON data, or None if an
              error occurs during file processing or JSON decoding.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)  # Load the JSON data

    def _flatten(json_obj, parent_key=''):
        """
        Recursively flattens a nested JSON object, helper function!
        """
        items = []
        for k, v in json_obj.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(_flatten(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)

    return _flatten(data)  

# Example Usage:
file_path = 'sample1.json'  #replace with json file path
flattened_data = read_and_flatten_json(file_path)
print(flattened_data)