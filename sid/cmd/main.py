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


@click.group()
@verbose
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
@verbose
@click.option('--language', '-l', default='plain', 
    help='Language of the files provided')
@click.option('--file', '-f', default='', multiple=True, 
    help='Files to run detection on')
@click.option('--ignore', show_default=True, multiple=True, 
    help='Files that contain code to be excluded from similarity results')
@click.option('--fingerprintsize', '-s', default=5, show_default=True, 
    help='Size of single fingerprint that will be used for matching. Should ' +
         'be set to a value such that any match shorter than this is almost ' +
         'always uninteresting, and any match longer is almost always ' +
         'interesting.')
@click.option('--window', '-w', default=10, show_default=True, 
    help='Window size for fingerprint spacing. This is the length of longest ' +
         'match that should not go unnoticed')
@click.option('--json', default=False, type=bool, 
    help='Output similarity detection results in JSON format instead of ' +
         'prettified text')
@click.pass_context
def compare(ctx, language, file, ignore, fingerprintsize, window, json):
    # TODO: docstring
    c = ctx.ensure_object(Context)

    try:
        s = SID(k=fingerprintsize, w=window, language=language)
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
