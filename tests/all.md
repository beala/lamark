#A Markdown Document#
Here's some *normal* markdown\blog post. Now we're going to try some latex.

Here we go:

{% latex title="My_Equation" alt_text="Some text" %}
\psi_{tot}(x,-t_0,r) = \frac{1}{(2\pi)^2} \int\!\!\!\int
\tilde\Psi_{tot}\left(k_x,\frac{c}{2}\sqrt{k_x^2 + k_r^2},r=0\right)
{% endlatex %}

And here's some {%latex title="eq"%}inline latex{%endlatex %}.

Here we're going to escape a latex tag \{%latex title="TITLE OF IMAGE" alt="Some alt text" %}\{%endlatex%}
