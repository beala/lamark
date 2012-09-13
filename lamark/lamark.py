import sys

import argparse
import lmlexer
import lmparser
import tagparser
import mdcodegen
import logging

VERSION="0.1.5"

class DictToObj(object):
    """Turn a dict into an object."""
    def __init__(self, entries):
        self.__dict__.update(entries)

def lamark(lamark_str, image_dir, name, imgZoom=2000):
    dict_args = {
            "f":name,
            "o":None,
            "i":image_dir,
            "debug":False,
            "warn":False,
            "zoom":str(imgZoom),
    }
    args=DictToObj(dict_args)
    logging.basicConfig(
            level=logging.ERROR,
            format='%(levelname)s:%(message)s')
    lexer = lmlexer.LmLexer(args)
    token_stream = lexer.lex(lamark_str)
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
    return md

def main():
    cli_parser = argparse.ArgumentParser(
            description="A tool for embedding LaTeX in Markdown.")
    cli_parser.add_argument(
            '-f',
            metavar="FILE",
            default=None,
            help="LaMark input file. Default is stdin.")
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
            "--zoom",
            default="2000",
            metavar="ZOOM",
            help="Default zoom value to pass to dvipng. Defaults to 2000")
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
    cli_parser.add_argument(
            "--version",
            action='store_true',
            default=False,
            help="Display version.")
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
    if args.version:
        print "Version: %s" % VERSION
        return

    # Get from stdin if file is -
    if args.f == None or args.f == "-":
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
