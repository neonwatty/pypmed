from pypmed.apis import query_pubmed_api

# test datapoints
test_input = {'author_first_name': 'rachel', 'author_last_name': 'gottschalk', 'institution':  'university of pittsburgh at pittsburgh', 'publication_year': 2022}
test_output = [{'pmid': '35063833',
                'journal_issn': '1879-0372',
                'journal_title': 'Current opinion in immunology',
                'article_title': 'Mechanisms encoding STAT functional diversity for context-specific inflammatory responses.',
                'publication_year': '2022',
                'author_first_name': 'rachel',
                'author_last_name': 'gottschalk',
                'institution': 'university of pittsburgh at pittsburgh'}]


# test query_pubmed_api
def test_query_pubmed_api():
    test_output_hat = query_pubmed_api(search_criteria=test_input)
    assert test_output_hat == test_output
