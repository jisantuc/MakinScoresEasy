import ConfigParser
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
    help=('Create weighted institutional rankings from RePEC'
          ' based on custom combinations of economic fields')
)
parser.add_argument('--codes', '-c', nargs='*',
                    description='Fields to search')
parser.add_argument('--weights', '-w', nargs='*',
                    description=('Weights to assign to scores in '
                                 'each fields. Must match length '
                                 'of --codes and --codes must be '
                                 'specified'))
parser.add_argument('--outf', '-o', default=None,
                    description=('File to dump output. If '
                                 'None, writes to stdout'))
parser.add_argument('--config',
                    description=('Location of config file. Ignores other '
                                 'options if specified.'))

def table_for_code(code):
    """
    Parameters
    ==========
    code: str
    three-letter lowercase NEP field code

    Returns
    =======
    Top rankings from code listed as a pandas DataFrame
    """

    pass

def weighted_scores(codes, weights=None):
    """

    Weights institutions' scores in fields identified by codes according
    to weights given in weights. If an institution isn't present in the
    table for one of the codes present in codes, it is given the worst score
    from that table.

    If codes and weights are not the same length and weights is not None,
    throws a ValueError.

    Parameters
    ==========
    codes: list of str
    three-letter lowercase NEP field codes
    weights: list of (positive) numerics
    Importance attached to ranking in each code

    Returns
    =======
    Table of weighted scores for each institution as pandas DataFrame
    """
    
    pass
