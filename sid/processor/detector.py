import logging
from time import time

from sid.languages.getter import get_language_parser
from sid.processor.fingerprint import Fingerprint


class SID(object):
    """This class is the base of Similarity Detector - SID. This class should be 
        used to run similarity detection, as it facilitates language parsing and 
        cleaning, fingerprint generation as well as pairwise comparison of 
        different files. The main method - `detect_pairwise` runs a detection on 
        a set of files and returns any similarities between all pairs of files 
        provided.
    """

    def __init__(self, k, w, language, robust_winnowing=False):
        """Method initializes SID class instance by setting parameters for 
        detection.
        
        :param k: Size of k-grams to consider
        :type k: int
        :param w: Window size where each window of lentgth w will contain at 
            least one fingerprint
        :type w: int
        :param language: Programming language of the source code
        :type language: str
        :param robust: Flag to choose if robust winnowing should be used, 
            defaults to False
        :type robust: bool, optional
        """
        self.k = k
        self.w = w
        self.robust_winnowing = robust_winnowing
        self.language_parser = get_language_parser(language)()

        logging.debug('Prepared SID class instance')


    def detect_pairwise(self, files, ignore=[]):
        """Method detects pairwise similar fragments of the source files 
            indicated. To exclude similar sections (due to some template or 
            provided fragments) specify ignore parameter.
        
        :param files: File names to run similarity detection on
        :type files: list of str
        :param ignore: File names that include fragments which should be ignored 
            if similarity is detected, defaults to []
        :type ignore: list of str, optional
        :return: An object describing fragments in files that match, partitioned 
            by pairs of files
        :rtype: dict
        """
        logging.info('Will start detection process')
        start = time()
        self.reset()

        self.build_database(files, ignore)
        logging.info('Fingerprint database built')

        matches = self.find_matches()
        logging.info('Found matches in {} file pairs'.
            format(len(matches.keys())))

        grouped_matches = self.group_matches(matches)
        logging.info('All matches have been grouped')
        logging.info('Completed detection in {} seconds'.format(time() - start))
        logging.info('Cleaning up and returning results...')

        return self.sanitize_matches(grouped_matches)

    
    def reset(self):
        """Method clears internal variables used in fingerprint matching among
            all submitted files.
        """
        self.cleaned_source = {}
        self.fingerprints = {}
        self.fingerprint_meta = {}
        self.inv_index = {}

    
    def build_database(self, files, ignore=[]):
        """Method parses files to compute all fingerprints within this file 
            using Winnowing algorithm. Before fingerprint generation, files are 
            passed through language specific parser that removes irrelevant 
            features (whitespaces, etc.). Fingrprints from files are saved as 
            well as inverse index of fingerprints is created mapping 
            fingerprints to files where they are found. The data computed is 
            saved in fields of the caller instance. To exclude similar sections 
            (due to some template or provided fragments) specify ignore 
            parameter.
        
        :param files: File names to run similarity detection on
        :type files: list of str
        :param ignore: File names that include fragments which should be ignored 
            if similarity is detected, defaults to []
        :type ignore: list of str, optional
        """
        fingerprinter = Fingerprint(
            k=self.k, 
            w=self.w, 
            robust=self.robust_winnowing
        )

        ignore_fp = []

        for file in ignore:
            # Compute fingerprints for ignored files and save them in a list to 
            # exclude matches between the submissions that correspond to them
            source, _ = self.language_parser.clean(file)
            fingerprints = fingerprinter.generate(source)
            
            for f in fingerprints:
                ignore_fp.append(f['fingerprint'])

        logging.info('Completed parse of ignored files')
        logging.debug('Ignored files containing {} fingerprints'.
            format(len(ignore_fp)))

        for file in files:
            self.fingerprint_meta[file] = {}

            logging.info('Will parse {}'.format(file))
            source, indices = self.language_parser.clean(file)

            logging.debug('Done parsing, handing to fingerprinter')
            self.fingerprints[file] = fingerprinter.generate(source)

            # Save tokenized source and indices for later lookup when computing 
            # precise indices for matches
            self.cleaned_source[file] = {
                'source': source,
                'indices': indices
            }
            logging.info('Done fingerprinting {}'.format(file))
            
            for idx, f in enumerate(self.fingerprints[file]): 
                fp = f['fingerprint']

                if fp not in self.fingerprint_meta[file]:
                    # This is the first time we see this fingerprint in this 
                    # file
                    self.fingerprint_meta[file][fp] = []

                    if fp not in ignore_fp:
                        # If fingerprint should be ignored, we still keep it in 
                        # file descriptions, but omit it from inverse index to 
                        # not find during matching. In any case, adding to 
                        # inverse index should only be done once per file even 
                        # if fingerprint has duplicates
                        if fp not in self.inv_index:
                            self.inv_index[fp] = []
                        self.inv_index[fp].append(file)

                self.fingerprint_meta[file][fp].append({
                    'id': idx,
                    'offset': f['offset']
                })
                

    def find_matches(self):
        """Method locates matching fingerprints in multiple files. To find 
            matching fingerprints, method iterates through inverse index of 
            fingerprints and for each pair of files sharing fingerprints, adds 
            the matching fingerprints to a list (there might be many matching 
            fingerprints in two files).
        
        :return: An object with filename pair as keys and list of matching 
            fingerprint metadata as values
        :rtype: dict
        """
        matches = {}

        for fp, files in self.inv_index.items():
            # The loop won't start execution if the length of files is 1, which
            # is an uninteresting fingerprint.
            for i in range(len(files) - 1):
                for j in range(i + 1, len(files)):
                    fk = self.file_key(files[i], files[j])
                    if fk not in matches:
                        matches[fk] = []

                    matches[fk].append((
                        self.fingerprint_meta[fk[0]][fp],
                        self.fingerprint_meta[fk[1]][fp]
                    ))

        return matches

    
    def group_matches(self, matches):
        """Method iterates over all matching fingerprints for each pair of files
            and groups them into fragments of consecutive matching fingerprints 
            to detect longer matches. The returned dictionary contains entries 
            for each pair of files with matching fingerprints, and for each 
            matching fragment indices (line, column) are given for start and end 
            of the match.
        
        :param matches: An object with filename pair as keys and list of 
            matching fingerprint metadata as values
        :type matches: dict
        :return: An object with pairs of filenames for each pair of files with 
            common fingerprints as keys; and lists of indices for start and end 
            of matches as values
        :rtype: dict
        """
        grouped_matches = {}

        for fk in matches:
            if fk[0] not in grouped_matches:
                grouped_matches[fk[0]] = []
            grouped_matches[fk[0]].append(
                self.aggregate_matches(fk, 0, 1, matches[fk])
            )

            if fk[1] not in grouped_matches:
                grouped_matches[fk[1]] = []
            grouped_matches[fk[1]].append(
                self.aggregate_matches(fk, 1, 0, matches[fk])
            )

        return grouped_matches


    def aggregate_matches(self, fk, file, source, matches):
        """Method iterates over all fingerprints of `file` (and their 
            counterparts in `source` file) to find longest matching sequences of 
            fingerprints. This task is performed, assuming that one file 
            contains the original (`source`) code, while the other (`file`) has 
            copied parts of it. The method iterates over matched fingerprints 
            and searches for the longest sequence, finding matches for all 
            matched fingerprints of `file`. There may be fingerprints in 
            `source` file that match, but are not included because they were 
            either shorter matches or there were other matches of the same 
            length.
        
        :param fk: File key - pair of filenames where given fingerprints match
        :type fk: tuple
        :param file: Index in `fk` of the file which is assumed to have copied 
            from `source`
        :type file: int
        :param source: Index in `fk` of the file which is assumed has copied 
            from to `file`
        :type source: int
        :param matches: All matching fingerprints among both files
        :type matches: list of tuple
        :return: The matched sequences assuming author of `file` has copied from 
            author of `source` (this is only an assumption when looking for 
            matches to specify inclusion of all fingerprints from `file`). 
            Sequences consist of fragment borders in the original source file
        :rtype: dict
        """
        expanded_matches = []
        # expanded_matches format: [ ({file_meta}, [ {source_meta} ]) ]
        # expanded_matches has sorted fingerprints for file. Each fingerprint   
        # has an associated list of all fingerprints in the potential source 
        # file
        for m in matches:
            for fp in m[file]:
                expanded_matches.append((fp, m[source]))
        
        expanded_matches.sort(key=lambda val: val[0]['id'])

        fragments = []

        for m in expanded_matches:
            # m is a pair (fingerprint, [matching fingerprints]), thus indexing 
            # is 0 and 1 based, not on keys supplied as arguments to this 
            # function
            if (len(fragments) == 0 or 
                    fragments[-1][fk[file]]['to']['id'] + 1 != m[0]['id']):
                # This is the first iteration and no fragments have been 
                # observed or the current file fingerprints do not form a 
                # sequence
                fragments.append({
                    fk[file]: { 'from': m[0], 'to': m[0] },
                    fk[source]: [ { 'from': x, 'to': x } for x in m[1] ]
                })
                continue

            existing_fragments = fragments[-1][fk[source]]
            # existing_fragments are the last fragments that might still be 
            # longer
            continuing_fragments = []
            # continuing_fragments will hold all of existing_fragments that do 
            # continue to match across both files
            following_fragments = { x['id']: x for x in m[1] }
            # following_fragments are the fragments in `source` file that follow 
            # the longest known match
            for f in existing_fragments:
                next_id = f['to']['id'] + 1
                if next_id in following_fragments:
                    # This match among fingerprints continues for longer. We try 
                    # to locate and keep only longest match
                    f['to'] = following_fragments[next_id]
                    continuing_fragments.append(f)
            
            if len(continuing_fragments) == 0:
                # For current file the fingerprint match continues, but none 
                # of the matches in other files continue
                fragments.append({
                    fk[file]: { 'from': m[0], 'to': m[0] },
                    fk[source]: [ { 'from': x, 'to': x } for x in m[1] ]
                })
            else:
                # This match continues, add to further matching
                fragments[-1][fk[file]]['to'] = m[0]
                fragments[-1][fk[source]] = continuing_fragments
            
        # fragments format: [ {file: {meta}, source: [ {meta} ]} ]
        return {
            'file': fk[source],
            'indices': self.merge_fragments((fk[file], fk[source]), fragments)
        }


    def merge_fragments(self, fk, fragments):
        """Method merges lists of consecutive fingerprints and extends the 
            boundaries of matched fragments to further matching symbols before 
            and after the matching fingerprints. Returned list contains objects 
            for each match in the two files concerned, with indices (line, 
            column) for start and end of the match.
        
        :param fk: File key - pair of filenames where the given fragments match
        :type fk: tuple of str
        :param fragments: List of matching fragments. Each fragment is a dict of 
            two entries (one for each file). The file coming first in file key 
            should have only one match description, the other file should have a 
            list of corresponding matches in the other (potential source) file
        :type fragments: list of dict
        :return: List of information for each matching fragment in the two 
            files. For each fragment dictionary with two entries is returned, 
            each of the entries represent list the start and end indices (line, 
            column) for a matching fragment in each file
        :rtype: list of dict
        """
        matches = []

        for f in fragments:
            from_fragment = f[fk[0]] # The fragment actually reported to user

            max_delta_prefix = 0
            max_delta_suffix = 0
            max_delta_idx = None

            for idx, candidate in enumerate(f[fk[1]]):
                prefix = self.prefix_length(fk, from_fragment['from']['id'], 
                                                candidate['from']['id'])
                suffix = self.suffix_length(fk, from_fragment['to']['id'], 
                                                candidate['to']['id'])

                if max_delta_prefix + max_delta_suffix <= prefix + suffix:
                    max_delta_prefix = prefix
                    max_delta_suffix = suffix
                    max_delta_idx = idx

            prefix = max_delta_prefix
            suffix = max_delta_suffix + self.k - 1

            indices = self.cleaned_source[fk[0]]['indices']
            this_file = { 
                'from': indices[from_fragment['from']['offset'] - prefix],
                'to': indices[from_fragment['to']['offset'] + suffix]
            }

            indices = self.cleaned_source[fk[1]]['indices']
            to_fragment = f[fk[1]][max_delta_idx] # The fragment actually reported to user
            source_file = { 
                'from': indices[to_fragment['from']['offset'] - prefix],
                'to': indices[to_fragment['to']['offset'] + suffix]
            }

            matches.append({
                'this_file': this_file,
                'source_file': source_file
            })

        return matches


    def file_key(self, a, b):
        """Method generates a tuple key for two file pair in a dictionary. 
            This is useful to identify all instances of two string pairs
            since the strings might be in reverse order. The tuple contains
            both strings ordered lexicographically.
        
        :param a: First file name
        :type a: str
        :param b: Second file name
        :type b: str
        :return: Lexicographically sorted tuple of both strings
        :rtype: tuple
        """
        return (a, b) if a < b else (b, a)
    

    def prefix_length(self, fk, id_a, id_b):
        """Method computes the length of prefix that also matches among the 
            files before first matching fingerprints. Method takes into 
            consideration ids of first fingerprints that match and tries to find 
            matching segments up to the previous fingerprint (if it exists). The 
            search must be limited by previous fingerprint, because it might 
            match but contain sections of code from fragments that should be 
            ignored.
        
        :param fk: File key - pair of filenames where the given fragments match
        :type fk: tuple of str
        :param id_a: Index of the fingerprint which is at the start of fragment 
            in the first file
        :type id_a: int
        :param id_b: Index of the fingerprint which is at the start of fragment 
            in the second file
        :type id_b: int
        :return: The length of matching prefix before the start of the 
            fingerprint
        :rtype: int
        """
        ids = (id_a, id_b)

        max_length = None # Max possible prefix length
        for f, id in zip(fk, ids):
            fp_meta = self.fingerprints[f][id]
            offset = fp_meta['offset']

            # Initial prefix is from file start to current fingerprint
            prefix = offset 
            if id > 0:
                # If there is previous fingerprint, then prefix can be up to 
                # that fingerprint
                prev_fp_meta = self.fingerprints[f][id - 1]
                prefix = offset - (prev_fp_meta['offset'] + 1)

            # Global length will be minimum of all lengths
            if max_length is None or max_length > prefix:
                max_length = prefix

        prefix = 0
        source_a = self.cleaned_source[fk[0]]['source']
        source_b = self.cleaned_source[fk[1]]['source']

        # Start looking from the previous position from start of the current
        # fingerprint
        target_a = self.fingerprints[fk[0]][id_a]['offset'] - 1
        target_b = self.fingerprints[fk[1]][id_b]['offset'] - 1
        while prefix < max_length:
            if source_a[target_a] != source_b[target_b]:
                # If prefixes do not match, return the longest match
                break
            # Otherwise step backward one position
            target_a -= 1
            target_b -= 1
            prefix += 1
        
        return prefix
    

    def suffix_length(self, fk, id_a, id_b):
        """Method computes the length of suffix that also matches among the 
            files after last matching fingerprints. Method takes into 
            consideration ids of last fingerprints that match and tries to find 
            matching segments before the next fingerprint (if it exists). The 
            search must be limited by next fingerprint, because it might 
            match but contain sections of code from fragments that should be 
            ignored.
        
        :param fk: File key - pair of filenames where the given fragments match
        :type fk: tuple of str
        :param id_a: Index of the fingerprint which is at the end of fragment in
            the first file
        :type id_a: int
        :param id_b: Index of the fingerprint which is at the end of fragment in
            the second file
        :type id_b: int
        :return: The length of matching suffix after the end of the fingerprint
        :rtype: int
        """
        ids = (id_a, id_b)

        max_length = None # Max possible suffix length
        for f, id in zip(fk, ids):
            fp_meta = self.fingerprints[f][id]
            offset = fp_meta['offset']

            source = self.cleaned_source[f]['source']
            # Initial suffix is from file start to current fingerprint
            suffix = (len(source) - 1) - (offset + self.k - 1)
            if id < len(self.fingerprints[f]) - 1:
                # If there is next fingerprint, then suffix can be up to 
                # that fingerprint
                next_fp_meta = self.fingerprints[f][id + 1]
                suffix = (next_fp_meta['offset'] - 1) - offset

            # Global length will be minimum of all lengths
            if max_length is None or max_length > suffix:
                max_length = suffix

        suffix = 0
        source_a = self.cleaned_source[fk[0]]['source']
        source_b = self.cleaned_source[fk[1]]['source']

        # Start looking from the position right after the current fingerprint
        target_a = self.fingerprints[fk[0]][id_a]['offset'] + self.k
        target_b = self.fingerprints[fk[1]][id_b]['offset'] + self.k
        while suffix < max_length:
            if source_a[target_a] != source_b[target_b]:
                # If suffixes do not match, return the longest match
                break
            # Otherwise step forward one position
            target_a += 1
            target_b += 1
            suffix += 1
        
        return suffix


    def sanitize_matches(self, matches):
        """Method restructures found matches in a more generic format that can 
        be more easily parsed by object based programs.
        
        :param matches: The matched sequences assuming author of `file` has 
            copied from author of `source` (this is only an assumption when 
            looking for matches to specify inclusion of all fingerprints from 
            `file`). Sequences consist of fragment borders in the original 
            source file
        :type matches: dict
        :return: An object containing single key with list of all found matches
        :rtype: dict
        """
        clean_matches = []
        file_lengths = {}

        # Count file lines by opening each match only once. All matches are 
        # bidirectional, and will be included in `matches`
        for file in matches:
            with open(file) as f:
                for i, l in enumerate(f):
                    pass
            file_lengths[file] = i + 1

        for file, matched_files in matches.items():
            for idx, match in enumerate(matched_files):
                match['similarity'] = self.get_similarity(
                    match['indices'], 
                    file_lengths[file]
                )
                matched_files[idx] = match

            clean_matches.append({
                'file': file,
                'possible_sources': matched_files
            })

        return {
            'match_results': clean_matches
        }


    def get_similarity(self, indices, total_lines):
        """Method calculates similarity metrics among two files, given code 
            fragment matches from one file to another, assuming that `file` has 
            fragments copied from other source (this does not prove that the 
            code was acutally copied). Metrics like percentage match and matched 
            line counts are calculated.
        
        :param indices: List of matching fragments among the files, consisting 
            of list of borders where matches are found in original source files
        :type indices: list of dict
        :param total_lines: Total number of lines in the file for which metrics 
            are being calculated
        :type total_lines: int
        :return: Similarity metrics among the files. These metrics are 
            one-directional, since the fragments matched can differ
        :rtype: dict
        """

        last_line = 0
        lines_matched = 0
        for i in indices:
            match = i['this_file']
            if match['from']['line'] > last_line:
                # If this match starts on a different line than previous match 
                # ended, add 1 line to the count to account for the first line 
                # of the match
                lines_matched += 1
            
            # Account for overlapping matches and count each line only once
            match_begin = max(match['from']['line'], last_line)
            
            lines_matched += match['to']['line'] - match_begin
            last_line = match['to']['line']
        
        return {
            'percentage': lines_matched / total_lines,
            'lines': lines_matched
        }
