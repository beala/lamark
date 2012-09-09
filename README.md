#Introduction
LaMark is a tool for embedding LaTeX in Markdown files. It is designed as a companion to Markdown blogging platforms such as Octopress and Jekyll.

Here is an example of a LaMark file: https://github.com/beala/lamark/blob/master/lamark/test/functional/demo.lm

And the cooresponding HTML: http://media.usrsb.in/lamark-demo/demo.html

#Overview
LaMark allows LaTeX to be embedded in Markdown files. Running a mixed LaTeX/Markdown file (called a LaMark file) through the LaMark processor will result in a pure Markdown file, along with a set of images that correspond to the embedded LaTeX. For example, consider this LaMark file:

```
#Some LaTeX
{% math "http://media.usrsb.in/" %}
a^2+b^2=c^2
{% end %}

{% math "http://media.usrsb.in/" imgName="one-half.png" %}
\frac{1}{2}
{% end %}
```

Running this through the LaMark processor will result in:

```
#Some LaTeX
![http://media.usrsb.in/0.png](http://media.usrsb.in/0.png)

![http://media.usrsb.in/one-half.png](http://media.usrsb.in/one-half.png)
```

Along with two image files: `0.png` and `one-half.png`

Using the command line tool is easy. Process a LaMark file named `example.lm` with:

```
lamark -f example.lm -o markdown.md
```

