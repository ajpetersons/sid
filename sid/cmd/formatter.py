import logging


def format_matches(matches):
    """Function receives similarity detection and returns user friendly results of similarity detection.
    
    :param matches: Similarity detection results in JSON format
    :type matches: dict
    """
    
    # TODO: implement output formatting
    logging.warn("Formatting is not yet implemented, use `--json` to " +
        "suppress this message")
    print()
    print(matches)
