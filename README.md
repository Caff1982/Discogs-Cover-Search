
# Discogs-Cover-Search

Discogs-Cover-Search is a Python program that downloads cover images from a csv file using the Discogs API. It is designed to be highly flexible, being able to parse search parameters from the csv column headers or allow the user to select their own parameters.

# Requirements and Usage

Use the package manager pip to install the Discogs API Client. 

`pip install discogs_client`

The program can then be run using:

`python main.py`

The application will start by prompting you for the path to the csv file. It will then search the column headers for search parameters. You can then add more parameters or remove them before searching. 

Before using the application I would recommend that the columns in your csv file conform to Discogs API search requirements. 'Format' inparticular was often not well defined in the csv files I have used, I ended up parsing the files before running the search. In the future in may add parsing to the parameter dictionary to help with this. 

# Contributing

Any issues and Pull Requests are welcome :)

If you like this project please star it on GitHub and feel free to share with anyone you think may benefit from this. 