Or convert straight to HTML using the [reference implementation of Markdown](http://daringfireball.net/projects/markdown/):

```
lamark -f example.lm | ./Markdown.pl > example.html
```

#Installation

`pip install lamark`

`latex` and `dvipng` are required.

- OS X: Install MacTeX: http://tug.org/mactex/
- Ubuntu: `sudo apt-get install texlive`

Tested on Python 2.7.2+

#Tutorial

Let's start by embedding an equation in our document using the `math` tag. The following LaMark embeds the equation `a^2`:

```
{% math %} a^2 {% end %}
```

Here we have the LaTeX equation `a^2` wrapped in a `math` tag. Notice that the tag starts with `{%math%}` and ends with a generic `{%end%}` tag. All tags that require a closing tag end with the generic `{%end%}` tag. As can be seen, LaMark resembles HTML, where strings are wrapped in tags to represent formatting/styling.

Just like HTML, LaMark tags also support arguments. Here is the same `math` tag, with the path to the generated image set to `http://media.usrsb.in/eq`:

```
{% math path="http://media.usrsb.in/eq/" %} a^2 {% end %}
```

Notice that the `path` really is just a path. There is no image name. Because we've omitted an image name, the image names will start at `0.png` and increase. We also have the option of explicitly setting an image name:
```
{% math path="http://media.usrsb.in/eq/" imgName="a_squared.png" %}
a^2
{% end %}
```

The generated image will now be called `a_squared.png`, and the generated Markdown will look like:

```
![http://media.usrsb.in/eq/a_squared.png](http://media.usrsb.in/eq/a_squared.png)
```

To generate this yourself, drop that tag in a text file, and run it through the LaMark processor:

```
lamark -f lamarkfile.lm
```

Please see the tag reference for the other tags and arguments that are available.

#Language Reference

LaMark supports two different types of tags: binary and unary. Binary tags have an opening tag and a closing tag (similar to `div` in HTML). Unary tags only have an opening tag (similar to `br` in HTML).

**Binary**:

```
{% TAG_NAME %} [TEXT] {% end %}
```

**Unary**:

```
{% TAG_NAME %}
```

The opening tag of both unary and binary tags have the same syntax:

```
{% TAG_NAME [ARG1 [ARG2 [...]]]] [ARG1_NAME="ARG1_VAL" [ARG2_NAME="ARG2_VAL" [...]]] %}
```

Where each argument is separated by a space, positional arguments come before keyword arguments, and the value of a keyword argument must be wrapped in double quotes. Most sane whitespacing is allowed. For example, the following is valid:

```
{% math
            "http://media.usrsb.in/"
            "Some LaTeX"
            imgZoom="2500"
%}
a^2
{%end%}
```

**At this time, tags cannot contain `%}`, and keyword values cannot contain `"`.**

LaMark tags can be escaped with a backslash. Consider the following LaMark:

```
\{%math%}
a^2
\{%end%}
```

This will be rendered as:

```
{%math%}
a^2
{%end%}
```

Backslashes are only escape characters if they come before a LaMark tag. In all other cases, they carry no special meaning and will be left alone by the LaMark processor.

Nesting of tags is allowed. Nested tags are evaluated from the inner-most tag outward. So, first the inner-most tag is evaluated, and the result is returned/embedded in the tag it's nested in. The evaluation continues up the chain.

## Tag Reference

Currently, LaMark supports 7 tags:
- `math`: For LaTeX equations. Shorthand for LaTeX's `$` symbol.
- `displaymath`: For larger LaTeX equations. Shorthand for `$$`.
- `picture`: For LaTeX pictures. Shorthand for the `picture` module.
- `pre`: Sets the preamble in the generated LaTeX.
- `doc`: Catchall tag for arbitrary LaTeX. Feeds this straight to the LaTeX interpreter.

### math

This renders inline LaTeX equations. Put anything in here that you would put between the `$` symbols (or `math` environment) in LaTeX.

**Example:**

`{%math%}a^2{%end%}`

**Positional arguments:**

`[path [alt [title [imgName [imgZoom]]]]]`

**Keyword arguments:**

Every positional argument has a keyword argument of the same name.

**Argument descriptions:**

- `path`: The path to the image used in the Markdown image tag.
- `alt`: The alt text used in the Markdown image tag.
- `title`: The title text used in the Markdown image tag.
- `imgName`: The image name for the generated image, including extension (eg, `my-image.png`)
- `imgZoom`: The zoom parameter used by `dvipng`, which corresponds to the dimensions of the generated image. `2000` is the default value. Larger values result in larger images (more zoomed in).

### displaymath

This is the same as `math` except the rendered images are larger and indented. Put anything here that you would put between the `$$` (or `displaymath` environment) in LaTeX.

### latex

This tag lets you embed arbitrary LaTeX. It is recommended that you use the `\documentclass{standalone}` for a tight crop of the generated image.

**Example:**

```
{%latex%}
\documentclass{standalone}
\begin{document}
{\LaTeX}
\end{document}
{%end%}
```

**Positional arguments:**

`[path [alt [title [imgName [imgZoom]]]]]`

**Keyword arguments:**

Every positional argument has a keyword argument of the same name.

**Argument descriptions:**

- `path`: The path to the image used in the Markdown image tag. Defaults to "" (current directory).
- `alt`: The alt text used in the Markdown image tag. Defaults to `path`.
- `title`: The title text used in the Markdown image tag. Defaults to "".
- `imgName`: The image name for the generated image, including extension (eg, `my-image.png`)
- `imgZoom`: The zoom parameter used by `dvipng`, which corresponds to the dimensions of the generated image. `2000` is the default value. Larger values result in larger images (more zoomed in).


### pre

This sets the preamble for all of the tags following this tag. The preamble is the section after the `documentclass` declaration, but before the `\begin{document}`. This is useful if the built in arguments for a tag don't offer enough customization.

**Example:**

```
{%pre%}
\usepackage[T1]{fontenc}
\usepackage[light,math]{iwona}
{%end%}
```

**Positional arguments:**

None.

**Keyword arguments:**

None.

# Command Line
Using the command line tool is self-explanatory:

```
% lamark -h
usage: lamark [-h] [-f FILE] [-o FILE] [-i DIR] [--debug] [--warn] [--version]

A tool for embedding LaTeX in Markdown.

optional arguments:
  -h, --help  show this help message and exit
  -f FILE     LaMark input file. Default is stdin.
  -o FILE     Markdown output file. Images will be placed in same directory
              unless overridden with -i. Defaults to stdout, in which case
              images will be placed in the pwd.
  -i DIR      Image directory.
  --debug     Turn on debug messages.
  --warn      Turn on warning messages.
  --version   Display version.
```

#License

```
Copyright (c) 2012 Alex Beal <alexlbeal@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

