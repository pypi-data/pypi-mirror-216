# SPDX-FileCopyrightText: 2023 German Aerospace Center
#
# SPDX-License-Identifier: MIT

import json
import pickle
import re
from pathlib import Path
import os


from jsonpath_ng import parse

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def extract_urls_pmc_ids(input_json: str, map_pickle: str, relevant_strs: list[str]) -> None:
    url_id_map = {}
    with open(input_json, "r") as json_in:
        data = json.load(json_in)
        expr = "$.*.files.*.url_count"
        jsonpath_expression = parse(expr)

        for datum in jsonpath_expression.find(data):
            # Check if any URLs were found at all
            if int(datum.value) > 0:
                all_urls = datum.context.value["all_urls"]
                for url in all_urls:
                    if [substr for substr in relevant_strs if (substr in url)]:
                        # At least one search string was found in the URL, i.e., the URL is relevant,
                        # so get PMC ID from PMC CSV and map it.
                        # The match can only have exactly one context, and that is the parent field,
                        # i.e., the PDF name
                        pdf_file = str(datum.context.path)
                        # Assert that the PDF file name ends with the default string '<PMC ID>.pdf'.
                        match = re.search(r'\.(PMC\d+)\.pdf$', pdf_file)
                        assert match  # TODO Handle differently
                        # Get the first (and only) group from the match, which is the ID part of the file name.
                        pmc_id = match.group(1)
                        if url in url_id_map:
                            url_id_map[url].add(pmc_id)
                        else:
                            # In the dataset as a whole, URLs may be mentioned in more than one publication.
                            # Here though, we only count one occurrence per publication, so it's enough to map
                            # URL to id, and disregard counts. This is because every PDF has exactly one PMC id.
                            url_id_map[url] = set()
                            url_id_map[url].add(pmc_id)

    if url_id_map:
        with open(map_pickle, "wb") as fo:
            pickle.dump(url_id_map, fo, pickle.HIGHEST_PROTOCOL)
    else:
        Path(map_pickle).touch()


def write_metadata(pickle_files: list[str], metadata_json: str):
    repos = []
    repo_objs = {}
    metadata_dict = {"repositories": repos}

    for pf in pickle_files:
        if os.path.getsize(pf) > 0:
            with open(pf, 'rb') as pif:
                pfd = pickle.load(pif)
                for repo_url, id_list in pfd.items():
                    repo_mentions = []
                    for val in id_list:
                        repo_mentions.append(
                            {
                                'mention_id': val,
                                'id_type': 'pmc'
                            }
                        )
                    if not repo_url in repo_objs:
                        repo_obj = {
                            repo_url: {
                                'mentions': repo_mentions,
                                'sources': [
                                    'extract-urls-pmc'
                                ]
                            }
                        }
                        repo_objs[repo_url] = repo_obj
                    else:
                        repo_objs[repo_url]['mentions'].append()

                    # if key in repos_list:
                    #     print(f'FOUND key {key}')
                    #         # repos_list[key]['mentions'].
                    #     # _json['repositories'][key]['publications'].update(value)
                    # else:
                    #     # repo_data = {'mentions': }
                    #     repos_list.get[key] = {'mentions': mention_id}

    with open(metadata_json, 'w') as mj:
        json.dump(metadata_dict, mj, indent=4, cls=SetEncoder)
