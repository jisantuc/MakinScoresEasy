Makin' Scores Easy
========

<img src="http://www.interviewmagazine.com/files/2008/11/21/img-martin-scorsese_14532014334.jpg" height="50%" width="50%"/>

This project allows anyone to create custom scores for economics institutions based on their personal preferences about fields of study. There are two ways to use it. The first is from the command line with manually specified options, and the second uses config files. Maybe someday this will be available as a service using Heroku or something, but I'm not a magician, so whatever.

You'll probably want to set up a `virtualenv` for installing depdencies. If you don't know what that is or if you don't know how to do that, follow the `virtualenv` instructions [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/). If you don't have `pip` installed, do that first.

# Usage

## Command line with options

To use the tool from the command line, first clone this directory using:

`git clone https://github.com/jisantuc/MakinScoresEasy.git

The options scorer accepts are:

- `--codes`, `-c`: list of [fields](https://ideas.repec.org/top/) (search "Top institutions by field" for a list of possible fields). If you enter no codes, the scorer will assume you want overall rankings. Codes used are the New Economics Papers codes found [here](http://nep.repec.org/).
- `--weights`, `-w`: list of identical length to the list of fields. This option allows you to express, for example, that you care twice as much about corporate finance (CFN) as how much you care about health economics (HEA). These don't need to sum to one, because the scorer will normalize whatever weights you put in.
- `--outf`, `-o`: an output file. If specified, the results of your custom weighting will be written to disk at the loction specified.

For example, to get a combined financial development and growth (FDG) + heterodox microeconomics (HME) score where you care three times as much about HME as you do about FDG and want to save the results to disk at `mysupergreatrankings.csv`, you would call:

```bash
python scorer.py --codes hme fdg --weights 3 1 --outf mysupergreatrankings.csv
```

## Using a config file

Alternatively, you can use a config file. Your config file should have a section called "RePEC Scorer". An example config file is included in this directory under `config.cfg`.

To call using a config file, specify the `--config` option with the path to your config file when you run. Items in a list should be separated by a "`, `" (a comma *and* a space). **Specifying a config file will cause the scorer to ignore whatever else you specify from the command line.**

If you use a config file, you *must* specify a weight for each code.

An example call identical to the above (using the provided config file) would be:

```bash
./scorer.py --config config.cfg
```
