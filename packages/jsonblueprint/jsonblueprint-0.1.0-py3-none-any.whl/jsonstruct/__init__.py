import json

def extract_structure(json_obj, path=""):
    structure = {}

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            new_path = f"{path}.{key}" if path else key
            structure.update(extract_structure(value, new_path))
    elif isinstance(json_obj, list):
        if not all(item is None for item in json_obj):
            item_structures = [extract_structure(item, f"{path}[i]") if item is not None else None for item in json_obj]
            if all(struct == item_structures[0] for struct in item_structures):
                if item_structures[0] is not None:
                    structure[f"{path}[]"] = item_structures[0]
        else:
            structure[path] = "NoneType[]"
    elif json_obj is None:
        structure[path] = "NoneType"
    else:
        structure[path] = type(json_obj).__name__

    return structure

def simplify_structure(structure, parent_path=""):
    simplified = {}
    for key, value in structure.items():
        new_key = key[len(parent_path):] if parent_path in key else key
        if isinstance(value, dict):
            value = simplify_structure(value, new_key)
        simplified[new_key] = value
    return simplified

def build_structure(json_obj, path=""):
    structure = {}
    structure_dict = {}
    structure_catalog = {}

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            new_path = f"{path}.{key}" if path else key
            structure.update(build_structure(value, new_path))
    elif isinstance(json_obj, list):
        if not all(item is None for item in json_obj):
            item_structures = [build_structure(item, f"{path}[i]") if item is not None else None for item in json_obj]
            if all(struct == item_structures[0] for struct in item_structures):
                if item_structures[0] is not None:
                    structure_dict = simplify_structure(item_structures[0])
                    struct_sig = str(sorted(structure_dict))
                    if struct_sig not in structure_catalog:
                        structure_catalog[struct_sig] = structure_dict
                    structure[f"{path}[]"] = struct_sig
        else:
            structure[path] = "NoneType[]"
    elif json_obj is None:
        structure[path] = "NoneType"
    else:
        structure[path] = type(json_obj).__name__

    return structure

def nested_dict(input_dict):
    output_dict = {}

    for key, value in input_dict.items():
        parts = key.split('.')
        d = output_dict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]

        d[parts[-1]] = value

    return output_dict
