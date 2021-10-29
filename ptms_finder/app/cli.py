"""
Entry point for the PTMs Finder Client
"""
import click

from ptms_finder import finder

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.command()
# required argumets
@click.argument(
    "input_file_path",
    type=click.Path(exists=True, dir_okay=False, allow_dash=True),
)
@click.argument(
    "fasta_file_path",
    type=click.Path(exists=True, dir_okay=False, allow_dash=True),
)
@click.argument("output_file_path", type=click.Path(dir_okay=True, allow_dash=True))
# optional arguments
@click.option(
    "--file_format",
    nargs=1,
    default="tsv",
    type=click.Choice(["tsv", "csv"], case_sensitive=False),
    help=(
        "A file format to read in an input file and write out to an output file,"
        " which defaults to tsv. csv is also supported."
    ),
)
def find(input_file_path, fasta_file_path, output_file_path, file_format):
    """
    Find post-translational modifications (PTMs).
    \b
    Arguments:
        \b
        INPUT_FILE_PATH - A path to an input file with a list of peptide sequences
        FASTA_FILE_PATH - A path to a fasta file with protein sequences
        OUTPUT_FILE_PATH - A path to an output file
    """
    finder.run(input_file_path, fasta_file_path, output_file_path, file_format)


cli.add_command(find)
