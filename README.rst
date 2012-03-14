============
python-tools
============

This package is a random collection of tools that might be useful to
python programmers.  All of the code in this repo is released under a
BSD license (see the top-level LICENSE file).

Code released courtesy of S7 Labs (http://s7labs.com).

mongoengine
===========

Tools for use with the excellent MongoEngine package
(http://mongoengine.org/)

extract-model.py
	Reverse engineer mongoengine Document subclass from mongodb
	collection.

	This can be useful when retrofitting mongoengine to an
	existing MongoDB database.  It examines a collection and
	prints a skeleton of a Document subclass which includes field
	and index declarations, as well as stubs of some standard
	methods, such as __unicode__(), which you should flesh out.

	The index declarations should be correct, since there is
	sufficient information in the database to figure out what they
	should be.  If it gets them wrong, that's a bug that needs to
	get fixed.

	The fields are more of a guess.  The best we can do is examine
	a bunch of documents, observe what fields exist, and intuit
	what they should be declared based on what data if found.  Due
	to MongoDB's schema-free nature, we can do no better than
	guess.  Don't just accept this blindly; consider it a starting
	point to save yourself a lot of typing.  Examine the output
	carefully to ensure it makes sense for your data.  If you have
	suggestions for better heuristics, please let me know.  The
	current logic is quite simplistic.
