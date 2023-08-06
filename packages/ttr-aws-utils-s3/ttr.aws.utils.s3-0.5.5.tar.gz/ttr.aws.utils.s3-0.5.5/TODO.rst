====
TODO
====

Simplify definition of time period
==================================
Now, there are two parameters to use. Check, if there is any standard or simpler way 
how to define period in time.

E.g. see calendar, timetrap from Ruby, mercurial...


Write csv only to output, not to a file
=======================================
get rid of one command line parameter -list-file and write all into stdout.

Informative messages must be printed into stderr.

Note: we must keep printing to stderr now even, when some versions in our period of interest are being found,
because if user redirects output to a file, it would not show any visible activity.


all "list aliases" option
=========================
Now, aliases are defined, but are not easily being shown.

Consider using -l option to print list of aliases out.

Warning: be sure, it is really needed, we want to keep the command clean.
