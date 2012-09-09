#Introduction
LaMark is a tool for embedding LaTeX in Markdown files. It is designed as a companion to Markdown blogging platforms such as Octopress and Jekyll.

Here is an example of a LaMark file: https://github.com/beala/lamark/blob/master/lamark/test/functional/demo.lm

And the cooresponding HTML: http://media.usrsb.in/lamark-demo/demo.html

**For detailed documentation about the LaMark language and its tags, please see the [wiki](https://github.com/beala/lamark/wiki).**

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

Please see the [tag reference](https://github.com/beala/lamark/wiki/Tag-Reference) for the other tags and arguments that are available.

#Command Line
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
