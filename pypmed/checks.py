
from rapidfuzz import fuzz


def institution_check(institution: str,
                      affiliation_info: str) -> int:
    # define score
    overall_score = 0
    institution_split = institution.split()
    aff_split = affiliation_info.lower().split()

    # loop through each word in the institution name, check match with each word in the affiliation info
    for u in institution_split:
        ind_best = 0
        val_best = 0
        for i, a in enumerate(aff_split):
            s = fuzz.ratio(u, a)
            if s > val_best:
                val_best = s
                ind_best = i

        # remove index of best match
        overall_score += val_best
        del aff_split[ind_best]
    # average overall score
    overall_score /= len(institution_split)
    return overall_score


def name_check(query_author_name: str,
               author_list_name: str) -> int:
    return fuzz.ratio(query_author_name, author_list_name)
