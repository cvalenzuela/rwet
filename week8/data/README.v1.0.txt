Cornell Movie-Quotes Corpus v1.0 (released July 2012)

Distributed together with:

"You had me at Hello: How phrasing affects memorability"
Cristian Danescu-Niculescu-Mizil, Justin Cheng, Jon Kleinberg and Lillian Lee
ACL 2012

RELATED CORPUS:  Cornell Movie-Dialogs Corpus, available at http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html

NOTE: If you have results to report on these corpora, please send email to cristian@cs.cornell.edu so we can add you to our list of people using this data.  Thanks!

 
Contents of this README:

	A) Brief description
	B) Memorability annotation
	C) Files description
	D) Contact

A) Brief description:

This corpus contains a collection of movie lines together with memorability annotations.

- 894014 movie script lines
- from 1068 movie scripts
- 6282 one-line memorable quotes that are automatically matched with the script line which contain them
- 2197 one-sentence memorable quotes paired with surrounding non-memorable quotes from the same movie, spoken by the same character and containing the same number of words

B) Memorability annotation

<> The memorability annotations are based on IMDb’s Memorable Quotes pages.  It is important to note that often the form of the IMDb-memorable-quote is different from the form in which the quote appears in the movie script.  For example, an IMDb quote for the movie psycho is:

"Oh, someone has seen her, all right. Someone always sees a girl with $400,000."

however, the quote appears in the movie script as:

"Someone has seen her. Someone always sees a girl with forty thousand dollars."

which is actually part of a longer line:

"Someone has seen her. Someone always sees a girl with forty thousand dollars. She is your girl friend, isn't she?"

In order to automatically match IMDb-memorable-quotes with script lines, we used an matching mechanism based on edit distance, lexical overlap and a few simple heuristics.  Keep in mind that although this matching mechanism works with very high precision, we did not manually check every single match, so a few matching errors may have  occurred.

<> Note that this corpus does not contain all IMDb memorable quotes: we discard quotes that have fewer than 20 characters and quotes that could not be confidently matched with with any line in the movie script.  Also, we did not consider multi-line IMDb quotes (blocks of lines involving multiple characters).



C) Files description:


<> moviequotes.memorable_nonmemorable_pairs.txt

	- this is the data used in the "You had me at hello" paper referenced above.
	- it contains 2197 pairs of the form (M, N) where:
		- M is a memorable one-sentence quote
		- N is a non-memorable quote selected from the same movie such that it is as close in the script as possible to the M (either before or after it), subject to the conditions that:
	 		(i) M and N are uttered by the same speaker,
			(ii) M and N have the same number of words, and
			(iii) N does not occur in the IMDb list of memorable quotes for the movie (either as a single line or as part of a larger block).


	- the pairs are separated by blank lines
	- each pair is represented by 4 lines with the following format:
		MOVIE_TITLE
		MEMORABLE_QUOTE
		LINE_ID_MEMORABLE MATCHED_QUOTE
		LINE_ID_NON_MEMORABLE NON_MEMORABLE_QUOTE

	where:	
		MEMORABLE_QUOTE is the memorable one-sentence quote as it appeared on IMDb.
		LINE_ID_MEMORABLE corresponds to a LINE_ID in moviequotes.scripts.txt (described below) with which the MEMORABLE_QUOTE was matched (see B above for a description of the matching process)
		MATCHED_QUOTE corresponds to the script line with which the MEMORABLE_QUOTE was matched
		LINE_ID_NON_MEMORABLE is the LINE_ID in moviequotes.scripts.txt (described below) of the NON_MEMORABLE_QUOTE

	- Example pair:
		star wars
		The Force is strong with this one.
		736048 The Force is strong with this one!
		735122 Send a detachment down to retrieve them.




<> moviequotes.memorable_quotes.txt

	- contains 6282 memorable one-line quotes (could be multiple sentences)
	- items are separated by blank lines
	- each item contains 3 lines with the following format:
		MOVIE_TITLE
		MEMORABLE_QUOTE
		LINE_ID_MEMORABLE MATCHED_QUOTE

	where:
		MEMORABLE_QUOTE is the memorable one-line quote as it appeared on IMDb
		LINE_ID_MEMORABLE corresponds to a LINE_ID in moviequotes.scripts.txt (described below) with which the MEMORABLE_QUOTE was matched
		MATCHED_QUOTE corresponds to the script line with which the MEMORABLE_QUOTE was matched

	Example item:
		psycho
		Oh, someone has seen her, all right. Someone always sees a girl with $400,000.
		621762 Someone has seen her. Someone always sees a girl with forty thousand dollars. She is your girl friend, isn't she?



<> moviequotes.scripts.txt
	- this file contains lines from 1068 movie scripts
	- one item per line, with the following fields (the field separator is: "+++$+++")
		LINE_ID	MOVIE_TITLE	MOVIE_LINE_NR	CHARACTER	REPLY_TO_LINE_ID TEXT
	where 
		LINE_ID is an unique ID of the script line
		MOVIE_TITLE is the title of the movie script
		MOVIE_LINE_NR is the line in that respective movie script
		CHARACTER is the name of the character uttering that line
		REPLY_TO_LINE_ID is the ID of the line after which this line follows in a conversation; empty field if the line is the beginning of a new conversation (where a conversation is defined as a group of lines not interrupted by stage directions)

	Example item:
		751519 +++$+++ strangers on a train +++$+++ 524 +++$+++ hammond +++$+++ 751518 +++$+++ You look worried. What's the matter?

	- CAVEAT:  in some cases stage directions could not be automatically identified due to the variety of the formats in which the original scripts were retrieved; as a consequence, some stage directions are still present in this file. Note that this does not affect the data used in the paper (moviequotes.memorable_nonmemorable_pairs.txt) which was both automatically and manually cleaned of stage directions.


D) Contact:

Please email any questions to: cristian@cs.cornell.edu (Cristian Danescu-Niculescu-Mizil)



This material is based upon work supported in part by the National Science Foundation under grant IIS-0910664.  Any opinions, findings, and conclusions or recommendations expressed above are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.