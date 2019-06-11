import click

from sid.processor.detector import SID
from sid.languages.errors import UnknownLanguageError
from sid.languages.getter import available_languages


if __name__ == '__main__':
    cli(ctx={}, debug=True)


@click.group()
@click.option('--debug/--no-debug', default=False, hidden=True)
@click.pass_context
def cli(ctx, debug):
    # TODO: docstring
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug


@cli.command(help='Run similarity ananlysis on a set of files')
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
@click.pass_context
def compare(ctx, language, file, ignore, fingerprintsize, window):
    # TODO: docstring
    try:
        s = SID(k=fingerprintsize, w=window, language=language)
    except UnknownLanguageError:
        click.echo("Could not run similarity detection, unknown language: {}".
            format(language))
        click.echo("Available languages: {}".
            format(", ".join(available_languages())))
        ctx.exit(1)
    except Exception as e:
        click.echo("Could not run similarity detection, an unknown error has " + 
            "occurred")
        if ctx.obj['DEBUG']:
            raise e
        ctx.exit(1)

    matches = s.detect_pairwise(file, ignore)

    print(matches)
