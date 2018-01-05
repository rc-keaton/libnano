'''
fasta.py
Read in FASTA files
'''

import re
import io

_fasta_re = r'>(.+)[\n\r]+((?:[^>\S]|[{}]+[\n\r]+)+)'

_ALPHABETS = {
    'DNA': r'ACGTWSMKRYBDHVN',
    'RNA': r'ACGUWSMKRYBDHVN',
    'AMINO_ACID': r'ABCDEFGHIJKLMNOPQRSTUVWYZX*-'
}

def sanitizeRecSeq(rec_id, rec_seq, alphabet, not_allowed):
    if alphabet == None and not_allowed:
        for idx, c in enumerate(rec_seq):
            if c in not_allowed:
                raise ValueError('Record: {}\n Contains illegal char {} at '
                                 'position {}'.format(rec_id, c, idx))
    if alphabet:
        ab = _ALPHABETS.get(alphabet.upper(), alphabet)
        replace_str = ''

        if not_allowed:
            for c in not_allowed:
                ab = ab.replace(c, replace_str)
        for idx, c in enumerate(rec_seq):
            if not c in ab:
                raise ValueError('Record: {}\n Contains illegal char {} at '
                                 'position {}'.format(rec_id, c, idx))
# end def

def parseFasta(fasta_fn, alphabet='DNA', not_allowed=None):
    ''' Parse a standard fasta file and return a list of tuples containing
    the record id, sequence. Optionally check each sequence against an alphabet
    (DNA, RNA, AMINO_ACID, or a custom alphabet) and/or against a list of
    characters that are not allowed:

        alphabet = 'DNA' and not_allowed = 'N' - check against the DNA alphabet
                                                  but do not allow degeneracy
        alphabet = 'ATGC' - custom alphabet (insure that every character in
                            the sequence is A, T, G, or C)

    If a sequence fails the alphabet / not_allowed check a ValueError is
    raised.
    '''

    re_comp = re.compile(_fasta_re.format(_ALPHABETS.get(alphabet, alphabet)))

    with io.open(fasta_fn, 'r', encoding='utf-8') as fd:
        d = [(match.group(1).strip(), \
             ''.join(match.group(2).strip().split())) \
                for match in re.finditer(re_comp, fd.read()) ]
        if alphabet or not_allowed:
            for rec_id, rec_seq in d:
                sanitizeRecSeq(rec_id, rec_seq, alphabet, not_allowed)
    return d
# end def

def parseFastaGen(fasta_fn, alphabet='DNA', not_allowed=None):
    ''' Generator that returns parsed records (ID, sequence) from a FASTA
    file.
    '''

    rec_id = ''
    rec_seq = ''
    start_record_delim = '>'
    end_record_delim = ''

    join_base = lambda: ''
    split_str = ' '

    with io.open(fasta_fn, 'r', encoding='utf-8') as fd:
        for line in fd:
            if start_record_delim in line:
                if rec_id != end_record_delim:
                    if alphabet or not_allowed:
                        sanitizeRecSeq(rec_id, rec_seq,
                                alphabet, not_allowed)
                    yield rec_id, rec_seq
                rec_id = line.strip().split(split_str)[0][1:]
                rec_seq = join_base()
            else:
                rec_seq += line.strip()
    if alphabet or not_allowed:
        sanitizeRecSeq(rec_id, rec_seq, alphabet, not_allowed)
    yield rec_id, rec_seq
# end def

def write(fasta_fn, records, iotype, wrap_len=60):
    """
    records: a list of tuples of (rec_id, rec_seq)
        []
    iotype: string 'unicode' or 'bytes'
    """
    if not isinstance(iotype, str):
        raise TypeError("Unsupported type of iotype")
    if iotype not in ["unicode", "bytes"]:
        raise TypeError("Unsupported iotype %s", iotype)
    if not isinstance(records, list):
        raise TypeError("records needs to be a list")
    if iotype == "unicode":
        with io.open(fasta_fn, 'w', encoding='utf-8') as fd:
            for record in records:
                writeRecord(fd, records[0], records[1], wrap_len)
    else:
        with io.open(fasta_fn, 'wb') as fd:
            for record in records:
                writeRecordB(fd, records[0], records[1], wrap_len)
# end def


def writeRecord(fd, rec_id, rec_seq, wrap_len):
    """ Write 
    """
    fd.write('>' + rec_id + '\n')
    for i in range(0, len(rec_seq), wrap_len):
        fd.write(rec_seq[i:i + wrap_len])
        fd.write('\n')
# end def

def writeRecordB(fd, rec_id, rec_seq, wrap_len):
    """ Write 
    """
    fd.write(b'>' + rec_id + b'\n')
    for i in range(0, len(rec_seq), wrap_len):
        fd.write(rec_seq[i:i + wrap_len])
        fd.write(b'\n')
# end def
