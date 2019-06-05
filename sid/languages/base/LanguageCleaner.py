class LanguageCleaner(object):
    def __init__(self):
        self.name = "identity"


    def clean(self, file):
        token_locations = []

        f = open(file, "r")
        for line_idx, line in enumerate(f):
            for char_idx, char in enumerate(line):
                # TODO: align offsets to antlr
                token_locations.append({
                    'line': line_idx, 
                    'col': char_idx
                })

        f.seek(0)
        return f.read(), token_locations
