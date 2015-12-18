import ConfigParser
import argparse
import re
import pandas as pd

parser = argparse.ArgumentParser(
    description=('Create weighted institutional rankings from RePEC'
          ' based on custom combinations of economic fields')
)
parser.add_argument('--codes', '-c', nargs='*', type=str, default=[],
                    help='Fields to search')
parser.add_argument('--weights', '-w', nargs='*', type=float, default=[],
                    help=('Weights to assign to scores in '
                                 'each fields. Must match length '
                                 'of --codes and --codes must be '
                                 'specified'))
parser.add_argument('--outf', '-o', default=None,
                    help=('File to dump output. If '
                                 'None, writes to stdout'))
parser.add_argument('--config',
                    help=('Location of config file. Ignores other '
                                 'options if specified.'))


def table_for_code(code, weight=1):
    """
    Parameters
    ==========
    code: str
    three-letter lowercase NEP field code

    Returns
    =======
    Top rankings from code listed as a pandas DataFrame
    """

    base_url = 'https://ideas.repec.org/top/top.%s.html'
    scoresdf = pd.read_html(base_url % code.lower(),
                            encoding='utf-8')[0]
    scoresdf.set_index('Institution', inplace=True)
    scoresdf['weight'] = weight
    scoresdf['weighted_score'] = scoresdf['weight'] * scoresdf['Score']
    return scoresdf[
        ['Score', 'Authors', 'Rank', 'weight', 'weighted_score']
    ]


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

    dfs = {code: table_for_code(code, weight) for code, weight in
           zip(codes, weights)}
    indices = []
    indices = list(reduce(lambda x, y: x | y,
                          map(lambda x: set(x.index.tolist()), dfs.values())))
    dfs = {code: dfs[code].reindex(indices).fillna(dfs[code]['Score'].max())
           for code in dfs.keys()}

    df = reduce(lambda x, y: x[['weighted_score']] + y[['weighted_score']],
                dfs.values())
    return (df / sum(weights)).sort_values('weighted_score').round(3)


def read_config(config_file):
    parser = ConfigParser.ConfigParser()
    parser.read(config_file)
    section = 'ScoringSettings'
    return {
        'codes': parser.get(section, 'codes').split(', '),
        'weights': map(float, parser.get(section, 'weights').split(', ')),
        'outf': parser.get(section, 'outf')
    }


if __name__ == '__main__':
    args = parser.parse_args()
    if args.config:
        opts = read_config(args.config)
        codes = opts['codes']
        weights = opts['weights']
        outf = opts['outf']
    else:
        codes = args.codes if len(args.codes) > 0 else ['inst.all']
        weights = args.weights if len(args.weights) > 0 else [1] * len(codes)
        outf = args.outf if args.outf else 'stdout'

    if len(weights) != len(codes):
        raise ValueError(
            ('Number of weights passed (%d) must equal number of codes '
             '(%d)') % (len(args.weights), len(args.codes))
        )

    scores = weighted_scores(codes, weights)\
        .sort_values('weighted_score').round(3)

    if outf != 'stdout':
        scores.to_csv(outf, encoding='utf-8', header=True)
    else:
        with pd.option_context('max_rows', len(scores)):
            print scores
        if len(scores) > pd.get_option('max_row'):
            print ('***********************************\n'
                   'Result df is pretty long. Consider writing to file. Be '
                   'prepared to do some scrolling.\n'
                   '***********************************')
