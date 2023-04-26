# function to convert XML ElementTree element to a dictionary
def elem_to_dict(elem):
    if len(elem) == 0:
        return elem.text
    d = {}
    for child in elem:
        child_dict = elem_to_dict(child)
        if child.tag in d:
            if isinstance(d[child.tag], list):
                d[child.tag].append(child_dict)
            else:
                d[child.tag] = [d[child.tag], child_dict]
        else:
            d[child.tag] = child_dict
    return d


def build_query_string(search_criteria: dict) -> str:
    # build query string
    search_string = ""
    if 'author_first_name' in search_criteria.keys() or 'author_last_name' in search_criteria.keys():
        if "author_first_name" in search_criteria.keys():
            search_string += f'{search_criteria["author_first_name"]} '
        if "author_last_name" in search_criteria.keys():
            search_string += f'{search_criteria["author_last_name"]} '
        search_string = search_string[:-1] + '[Author] '
    if "publication_year" in search_criteria.keys():
        search_string += f'{search_criteria["publication_year"]}[PDAT] '
    if "journal" in search_criteria.keys():
        search_string += f'{search_criteria["journal"]}[Journal]'
    search_string = search_string.strip()
    return search_string
