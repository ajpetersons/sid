# SID - software SImilarity Detection tool

SID is a SImilarity Detector built to aid in detection of academic misconduct. 
This tool is intended to be used by academics that are involved in detection of 
academic misconduct in programming assignments, but is not limited to such 
persons. SID analyzes multiple files and attempts to detect similarities among 
them. Usually source code is refactored in a case of academic misconduct, thus 
SID analyzes the structure of code beyond the scope of identical passages, 
changes in comments, space characters or variable naming.

## NOTICE

This tool in no way is intended to detect plagiarism and does not do so. SID 
detects similarity among multiple files, which can be purely coincidental and
must be evaluated manually before drawing any conclusions.

## Parameters

There are multiple parameters that can be configured for SID command line tool:

### Files to compare:
This is probably the main parameter as it lists all files that need to be 
considered for similarity. This parameter should be repeated to input multiple 
files.

### Ignored files: 
There are often situations when some fragments of code are expected to be 
similar - code given during lectures, template code, standard algorithms, etc. 
SID allows to specify files that include fragments which should not be 
considered as similarity match, there can be multiple such parameters.

### Language: 
This parameter sets the programming language used for similarity detection and 
submission preprocessing. Since preprocessing is language specific and SID is 
not yet capable of determining the language submissions are written in, this 
parameter is required and must always be set by the user, otherwise SID will 
assume plain text files.

### Fingerprint size:
This integer parameter controls the size of k-grams used in hash calculation. 
Having longer k-grams means more information saved in each hash value, but will 
be less sensitive to small matches. This parameter is the main mean to control 
the sensitivity of the algorithm. Usually this value should be set such that any 
match that is smaller than fingerprint size is almost always uninteresting, but 
any match longer - almost always interesting.

### Window size: 
This is the length of window in which a fingerprint is chosen. Each window 
consists of a number of consecutive k-grams, which are always offset by one 
(hence two consecutive k-grams will share k-1 symbols). A fingerprint is chosen 
for each window in the code, with windows covering all possible consecutive 
fragments (of fixed length) of k-grams. Window size also represents the maximum 
interval between two consecutive fingerprints.

### JSON results: 
By setting this parameter, similarity results can be retrieved in JSON format 
for further processing in GUI tools or other methods. By default SID outputs the 
results in a prettified format after completing detection. Unfortunately 
formatting is not yet implemented, so JSON output is returned always.

One parameter, however, is enabled by default in source code level - use of 
robust Winnowing algorithm. This parameter controls fingerprint selection 
strategy, specifically in case of ties for minimal hash robust Winnowing prefers 
to select the hash used in the previous window over the rightmost hash, which is 
the default behaviour. The same guarantees as before still hold, but in some 
cases it can reduce the amount of fingerprints generated, especially in 
repetitive sources.

## Copyright

This tool has been initially developed by Artūrs Jānis Pētersons as a masters 
project at School of Informatics in University of Edinburgh, with supervision 
from Kyriakos Kalorkoti. This tool is intended to be open source for anyone to 
download, use and modify if needed. 

## How to set up locally

- Download [Antlr jar file](https://www.antlr.org/download.html), and place in 
`/usr/local/lib`
- Install [Antlr Python runtime](https://pypi.org/project/antlr4-python3-runtime/),
use `conda install -c conda-forge antlr-python-runtime` command if running 
Anaconda
- Add Antlr to classpath: 
`export CLASSPATH=".:/usr/local/lib/antlr-4.0-complete.jar:$CLASSPATH"`
- Create an alias for easier use: 
`alias antlr4='java -jar /usr/local/lib/antlr-4.0-complete.jar'`
- Download desired grammar (`*.g4`) file from Antlr 
[library](https://github.com/antlr/grammars-v4)
- Run `antlr4 -Dlanguage=Python3 Language.g4` to build lexer and parser for the 
desired language (Currently Python 3 and Matlab are available in 
`sid/languages/.`)
- Run `python setup.py install` to install locally Python package and command 
line tool
- Use command line tool by first running help: `sid --help`
