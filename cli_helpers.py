import os


def add_io_arguments(parser):
    """Add the shared single-file and folder input/output options to an argparse parser."""
    parser.add_argument("-i", "--input", metavar="FILE",
                        help="single binary file to convert (requires --output)")
    parser.add_argument("-o", "--output", metavar="FILE",
                        help="path to write the converted file to (requires --input)")
    parser.add_argument("-I", "--input-dir", metavar="DIR",
                        help="convert every file in this folder (requires --output-dir)")
    parser.add_argument("-O", "--output-dir", metavar="DIR",
                        help="folder to save converted files into (requires --input-dir)")


def resolve_io(parser, args, default_input_dir, default_output_dir):
    """Validate the io options and return (mode, input_path, output_path).

    mode is "file" or "dir". With no options given, folder mode runs on the defaults.
    """
    single = args.input is not None or args.output is not None
    batch = args.input_dir is not None or args.output_dir is not None

    if single and batch:
        parser.error("use either --input/--output or --input-dir/--output-dir, not both")

    if single:
        if args.input is None or args.output is None:
            parser.error("--input and --output must be given together")
        if not os.path.isfile(args.input):
            parser.error(f"input file not found: {args.input}")
        return "file", args.input, args.output

    if batch:
        if args.input_dir is None or args.output_dir is None:
            parser.error("--input-dir and --output-dir must be given together")
        input_dir, output_dir = args.input_dir, args.output_dir
    else:
        input_dir, output_dir = default_input_dir, default_output_dir

    if not os.path.isdir(input_dir):
        parser.error(f"input folder not found: {input_dir}")
    return "dir", input_dir, output_dir


def make_parent_dir(path):
    """Create the folder that will contain path, if it has one."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
