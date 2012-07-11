import sys

import argparse
import lmlexer
import lmparser
import tagparser
import mdcodegen
import logging

def main():
    cli_parser = argparse.ArgumentParser(
            description="A LaTeX processor for Markdown")
    cli_parser.add_argument(
            '-f',
            required=True,
            metavar="FILE",
            help="Input matex file. '-' for stdin.")
    cli_parser.add_argument(
            "-o",
            metavar="FILE",
            default=None,
            help=("Output Markdown file. Images will be placed in same " +
                "dir unless overridden with -i. Defaults to ./output.md."))
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
    args = cli_parser.parse_args()

    # Set log level
    if args.debug:
        log_lvl = logging.DEBUG
    else:
        log_lvl = logging.ERROR
    logging.basicConfig(level=log_lvl)
    # Get from stdin if file is -
    if args.f == "-":
        input_file = sys.stdin
    else:
        input_file = open(args.f)
    # Lex
    lexer = lmlexer.LmLexer(args)
    token_stream = lexer.lex(input_file.read())
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
