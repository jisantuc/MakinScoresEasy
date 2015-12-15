projname
========

This project allows anyone to create custom scores for economics institutions based on their personal preferences about fields of study. There are two ways to use it. The first is from the command line with manually specified options, and the second uses config files. Maybe someday this will be available as a service using Heroku or something, but I'm not a magician, so whatever.

# Usage

## Command line with options

To use the tool from the command line, first clone this directory using:

`git clone https://github.com/jisantuc/projname.git`

Then `chmod a+x scorer.py`.

The options scorer accepts are:

- `--codes`, `-c`: list of [fields](https://ideas.repec.org/top/) (search "Top institutions by field" for a list of possible fields). Should be lowercase, but if you enter them upper case, the scorer will call you names but still work. If you enter no codes, the scorer will assume you want overall rankings.
- `--weights`, `-w`: list of identical length to the list of fields. This option allows you to express, for example, that you care twice as much about corporate finance (CFN) as how much you care about health economics (HEA). These don't need to sum to one, because the scorer will normalize whatever weights you put in.
- `--outf`, `-o`: an output file. If specified, the results of your custom weighting will be written to disk at the loction specified.

For example, to get a combined financial development and growth (FDG) + heterodox microeconomics (HME) score where you care three times as much about HME as you do about FDG and want to save the results to disk at `mysupergreatrankings.csv`, you would call:

```bash
./scorer.py --codes hme fdg --weights 3 1 --outf mysupergreatrankings.csv
```

## Using a config file

Alternatively, you can use a config file. Your config file should have a section called "RePEC Scorer". An example config file is included in this directory under `config.cfg`.

To call using a config file, specify the `--config` option with the path to your config file when you run. **Specifying a config file will cause the scorer to ignore whatever else you specify from the command line.**

An example call identical to the above (using the provided config file) would be:

```bash
./scorer.py --config config.cfg
```
