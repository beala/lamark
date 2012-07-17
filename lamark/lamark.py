import sys

import argparse
import lmlexer
import lmparser
import tagparser
import mdcodegen
import logging

def main():
    cli_parser = argparse.ArgumentParser(
            description="A tool for embedding LaTeX in Markdown.")
    cli_parser.add_argument(
            '-f',
            required=True,
            metavar="FILE",
            help="LaMark input file. '-' for stdin.")
    cli_parser.add_argument(
            "-o",
            metavar="FILE",
            default=None,
            help=("Markdown output file. Images will be placed in same " +
                "directory unless overridden with -i. Defaults to stdout, "+
                "in which case images will be placed in the pwd."))
    cli_parser.add_argument(
            "-i",
            metavar="DIR",
            default=None,
            help="Image directory.")
    cli_parser.add_argument(
            "--debug",
            action='store_true',
            default=False,
            help="Turn on debug messages.")
    cli_parser.add_argument(
            "--warn",
            action='store_true',
            default=False,
            help="Turn on warning messages.")
    args = cli_parser.parse_args()

    # Set log level
    if args.debug:
        log_lvl = logging.DEBUG
    elif args.warn:
        log_lvl = logging.WARNING
    else:
        log_lvl = logging.ERROR
    logging.basicConfig(
            level=log_lvl,
            format='%(levelname)s:%(message)s')
    # Get from stdin if file is -
    if args.f == "-":
        input_file = sys.stdin
    else:
        input_file = open(args.f)
    # Lex
    lexer = lmlexer.LmLexer(args)
    with input_file as f:
        token_stream = lexer.lex(f.read())
    logging.debug("Token stream:\n" + str(token_stream))
    # Parse
    parser = lmparser.LmParser(args)
    ast = parser.parse(token_stream)
    logging.debug("AST:\n" + str(ast))
    # Parse tags
    tparser = tagparser.TagParser(args)
    tag_ast = tparser.parse(ast)
    logging.debug("Tag AST:\n" + str(tag_ast))
    # Gen markdown and images
    code_gen = mdcodegen.MdCodeGen(args)
    md = code_gen.generate(tag_ast)
    # Write resultant markdown
    if args.o:
        output_file = open(args.o, 'w')
    else:
        output_file = sys.stdout
    with open(args.o, 'w') if args.o else sys.stdout as output_file:
        output_file.write(md)

if __name__=="__main__":
    main()
