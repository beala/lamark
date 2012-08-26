import latexgen
import refgen

binary_tag_plugins = {
        (
            "math",
            "displaymath",
            "picture",
            "pre",
            "doc"):latexgen.LatexGen,
        ("ref",):refgen.RefGen,
    }

unary_tag_plugins = {
        ("ref-footer",):refgen.FooterGen,
    }
