class Fingerprint(object):
    d = 257 # Hashing constant
    # q = (1 << 64) - 59 # A large prime, hash taken modulo this
    q = 100


    def __init__(self, k, w, source, robust=False):
        """Fingerprint class constructor. The class processes one input source 
            and generates fingerprints using Winnowing algorithm.
        
        :param k: Size of k-grams to consider
        :type k: int
        :param w: Window size where each window of lentgth w will contain at 
            least one fingerprint
        :type w: int
        :param source: Input text to fingerprint
        :type source: str
        :param robust: Flag to choose if robust winnowing should be used, 
            defaults to False
        :type robust: bool, optional
        """
        self.k = k
        self.w = w
        self.source = source
        self.robust = robust


    def generate(self):
        """Method initiates fingerprint generation. Fingerprints are coupled 
            together with their relative postition to the start of string to 
            locate where the match occurred. Return type is list of dictionaries 
            where two keys exist - 'fingerprint' and 'position'.
        
        :return: Generated fingerprints for the source text
        :rtype: list of dict
        """
        # generate fingerprints from source
        self.fingerprints = []
        self.source_pos = 0 # Start of current k-gram in source
        self.top_d = (self.d ** (self.k - 1)) % self.q

        self.winnowing()

        return self.fingerprints


    def record(self, fingerprint, position):
        """Method records the current fingerprint along with it's position in a 
        global buffer
        
        :param fingerprint: Hash value of the current fingerprint
        :type fingerprint: int
        :param position: Position of the k-gram where fingerprint starts
        :type position: int
        """

        self.fingerprints.append({
            'fingerprint': fingerprint,
            'position': position,
        })


    def winnowing(self):
        """Method implements Winnowing algorithm of choosing fingerprints. Based 
        on https://doi.org/10.1145/872757.872770
        """

        # Circular buffer implementing window of size w
        h = []
        for i in range(self.w):
            h.append(float('inf'))

        r = 0 # Window right end
        min_r = 0 # Index of minimum hash

        # At the end of each iteration, min holds the position of the rightmost 
        # minimal hash in the current window. record(x) is called only the first 
        # time an instance of x is selected as the rightmost minimal hash of a 
        # window.
        next_hash = self.init_hash()
        while next_hash != -1:
            # If we are not at the end of source file, computate next 
            # fingerprint.

            r = (r + 1) % self.w # Shift the window by one
            h[r] = next_hash # And add one new hash

            if min_r == r:
                # The previous minimum is no longer in this window. Scan h 
                # leftward starting from r for the rightmost minimal hash. Note 
                # min starts with the index of the rightmost hash.
                i = (r - 1 + self.w) % self.w
                while i != r:
                    if h[i] < h[min_r]: 
                        min_r = i
                    i = (i - 1 + self.w) % self.w
                
                self.record(h[min_r], self.global_pos(min_r, r)) 
            elif h[r] < h[min_r] or (not self.robust and h[r] <= h[min_r]):
                # Otherwise, the previous minimum is still in this window. 
                # Compare against the new value and update min if necessary.
                min_r = r
                self.record(h[min_r], self.global_pos(min_r, r))

            next_hash = self.next_hash()
    
    
    def init_hash(self):
        """Method computes the initial hash value for the first k-gram. Since 
            the hash function is rolling, the first value must be precomputed. 
            In case the k-gram length is shorter than the input file, one 
            (incomplete) k-gram is assumed.
        
        :return: The hash value of first k-gram in the source text
        :rtype: int
        """

        # Check that source is at least k characters long. Otherwise, compute 
        # hash from the input there is and return that as the only fingerprint 
        # in the document.
        init_hash_length = min(len(self.source), self.k)

        self.hash = 0
        for i in range(init_hash_length): 
            self.hash = ((self.hash + ord(self.source[i])) * self.d) % self.q

        return self.hash

    
    def next_hash(self):
        """Method implements rolling hash function, based on the current hash 
            value. Based on https://doi.org/10.1145/872757.872770 and 
            https://doi.org/10.1147/rd.312.0249 . If the end of source text is 
            reached, method returns -1.
        
        :return: The hash value of the next k-gram in the source text
        :rtype: int
        """

        if len(self.source) <= self.source_pos + self.k:
            # If we are at the end of input, indicate that to the caller.
            return -1

        # Remove first element of the k-gram from hash
        self.hash = (
            self.hash - self.top_d * ord(self.source[self.source_pos])
        ) % self.q

        self.source_pos += 1

        # Add new element to k-gram hash
        k_gram_end = self.source_pos + self.k - 1
        self.hash = (
            (self.hash + ord(self.source[k_gram_end])) * self.d
        ) % self.q

        return self.hash

    
    def global_pos(self, target_idx, curr_idx):
        """Method calculates the global position of k-gram given the relative 
            positions in the circular buffer of length w
        
        :param target_idx: The position index of k-gram we are interested in
        :type target_idx: int
        :param curr_idx: The position index of current last entry in circular 
            buffer
        :type curr_idx: int
        :return: Global position of the k-gram in the source string
        :rtype: int
        """

        # Calculate how far back in the circular we need to look
        delta = (self.w + curr_idx - target_idx) % self.w
        return self.source_pos - delta
