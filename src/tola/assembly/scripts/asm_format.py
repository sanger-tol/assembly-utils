import click
import pathlib
import re
import sys

from tola.assembly.parser import parse_agp, parse_tpf
from tola.assembly.format import format_agp, format_tpf


@click.command(
    help="""Parse and reformat ToL AGP and TPF files. Parses the files
      provided on the comamnd line, or STDIN if none are given.""",
)
@click.argument(
    "input_files",
    nargs=-1,
    type=click.Path(
        dir_okay=False,
        exists=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
@click.option(
    "--input-format",
    "-i",
    type=click.Choice(
        ["AGP", "TPF"],
        case_sensitive=False,
    ),
    help="""Format of input. Automatically determined from each input file's
      extension, or defaults to 'AGP'""",
)
@click.option(
    "--output-file",
    "-o",
    type=click.Path(
        path_type=pathlib.Path,
        exists=False,
    ),
    help="""Output file. Format is guessed from extension. If no output file
      is given, ouput is printed to STDOUT""",
)
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(
        ["AGP", "TPF", "STR", "REPR"],
        case_sensitive=False,
    ),
    help="""Format of output. Automatically determined from output file extension,
      or defaults to 'AGP'. 'STR' is a human-readable format, and 'REPR' is the
      parsed assembly object's data structure.""",
)
@click.option(
    "--name", "-n",
    "assembly_name",
    help="""Name of the assembly. Defaults to the file name or 'stdin'"""
)
def cli(input_files, input_format, output_file, output_format, assembly_name):
    if output_file:
        if not output_format:
            output_format = format_from_file_extn(output_file)
        out_fh = output_file.open("w")
    else:
        out_fh = sys.stdout

    if not output_format:
        output_format = "AGP"

    if input_files:
        for pth in input_files:
            # Select the format of the input file
            if input_format:
                in_fmt = input_format
            else:
                in_fmt = format_from_file_extn(pth, default="AGP")

            # Select the name of the assembly
            asm_name = assembly_name if assembly_name else pth.stem

            with pth.open("r") as in_fh:
                process_fh(in_fh, in_fmt, asm_name, out_fh, output_format)
    else:
        # Process STDIN
        in_fmt = input_format if input_format else "AGP"
        asm_name = assembly_name if assembly_name else "stdin"
        process_fh(sys.stdin, in_fmt, asm_name, out_fh, output_format)


def process_fh(in_fh, in_fmt, asm_name, out_fh, out_fmt):
    if in_fmt == "AGP":
        asm = parse_agp(in_fh, asm_name)
    elif in_fmt == "TPF":
        asm = parse_tpf(in_fh, asm_name)
    else:
        msg = f"Unknown input format: '{in_fmt}'"
        raise ValueError(msg)

    if out_fmt == "AGP":
        format_agp(asm, out_fh)
    elif out_fmt == "TPF":
        format_tpf(asm, out_fh)
    elif out_fmt == "STR":
        out_fh.write(str(asm))
    elif out_fmt == "REPR":
        out_fh.write(repr(asm))
    else:
        msg = f"Unknown output format: '{out_fmt}'"
        raise ValueError(msg)


def format_from_file_extn(pth, default=None):
    """
    Guess the file format from the extension, or default to "AGP"
    """
    if m := re.search(r"\.(agp|tpf)\w*$", pth.name, flags=re.IGNORECASE):
        return m.group(1).upper()
    else:
        return default


if __name__ == "__main__":
    cli()
