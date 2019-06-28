import logging
import os
import shutil
import json
from jinja2 import Environment, FileSystemLoader


def format_matches(matches, dir):
    """Function receives similarity detection and returns user friendly results 
        of similarity detection.
    
    :param matches: Similarity detection results in JSON format
    :type matches: dict
    :param dir: Directory to save report files in
    :type dir: str
    """
    
    templates_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                                  "templates", "compiled")

    file_loader = FileSystemLoader(templates_path)
    env = Environment(loader=file_loader)
    template = env.get_template("index.html")

    # Results directory is cleared, if it exists, and then created
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)

    res_file_idx = 0
    for result in matches["match_results"]:
        this_file_text = open(result["file"], "r").read()
        for source in result["possible_sources"]:
            source_file_text = open(source["file"], "r").read()

            this_file = {
                "file": result["file"],
                "similarity": source["similarity"]["percentage"]*100.0,
                "lines": source["similarity"]["lines"],
                "text": json.dumps(this_file_text)
            }
            # Find the similarity percentages of the other file
            source_similarity = find_similarity(matches, result["file"], 
                                                source["file"])
            source_file = {
                "file": source["file"],
                "similarity": source_similarity["percentage"]*100.0,
                "lines": source_similarity["lines"],
                "text": json.dumps(source_file_text)
            }
            indices = source["indices"]
            output = template.render(current=this_file, source=source_file, 
                                     indices=indices)
            res_path = os.path.join(dir, "match_{}.html".format(res_file_idx))
            logging.debug('Compiling result file {}'.format(res_path))
            report_file = open(res_path, "w")
            report_file.write(output)
            res_file_idx += 1


def find_similarity(matches, current, source):
    """Function searches for a specific file similarity result among two files. 
        Since the direction of similarity can be in either way, lookup is done 
        in specified direction
    
    :param matches: Similarity detection results in JSON format
    :type matches: dict
    :param current: The name of the current file, assumed to copy from `source` 
        file
    :type current: str
    :param source: The name of assumed source file, this is the file that 
        `current` might have copied from 
    :type source: str
    :return: Similarity results among both files with `percentage` and number of 
        `lines` matched
    :rtype: dict
    """
    for file in matches["match_results"]:
        if file["file"] != source:
            continue

        for possible_source in file["possible_sources"]:
            if possible_source["file"] == current:
                return possible_source["similarity"]

    # If file had not been found, then there is no detected similarity between 
    # the files. Return no similarity scores
    return {
        "similarity": 0.0,
        "lines": 0
    }
