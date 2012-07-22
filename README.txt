Introduction
============

LaMark is a tool for embedding LaTeX equations in Markdown files. It is
designed as a companion to Markdown blogging platforms such as Octopress
and Jekyll.

Here is an example of a LaMark file:
https://github.com/beala/lamark/blob/master/lamark/test/functional/demo.lm

And the cooresponding HTML: http://media.usrsb.in/lamark-demo/demo.html

Overview
========

LaMark allows LaTeX to be embedded in Markdown files. Running a mixed
LaTeX/Markdown file (called a LaMark file) through the LaMark processor
will result in a pure Markdown file, along with a set of images that
correspond to the embedded LaTeX. For example, consider this LaMark
file:

\`\`\` #Some LaTeX {% latex "http://media.usrsb.in/" %}
a\ :sup:`2+b`\ 2=c^2 {% end %}

{% latex "http://media.usrsb.in/" imgName="one-half.png" %} \`\`\`

Running this through the LaMark processor will result in:

\`\`\` #Some LaTeX |http://media.usrsb.in/0.png|

|http://media.usrsb.in/one-half.png| \`\`\`

Along with two image files: ``0.png`` and ``one-half.png``

Using the command line tool is easy. Process a LaMark file named
``example.lm`` with:

``python lamark.py -f example.lm -o markdown.md``

Or convert straight to HTML using the `reference implementation of
Markdown <http://daringfireball.net/projects/markdown/>`_:

``python lamark.py -f example.lm | ./Markdown.pl > example.html``

Usage
=====

Following Octopress's lead, LaMark tags are wrapped in a bracket and
percent sign as follows:

``{% latex %} [LaTeX] {% end %}``

LaMark tags also accept positional and keyword arguments. The positional
arguments must come before the keyword arguments:

``{% latex "http://media.usrsb.in/" "pythag.png" imgZoom="3000" %} a^2+b^2=c^2 {% end %}``

Where ``http://media.usrsb.in/`` is path to the image, which will be
used in the resultant Markdown file, ``pythag.png`` is the name of the
image that will be generated, and ``3000`` is the ``zoom`` parameter
that dvipng uses to size the image. The syntax is as follows:

``{% latex [path [alt [imgZoom [imgName]]]] %} [LaTeX] {% end %}``

The syntax for the keyword arguments is:

``{% latex [ARG_NAME="ARG_VALUE"] %} [LaTeX] {% end %}``

Where the possible arguments are:

-  ``path``: The path to the image used in the Markdown image tag.
-  ``alt``: The alt text used in the Markdown image tag.
-  ``imgName``: The image name for the generated image, including
   extension (eg, ``my-image.png``)
-  ``imgZoom``: The zoom parameter used by ``dvipng``, which
   coorresponds to the dimensions of the generated image. ``2000`` is
   the default value. Larger values result in larger images (more zoomed
   in).

As stated above, positional and keyword arguments can be used together,
but the positional arguments must come first:

``{%latex [POSITIONAL ARGS] [KEYWORD_ARGS] %} [LaTeX] {%end%}``

LaMark does its best to be flexible, and allow for whitespace in tags.
The following is valid LaMark:

``{% latex             "http://media.usrsb.in/"             "Some LaTeX"                                                          imgZoom="2500"             %}a^2             {%end            %}``

In short, most sensible (and some wacky) whitespacing styles are valid.

LaMark tags can be escaped with a backslash. Consider the following
LaMark:

``\{%latex%} a^2 \{%end%}``

This will be rendered as:

``{%latex%} a^2 {%end%}``

Backslashes are only escape characters if they come before a LaMark tag.
In all other cases, they carry no special meaning and will be left alone
by the LaMark processor.

Using the command line tool is self-explanatory:

\`\`\` % python lamark.py -h usage: lamark.py [-h] -f FILE [-o FILE] [-i
DIR] [--debug] [--warn]

A LaTeX processor for Markdown

optional arguments: -h, --help show this help message and exit -f FILE
LaMark input file. '-' for stdin. -o FILE Markdown output file. Images
will be placed in same directory unless overridden with -i. Defaults to
stdout, in which case images will be placed in the pwd. -i DIR Image
directory. --debug Turn on debug messages. --warn Turn on warning
messages. \`\`\`

Dependencies
============

``latex`` and ``dvipng`` are required.

-  OS X: Install MacTeX: http://tug.org/mactex/
-  Ubuntu: ``sudo apt-get install texlive``

Tested on Python 2.7.2+

License
=======

\`\`\` Copyright (c) 2012 Alex Beal alexlbeal@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. \`\`\`

.. |http://media.usrsb.in/0.png| image:: http://media.usrsb.in/0.png
.. |http://media.usrsb.in/one-half.png| image:: http://media.usrsb.in/one-half.png
