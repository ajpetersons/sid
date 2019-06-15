import logging
import click

from sid.cmd.context import Context
from sid.cmd.decorators import verbose
from sid.cmd.formatter import format_matches
from sid.processor.detector import SID
from sid.languages.errors import UnknownLanguageError
from sid.languages.getter import available_languages


if __name__ == '__main__':
    # Allow to run this script directly while debugging
    cli(ctx=Context(), debug=True)


@click.group(help='SID - software SImilarity detection software')
@click.pass_context
def cli(ctx):
    """Base command for cli application. Used to host subcommands. Initially 
        there is only one subcommand, but in case there is need to add more 
        subcommands, backwards compatibility will not be broken.
    
    :param ctx: Command context, that will be passed further if 
        @click.pass_context decorator is present
    :type ctx: click.Context
    """
    pass


@cli.command(help='Run similarity ananlysis on a set of files')
@click.pass_context
@verbose
@click.option('--language', '-l', default='plain', 
    help='Programming language of the software files provided')
@click.option('--file', '-f', default='', multiple=True, 
    help='Files to run detection on')
@click.option('--ignore', show_default=True, multiple=True, 
    help='Files that contain code to be excluded from similarity results')
@click.option('--fingerprint-size', '-s', default=5, show_default=True, 
    help='Size of single fingerprint that will be used for matching. Should ' +
         'be set to a value such that any match shorter than this is almost ' +
         'always uninteresting, and any match longer is almost always ' +
         'interesting.')
@click.option('--window', '-w', default=10, show_default=True, 
    help='Window size for fingerprint spacing. This is the length of longest ' +
         'match that should not go unnoticed')
@click.option('--json / --no-json', default=False, 
    help='Output similarity detection results in JSON format instead of ' +
         'prettified text')
def compare(ctx, language, file, ignore, fingerprint_size, window, json):
    """The main command of the software - this function handles similarity 
        detection when called from command line. The function initializes 
        similarity detector with all proper arguments and runs the detectio. 
        After detection completes, results are printed in the format requested 
        by the user - either JSON or formatted user readable (not yet 
        implemented). This function also handles possible exceptions during 
        initialization and all logging related to the subject.
    
    :param ctx: Command context, that has been received from parent command and
        will be passed further if @click.pass_context decorator is present
    :type ctx: click.Context
    :param language: Programming language of the software files provided
    :type language: str
    :param file: Files to run detection on
    :type file: list
    :param ignore: Files that contain code to be excluded from similarity 
        results such as template files
    :type ignore: list
    :param fingerprint_size: Size of single fingerprint that will be used for 
        matching (algorithm k-gram size)
    :type fingerprint_size: int
    :param window: Window size for fingerprint spacing
    :type window: int
    :param json: Indicator if output should be formatted or raw JSON
    :type json: boolean
    :raises e: This function catches error from detector instance creation, and 
        raises the error again for debugging if verbosity is enabled
    """
    c = ctx.ensure_object(Context)

    try:
        s = SID(
            k=fingerprint_size, 
            w=window, 
            language=language, 
            robust_winnowing=True,
        )
    except UnknownLanguageError:
        logging.warn("Could not run similarity detection, unrecognized " +
            "language: {}. Available languages: {}".
            format(language, ", ".join(available_languages())))
        ctx.exit(1)
    except Exception as e:
        logging.warn("Could not run similarity detection, an unknown error " + 
            "has occurred")
        if c.verbosity >= 2:
            raise e
        ctx.exit(1)

    matches = s.detect_pairwise(file, ignore)

    if json:
        print(matches)
    else:
        format_matches(matches)


@cli.command(help='Print information about SID')
@click.pass_context
def about(ctx):
    """Command to print information about similarity detection software. This 
        command prints description about the software itself, parameter 
        descriptions as well as copyright information.

    :param ctx: Command context, that has been received from parent command and
        will be passed further if @click.pass_context decorator is present
    :type ctx: click.Context
    """

    info = """
                            ====      SID      ====

SID is a SImilarity Detector built to aid in detection of academic misconduct. 
This tool is intended to be used by academics that are involved in detection of 
academic misconduct in programming assignments, but is not limited to such 
persons. SID analyzes multiple files and attempts to detect similarities among 
them. Usually source code is refactored in a case of academic misconduct, thus 
SID analyzes the structure of code beyond the scope of identical passages, 
changes in comments, space characters or variable naming.

  **  NOTICE  **
This tool in no way is intended to detect plagiarism and does not do so. SID 
detects similarity among multiple files, which can be purely coincidental and
must be evaluated manually before drawing any conclusions.

There are multiple parameters that can be configured for SID command line tool:
  Files to compare: 
        This is probably the main parameter as it lists all files that need to 
        be considered for similarity. This parameter should be repeated to input 
        multiple files.
  Ignored files: There are often situations when some fragments of code are 
        expected to be similar - code given during lectures, template code, 
        standard algorithms, etc. SID allows to specify files that include 
        fragments which should not be considered as similarity match, there can 
        be multiple such parameters.
  Language: This parameter sets the programming language used for similarity 
        detection and submission preprocessing. Since preprocessing is language 
        specific and SID is not yet capable of determining the language 
        submissions are written in, this parameter is required and must always 
        be set by the user, otherwise SID will assume plain text files.
  Fingerprint size: This integer parameter controls the size of k-grams used in 
        hash calculation. Having longer k-grams means more information saved in 
        each hash value, but will be less sensitive to small matches. This 
        parameter is the main mean to control the sensitivity of the algorithm. 
        Usually this value should be set such that any match that is smaller t
        han fingerprint size is almost always uninteresting, but any match 
        longer - almost always interesting.
  Window size: This is the length of window in which a fingerprint is chosen. 
        Each window consists of a number of consecutive k-grams, which are 
        always offset by one (hence two consecutive k-grams will share k-1 
        symbols). A fingerprint is chosen for each window in the code, with 
        windows covering all possible consecutive fragments (of fixed length) of 
        k-grams. Window size also represents the maximum interval between two 
        consecutive fingerprints.
  JSON results: By setting this parameter, similarity results can be retrieved 
        in JSON format for further processing in GUI tools or other methods. By 
        default SID outputs the results in a prettified format after completing 
        detection. Unfortunately formatting is not yet implemented, so JSON 
        output is returned always.

One parameter, however, is enabled by default in source code level - use of 
robust Winnowing algorithm. This parameter controls fingerprint selection 
strategy, specifically in case of ties for minimal hash robust Winnowing prefers 
to select the hash used in the previous window over the rightmost hash, which is 
the default behaviour. The same guarantees as before still hold, but in some 
cases it can reduce the amount of fingerprints generated, especially in 
repetitive sources.

This tool has been initially developed by Artūrs Jānis Pētersons as a masters 
project at School of Informatics in University of Edinburgh, with supervision 
from Kyriakos Kalorkoti. This tool is intended to be open source for anyone to 
download, use and modify if needed. 

                            ====               ====
    """

    print(info)
