from sid.languages.getter import get_language_parser
from sid.processor.fingerprint import Fingerprint


class SID(object):
    def __init__(self, k, w, language, robust_winnowing=False):
        self.k = k
        self.w = w
        self.robust_winnowing = robust_winnowing
        self.language_parser = get_language_parser(language)()


    def detect_pairwise(self, files, ignore=[]):
        self.reset()

        self.build_database(files, ignore)
        matches =  self.find_matches()

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

        for file in files:
            self.fingerprint_meta[file] = {}

            source, indices = self.language_parser.clean(file)
            fingerprints = fingerprinter.generate(source)
            self.cleaned_source[file] = {
                'source': source,
                'indices': indices
            }
            
            self.fingerprints[file] = []
            for idx, f in enumerate(fingerprints): 
                fp = f['fingerprint']
                self.fingerprints[file].append(fp)
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
        matches = []

        for f in fragments:
            prefix_len = self.prefix_length(fk, f[0][0]['id'], f[1][0]['id'])
            suffix_len = self.suffix_length(fk, f[0][-1]['id'], f[1][-1]['id'])

            m = {}
            for i in range(2):
                start_offset = f[0]['offset'] - prefix_len
                end_offset = f[-1]['offset'] + suffix_len + self.k - 1

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