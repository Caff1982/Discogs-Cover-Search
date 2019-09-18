import csv

from discogs import Discogs


# hard coded while testing
filepath = 'AlbumsExport.csv'

class ImageScraper:
    """
    Takes CSV file of music releases and searches Discogs API for cover image.
    Creates a dictionary mapping the column headers to search terms which can
    be customized.
    Cover images are saved in 'images' directory using the cover id from 
    Discogs. Creates an output CSV copying each row and adding the cover id
    of 'Null' if nothing found.
    """

    def __init__(self, filepath, delimiter=',', encoding='utf-8', quotechar='"'):
        self.discogs = Discogs()
        self.filepath = filepath
        self.delimiter = delimiter
        self.encoding = encoding
        self.quotechar = quotechar
        self.search_terms = ('title', 'artist', 'format', 'album', 'label', 'year')
        self.output_csv = 'output.csv'

        self.get_columns()
        self.get_param_dict()


    def get_columns(self):
        """
        Returns the columns from CSV file as a list
        """
        with open(self.filepath, 'r', encoding=self.encoding) as file:
            csv_reader = csv.reader(file, delimiter=self.delimiter, quotechar=self.quotechar)
            headers = next(csv_reader)
            self.columns = [col for col in headers]
            print(self.columns)

    def get_param_dict(self):
        self.param_dict = {}
        for i, col in enumerate(self.columns):
            for param in self.search_terms:
                if col.lower() == param:
                    self.param_dict[param] = i

        # If item is not on an album it probably is an album
        # if not param_dict.get('album'):
        #     param_dict['format'] = 'album' 

    def get_search_params(self, row):
        """
        Takes row from csv file and returns a dictionary mapping the search
        parameters to their values
        """
        params = {}
        for k,v in self.param_dict.items():
            params[k] = row[v].replace(" ", "+")
        return params

    def run(self):
        with open(filepath, 'r', encoding=self.encoding) as input_file:
            csv_reader = csv.reader(input_file, delimiter=self.delimiter)
            next(csv_reader)
            for row in csv_reader:
                print(row)
                params = self.get_search_params(row)
                try:
                    response, cover_id = self.discogs.search(params)
                    with open(self.output_csv, 'a') as output_file:
                        output_csv = csv.writer(output_file)
                        output_csv.writerow(row + [cover_id])
                        binary_str = response.read()
                        file_obj = open('images/' + cover_id + '.jpg', 'wb')
                        file_obj.write(binary_str)
                        file_obj.close()
                except TypeError:
                    with open(self.output_csv, 'a') as output_file:
                        output_csv = csv.writer(output_file)
                        output_csv.writerow(row + ['Null'])




if __name__ == '__main__':
    # TODO: display InputFileParser arg
    file = ImageScraper(filepath, delimiter=';', encoding='utf-8-sig')
    # TODO: confirm paramters before searching
    print(file.param_dict)
    file.run()




    
