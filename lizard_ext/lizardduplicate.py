'''
Get Duplicated parameter lists
'''
from collections import defaultdict, deque
from .extension_base import ExtensionBase


class Duplicate(object):
    def __init__(self, start_line, end_line):
        self.start_line = start_line
        self.end_line = end_line


class Sequence(object):
    def __init__(self):
        self.hash = ''

    def append(self, token):
        self.hash += token

    def __eq__(self, other):
        return self.hash == other.hash


class LizardExtension(ExtensionBase):

    SAMPLE_SIZE = 21

    def __init__(self, context=None):
        self.duplicates = []
        self.saved_sequences = deque()
        self.saved_hash = defaultdict(list)
        super(LizardExtension, self).__init__(context)

    def __call__(self, tokens, reader):
        continuous = False
        for token in tokens:
            self.saved_sequences.append(Sequence())
            for s in self.saved_sequences:
                s.append(token)
            if len(self.saved_sequences) > self.SAMPLE_SIZE:
                s = self.saved_sequences.popleft()
                for p in self.saved_hash[s.hash]:
                    if not continuous:
                        self.duplicates.append([Duplicate(1, 6), Duplicate(7, 12)])
                        continuous = True
                if not self.saved_hash[s.hash]:
                    continuous = False
                self.saved_hash[s.hash].append(s)

            yield token
