import sys

import argparse
import mdlexer
import mdparser
import tagparser
import mdcodegen

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
            default="./output.md",
            help=("Output Markdown file. Images will be placed in same " +
                "dir unless overridden with -i. Defaults to ./output.md."))
    cli_parser.add_argument(
            "-i",
            metavar="DIR",
            default=None,
            help="Image directory.")
    args = cli_parser.parse_args()

    # Get from stdin if file is -
    if args.f == "-":
        input_file = sys.stdin
    else:
        input_file = open(args.f)
    # Lex
    lexer = mdlexer.MdLexer(args)
    token_stream = lexer.lex(input_file.read())
    print "Token stream:"
    print token_stream
    # Parse
    parser = mdparser.MdParser(args)
    ast = parser.parse(token_stream)
    print "AST:"
    print ast
    # Parse tags
    tparser = tagparser.TagParser(args)
    tag_ast = tparser.parse(ast)
    print "Tag AST:"
    print tag_ast
    # Gen markdown and images
    code_gen = mdcodegen.MdCodeGen(args)
    md = code_gen.generate(tag_ast)
    print md
    # Write resultant markdown
    with open(args.o, 'w') as output_f:
        output_f.write(md)

if __name__=="__main__":
    main()
