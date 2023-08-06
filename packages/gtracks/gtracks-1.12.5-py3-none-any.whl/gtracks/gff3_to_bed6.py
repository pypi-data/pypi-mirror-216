#===============================================================================
# gff3_to_bed6.py
#===============================================================================

"""Convert gff3 data to bed6 format"""




# Imports ======================================================================

from argparse import ArgumentParser
from pybedtools import BedTool
import gff2bed




# Functions ====================================================================

def parse_arguments():
    parser = ArgumentParser(description='convert gff3 to bed6')
    parser.add_argument('gff', metavar='<input.gff3>', help='input gff3 file')
    parser.add_argument('--type', metavar='<type>', default='gene', help='type of gff3 record to parse [gene]')
    parser.add_argument('--tag', metavar='<tag>', default='ID', help='gff3 tag to parse [ID]')
    return parser.parse_args()


def main():
    args = parse_arguments()
    print(BedTool(gff2bed.convert(
        gff2bed.parse(args.gff, type=args.type), tag=args.tag)).saveas().sort(),
        end='')


# Execute ======================================================================

if __name__ == '__main__':
    main()
