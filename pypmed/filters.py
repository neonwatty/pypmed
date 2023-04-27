from .checks import name_check, institution_check


def author_metadata_filter(author_metadata: dict,
                           article_dict: dict,
                           author_list) -> list:
    # unpack current metadata
    author_query_name = author_metadata['author_first_name'] + ' ' + author_metadata['author_last_name']
    institution = author_metadata['institution']
    # loop over authors in author list and calculate score
    best_match = None
    best_score = 0
    for item in author_list:
        # create author name
        last_name = item['LastName'].lower()
        first_name = item['ForeName'].lower()
        author_list_name = first_name + ' ' + last_name

        # compute score
        score = name_check(author_query_name, author_list_name)

        # check if score is better than previous best
        if score > best_score and score > 80:
            best_score = score
            best_match = item

    # check if best match for name is not None - if so article is confirmed for author
    if best_match is not None:
        # add author info to article package
        article_dict['author_first_name'] = author_metadata['author_first_name']
        article_dict['author_last_name'] = author_metadata['author_last_name']
        # check affiliation if provided
        if institution is not None and 'AffiliationInfo' in list(best_match.keys()):
            try:
              affiliation_info = best_match['AffiliationInfo']['Affiliation']
              score = institution_check(institution, affiliation_info)
              if score > 80:
                  # author and institution confirmed - add to return list
                  article_dict['institution'] = institution
            except Exception as e:
                  article_dict['institution'] = ''
        return article_dict
    return None
