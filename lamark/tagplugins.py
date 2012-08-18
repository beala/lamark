import latexgen
import refgen

tag_plugins = {
        ("latex",):latexgen.LatexGen,
        ("ref", "reffooter"):refgen.RefGen
        }
