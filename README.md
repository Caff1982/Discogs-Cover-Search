
# Discogs-Cover-Search

Discogs-Cover-Search is a Python program that downloads cover images from a csv file using the Discogs API. It is designed to be highly flexible, being able to parse search parameters from the csv column headers or allow the user to select their own parameters.

# Requirements and Usage

Use the package manager pip to install the Discogs API Client. 

`pip install discogs_client`

The program can then be run using:

`python main.py`

The application will start by prompting you for the path to the csv file. It will then search the column headers for search parameters and confirm this. You can then add more parameters or remove them before searching. 

Before using the application I would recommend parsing the input csv file for better searching. It may be worth reviewing the Discogs database to make sure the data fits their search criteria. 


