import logging

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
        self.reset()

        self.build_database(files, ignore)
        logging.info('Fingerprint database built')

        matches =  self.find_matches()
        logging.info('Found matches in {} file pairs'.
            format(len(matches.keys())))

        return self.group_matches(matches)

    
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

        self.ignore = []

        for file in ignore:
            source, _ = self.language_parser.clean(file)
            fingerprints = fingerprinter.generate(source)
            
            for f in fingerprints:
                self.ignore.append(f['fingerprint'])

        logging.info('Completed parse of ignored files')
        logging.debug('Ignored files containing {} fingerprints'.
            format(len(self.ignore)))

        for file in files:
            self.fingerprint_meta[file] = {}

            logging.info('Will parse {}'.format(file))
            source, indices = self.language_parser.clean(file)

            logging.debug('Done parsing, handing to fingerprinter')
            fingerprints = fingerprinter.generate(source)

            self.cleaned_source[file] = {
                'source': source,
                'indices': indices
            }
            logging.info('Done fingerprinting {}'.format(file))
            
            self.fingerprints[file] = []
            for idx, f in enumerate(fingerprints): 
                fp = f['fingerprint']
                self.fingerprints[file].append(fp)

                if fp in self.fingerprint_meta[file]:
                    # Fingerprint already seen in file, no need to repeatedly 
                    # add it.
                    continue

                # FIXME: multiple identical fingerprints won't be matched
                self.fingerprint_meta[file][fp] = {
                    'id': idx,
                    'offset': f['offset']
                }

                if fp in self.ignore:
                    continue

                if fp not in self.inv_index:
                    self.inv_index[fp] = []
                self.inv_index[fp].append(file)
                

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

        for fp in self.inv_index:
            files = self.inv_index[fp]

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
            matches[fk].sort(key=lambda val: (val[0]['id'], val[1]['id']))

            fragments = []

            for m in matches[fk]:
                if len(fragments) == 0:
                    fragments.append(([m[0]], [m[1]]))
                    continue
                
                if (fragments[-1][0][-1]['id'] + 1 == m[0]['id'] and
                        fragments[-1][1][-1]['id'] + 1 == m[1]['id']):
                    fragments[-1][0].append(m[0])
                    fragments[-1][1].append(m[1])
                else:
                    fragments.append(([m[0]], [m[1]]))

            grouped_matches[fk] = self.merge_fragments(fk, fragments)

        return grouped_matches


    def merge_fragments(self, fk, fragments):
        """Method merges lists of consecutive fingerprints and extends the 
            boundaries of matched fragments to further matching symbols before 
            and after the matching fingerprints. Returned list contains objects 
            for each match in the two files concerned, with indices (line, 
            column) for start and end of the match.
        
        :param fk: File key - pair of filenames where the given fragments match
        :type fk: tuple of str
        :param fragments: List of matching fragments. Each fragment is a tuple 
            of two entries (one for each file) with lists of fingerprint 
            metadata for match sequences
        :type fragments: list of tuple of list of dict
        :return: List of information for each matching fragment in the two 
            files. For each fragment dictionary with two entries is returned, 
            each of the entries represent list the start and end indices (line, 
            column) for a file
        :rtype: list of dict
        """
        matches = []

        for f in fragments:
            prefix_len = self.prefix_length(fk, f[0][0]['id'], f[1][0]['id'])
            suffix_len = self.suffix_length(fk, f[0][-1]['id'], f[1][-1]['id'])

            m = {}
            for i in range(2):
                start_offset = f[i][0]['offset'] - prefix_len
                end_offset = f[i][-1]['offset'] + suffix_len + self.k - 1

                m[fk[i]] = {
                    'from': self.cleaned_source[fk[i]]['indices'][start_offset],
                    'to': self.cleaned_source[fk[i]]['indices'][end_offset],
                }

            matches.append(m)

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
        meta = self.fingerprint_meta[fk[0]]
        fingerprints = self.fingerprints[fk[0]]
        fp_meta = meta[fingerprints[id_a]]
        offset_a = fp_meta['offset']

        prefix_a = offset_a
        if id_a > 0:
            prev_fp_meta = meta[fingerprints[id_a-1]]
            prefix_a = fp_meta['offset'] - (prev_fp_meta['offset'] + 1)

        meta = self.fingerprint_meta[fk[1]]
        fingerprints = self.fingerprints[fk[1]]
        fp_meta = meta[fingerprints[id_b]]
        offset_b = fp_meta['offset']

        prefix_b = offset_b
        if id_b > 0:
            prev_fp_meta = meta[fingerprints[id_b-1]]
            prefix_b = fp_meta['offset'] - (prev_fp_meta['offset'] + 1)

        max_length = min(prefix_a, prefix_b)

        prefix = 0
        source_a = self.cleaned_source[fk[0]]['source']
        source_b = self.cleaned_source[fk[1]]['source']
        while prefix < max_length:
            idx_a = offset_a - prefix - 1
            idx_b = offset_b - prefix - 1
            if source_a[idx_a] != source_b[idx_b]:
                break

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
        # TODO: might be able to merge with prefix_length
        # TODO: probably should add more comments about some code choices
        meta = self.fingerprint_meta[fk[0]]
        fingerprints = self.fingerprints[fk[0]]
        fp_meta = meta[fingerprints[id_a]]
        offset_a = fp_meta['offset'] + self.k - 1

        suffix_a = len(self.cleaned_source[fk[0]]['source']) - 1 - offset_a
        if id_a < len(self.fingerprints[fk[0]]) - 1:
            next_fp_meta = meta[fingerprints[id_a+1]]
            suffix_a = (next_fp_meta['offset'] - 1) - fp_meta['offset']

        meta = self.fingerprint_meta[fk[1]]
        fingerprints = self.fingerprints[fk[1]]
        fp_meta = meta[fingerprints[id_b]]
        offset_b = fp_meta['offset'] + self.k - 1

        suffix_b = len(self.cleaned_source[fk[1]]['source']) - 1 - offset_b
        if id_b < len(self.fingerprints[fk[1]]) - 1:
            next_fp_meta = meta[fingerprints[id_b+1]]
            suffix_b = (next_fp_meta['offset'] - 1) - fp_meta['offset']

        max_length = min(suffix_a, suffix_b)

        suffix = 0
        source_a = self.cleaned_source[fk[0]]['source']
        source_b = self.cleaned_source[fk[1]]['source']
        while suffix < max_length:
            idx_a = offset_a + suffix + 1
            idx_b = offset_b + suffix + 1
            if source_a[idx_a] != source_b[idx_b]:
                break

            suffix += 1
        
        return suffix
