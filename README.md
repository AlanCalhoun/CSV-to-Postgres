# CSV-to-Postgres
These files are largely based on the work of Nate from StrataScratch. https://github.com/Strata-Scratch/csv_to_db_automation

I highly recommend his tutorials on Pandas and Numpy: https://www.youtube.com/channel/UCW8Ews7tdKKkBT6GdtQaXvQ/playlists

A Jupyter Notebook and .py script to automate importing all the csv’s in a folder to a Postgres DB. The edits I needed to make to overcome an utf-8 encoding error has the potential of dropping some data due needing to use an errors='ignore'.

The script “csv_import_functions.py” was heavily edited to account for how the Electronic Medical Record exports the csv files.

I’m exceptionally new to this, and welcome any suggestions.
