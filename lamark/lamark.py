import sys
import random

import argparse
import lmlexer
import lmparser
import tagparser
import mdcodegen
import logging

VERSION="0.2.1"

class DictToObj(object):
    """Turn a dict into an object."""
    def __init__(self, entries):
        self.__dict__.update(entries)

def lamark(lamark_str, image_dir, name, imgZoom=2000, img_path=None, gen_images=True, debug_level="ERROR"):
    dict_args = {
            "f":name,
            "o":None,
            "i":image_dir,
            "debug":False,
            "warn":False,
            "zoom":str(imgZoom),
            "img_path": img_path,
            "gen_images": gen_images,
    }
    args=DictToObj(dict_args)
    # Set log level
    if debug_level == "DEBUG":
        log_lvl = logging.DEBUG
    elif debug_level == "WARNING":
        log_lvl = logging.WARNING
    else:
        log_lvl = logging.ERROR
    logging.basicConfig(
            level=log_lvl,
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
            "--no-images",
            default=False,
            action='store_true',
            help="Don't generate images, just generate markdown.")
    cli_parser.add_argument(
            "--image-path",
            metavar="PATH",
            default=None,
            help="""The generated markdown will point to the generated images in
                 its source. This sets the default path used in these image tags.
                 This is useful if you will be uploading the images to a server.
                 The default path is relative to the generated file.""")
    cli_parser.add_argument(
            "--doc-name",
            metavar="NAME",
            default=None,
            help="""If input is coming from stdin, use this option to give your
                    document a name. This name can be used by the generation
                    stages.""")
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

    # "-" means get from stdin, and use a random name.
    if args.f == None or args.f == "-":
        input_file = sys.stdin
        doc_name = str(random.getrandbits(32)) if args.doc_name is None else args.doc_name
    else:
        input_file = open(args.f)
        doc_name = args.f
    with input_file as f:
        lamark_string = f.read()

    md = lamark(lamark_string,
            args.i,
            doc_name,
            args.zoom,
            args.image_path,
            not args.no_images,
            "DEBUG" if args.debug else "WARNING")

    # Write resultant markdown
    with open(args.o, 'w') if args.o else sys.stdout as output_file:
        output_file.write(md)

if __name__=="__main__":
    main()
