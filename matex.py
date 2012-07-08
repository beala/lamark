import argparse
import mdlexer
import mdparser
import tagparser
import mdcodegen

def main():
    cli_parser = argparse.ArgumentParser(
            description="A LATEX processor for Markdown")
    cli_parser.add_argument("FILE")
    cli_parser.add_argument("OUTPUT_FILE")
    args = cli_parser.parse_args()

    l = mdlexer.MdLexer(args)
    token_stream = l.lex(open(args.FILE).read())
    print "Token stream:"
    print token_stream
    m = mdparser.MdParser(args)
    ast = m.parse(token_stream)
    print "AST:"
    print ast
    tparser = tagparser.TagParser(args)
    tag_ast = tparser.parse(ast)
    print "Tag AST:"
    print tag_ast
    mg = mdcodegen.MdCodeGen(args)
    md = mg.generate(tag_ast)
    print md
    with open(args.OUTPUT_FILE, 'w') as output_f:
        output_f.write(md)

if __name__=="__main__":
    main()
