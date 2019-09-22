import os
import csv
import shutil
import time

from discogs import Discogs


class ImageScraper:
    """
    Takes CSV file of music releases and searches Discogs API for cover image.
    Creates a dictionary mapping the column headers to search terms which can
    be customized.

    Cover images are saved in 'images' directory using the cover id from
    Discogs. Creates an output CSV copying each row and adding the cover id
    of 'Null' if nothing found.
    """
    def __init__(self, filepath, delimiter=',',
                 encoding='utf-8', quotechar='"'):
        self.discogs = Discogs()
        self.filepath = filepath
        self.delimiter = delimiter
        self.encoding = encoding
        self.quotechar = quotechar
        self.search_terms = ('title', 'artist', 'format',
                             'album', 'label', 'year')
        self.output_csv = 'output.csv'

        if not os.path.exists('images/'):
            os.mkdir('images/')
        self.image_path = 'images/'

        self.get_columns()
        self.get_param_dict()

    def get_columns(self):
        """
        Returns the columns from CSV file as a list
        """
        with open(self.filepath, 'r', encoding=self.encoding) as file:
            csv_reader = csv.reader(file, delimiter=self.delimiter,
                                    quotechar=self.quotechar)
            headers = next(csv_reader)
            self.columns = [col for col in headers]

    def get_param_dict(self):
        self.param_dict = {}
        for i, col in enumerate(self.columns):
            for param in self.search_terms:
                if col.lower() == param:
                    self.param_dict[param] = i

    def confirm_dict(self):
        update_dict = True
        while update_dict:
            for param, col in self.param_dict.items():
                print(f'{param} found in column {col}')
            print('\nTo procede with these settings press Enter.')
            print('To add an item enter the header-text then col eg: title 1.')
            print('To delete an item enter the item eg: artist.')
            update_dict = input('> ')
            if update_dict:
                if len(update_dict.split()) == 2:
                    param, col = update_dict.split()
                    self.param_dict[param] = int(col)
                elif len(update_dict.split()) == 1:
                    del self.param_dict[update_dict]
                else:
                    print("I didn't understand that, please try again.")

    def get_search_params(self, row):
        """
        Takes row from csv file and returns a dictionary mapping the search
        parameters to their values
        """
        params = {}
        for k, v in self.param_dict.items():
            params[k] = row[v].replace(" ", "+")
        return params

    def run(self):
        with open(filepath, 'r', encoding=self.encoding) as input_file:
            csv_reader = csv.reader(input_file, delimiter=self.delimiter)
            next(csv_reader)
            for row in csv_reader:
                params = self.get_search_params(row)
                try:
                    response, cover_id = self.discogs.search(params)
                    with open(self.output_csv, 'a') as output_file:
                        output_csv = csv.writer(output_file)
                        output_csv.writerow(row + [cover_id])
                        with open(self.image_path + cover_id + '.jpg', 'wb') as f:
                            shutil.copyfileobj(response.raw, f)
                        del response

                except TypeError:
                    with open(self.output_csv, 'a') as output_file:
                        output_csv = csv.writer(output_file)
                        output_csv.writerow(row + ['Null'])
                time.sleep(1.2)


if __name__ == '__main__':
    filepath = input('Please enter the name or path to the input CSV file.\n')
    file = ImageScraper(filepath)

    file.confirm_dict()

    file.run()
