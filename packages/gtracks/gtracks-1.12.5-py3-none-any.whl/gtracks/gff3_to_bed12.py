#===============================================================================
# gff3_to_bed12.py
#===============================================================================

"""Convert gff3 data to bed12 format"""




# Imports ======================================================================

from argparse import ArgumentParser
from pybedtools import BedTool
import gzip




# Functions ====================================================================

def parse_gff_attributes(attr: str):
    """Parse an entry from the "attr" column of a GFF3 file and return it as
    a dict

    Parameters
    ----------
    attr : str
        feature attribute string

    Returns
    ------
    dict
        attr entries as a dict
    """

    return dict(pair.split('=') for pair in attr.split(';'))


def parse_gff(gff, type: str = 'gene', parse_attr=True):
    """Parse a GFF3 file and yield its lines as tuples

    Parameters
    ----------
    gff
        path to GFF3 file
    type
        string indicating feature type to include, or None to include all
        features
    parse_attr : bool
        if False, do not parse attributes

    Yields
    ------
    seqid, start, end, strand, attr
        coordinates of a feature
    """

    with (gzip.open(gff, 'rt') if str(gff).endswith('.gz') else open(gff, 'r')) as f:
        for line in f:
             if not line.startswith('#'):
                seqid, _, t, start, end, _, strand, _, attr = line.rstrip().split('\t')
                if ((t == type) or (type is None)):
                    if parse_attr:
                        yield (seqid, int(start), int(end), strand,
                            parse_gff_attributes(attr))
                    else:
                        yield seqid, int(start), int(end), strand, '.'


def generate_bed(gff, type: str = 'gene', tag: str = 'ID'):
    """Convert rows of GFF3 data to BED data. This involves reordering the
    columns to conform with BED format and shifting the coordinates to 0-based
    half-open values.

    Parameters
    ----------
    gff
        path to GFF3 file
    type
        type of GFF3 record to parse
    tag : str
        GFF3 attribute tag to parse [ID]

    Yields
    ------
    tuple
        a row of BED data
    """

    for seqid, start, end, strand, attr in parse_gff(gff, type=type):
        yield seqid, start - 1, end, attr[tag], 0, strand


def parse_arguments():
    parser = ArgumentParser(description='convert gff3 to bed12')
    parser.add_argument('gff', metavar='<input.gff3>', help='input gff3 file')
    # parser.add_argument('--canon', action='store_true', help='canonical transcripts only')
    return parser.parse_args()


def main():
    args = parse_arguments()
    transcripts = BedTool(tuple(generate_bed(args.gff, type='mRNA', tag='ID'))).sort()
    exons = BedTool(tuple(generate_bed(args.gff, type='exon', tag='Parent'))).sort()
    cds = BedTool(tuple(generate_bed(args.gff, type='CDS', tag='Parent'))).sort()
    for t in transcripts:
        block_size, block_start = zip(
            *((str(exon.stop - exon.start), str(exon.start - t.start))
              for exon in exons.intersect(BedTool((t,)), nonamecheck=True) if exon.fields[3] == t.fields[3]))
        thick = tuple(c for c in cds.intersect(BedTool((t,)), nonamecheck=True) if c.fields[3] == t.fields[3])
        if thick:
            thick_start = thick[0].start
            thick_stop = thick[-1].end
        else:
            thick_start = t.start
            thick_stop = t.start
        print('\t'.join(str(x) for x in tuple(t) + (thick_start, thick_stop,
            '0,0,0', len(block_size), ','.join(block_size)+',',
            ','.join(block_start)+',')))


if __name__ == '__main__':
    main()
