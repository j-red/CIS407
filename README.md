# CIS 407 Intership Seminar Portfolio Project

By Jared Knofczynski and JT Kashuba.  
University of Oregon, Fall 2020.

## Features

A simple PDF management system for merging any number of PDF files. While PDFs are everywhere nowadays, working with them without dedicated (and often expensive) programs can still prove to be quite difficult. This PDF Merger allows users to upload any number of PDFs (within reason, of course) and merge them into one document available for download. Users can simply navigate to the webpage, select PDFs from their local machines, click 'Submit', and wait as their new merged PDF is processed! Once the merging is complete, the user will be prompted with a dialog box to save the new file back to their machine.  

* Input PDFs and merged files will be stored on the remote server for two minutes before being deleted from the temporary storage. Be sure to download your merged results before your time is up!

* Built on the Flask micro-framework and Docker containers, this system is portable and extremely lightweight. It could easily be adapted to include other PDF management techniques or scaled to allow for a larger concurrent userbase.

* Sessions are stored individually for each user, preventing users' input from overlapping with one another even with common PDF file names (how many people do you think have a file called 'resume.pdf' saved on their machine? Our guess was, quite a few!).
