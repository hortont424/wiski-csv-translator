WISKI CSV Translator
--------------------

Usage
=====

./wiski.py INPUT\_FILENAME INPUT\_TYPE OUTPUT\_FILENAME

INPUT\_FILENAME is a comma-separated file containing data in the
format defined by INPUT\_TYPE, and OUTPUT\_FILENAME is the name
of the destination CSV file. The destination will be overwritten
if it already exists.

Dependencies
============

* Python 2.6 or 2.7

Adding New Input Types
======================

To add a new input type, copy the file *Passthrough.py* to a new
file, *INPUT\_TYPE.py*. Edit the file, changing instances of 
"Passthrough" to "INPUT\_TYPE".

Next, edit *wiski.py*. The **load\_instructions** function includes
imports for each input type, and returns a list of the input types.
Add an import for your new type (from INPUT\_TYPE import INPUT\_TYPE),
and then add the newly-imported class to the list that is returned.

Finally, make the **process\_row** function in *INPUT\_TYPE.py* perform
your row transformations!
