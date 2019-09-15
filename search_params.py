import csv


class Params:
	"""
	We will use this class to get the search params from the CSV file headers, 
	We will also allow the user to manually assign columns to search params,
	Goal will be to return a dict mapping cols to params
	"""

	def __init__(self, filepath, delimiter=',', encoding='utf-8', quotechar='"'):
		self.filepath = filepath
		self.delimter = delimiter
		self.encoding = encoding
		self.quotechar = quotechar
		self.get_columns()

		self.search_params = ('title', 'artist', 'format', 'album', 'label', 'year')


	def get_columns(self):
		"""
		Returns the columns from CSV file as a list
		"""
		with open(self.filepath, 'r', encoding=self.encoding) as file:
			csv_reader = csv.reader(file, delimiter=self.delimter, quotechar=self.quotechar)
			headers = next(csv_reader)
			print(headers)
			self.columns = [col for col in headers]
			print(self.columns)

	def get_param_dict(self):
		param_dict = {}
		for i, col in enumerate(self.columns):
			for param in self.search_params:
				print(col, param)
				if col.lower() == param:
					param_dict[param] = i

		# If item is not on an album it probably is an album
		if not param_dict.get('album'):
			param_dict['format'] = 'album' 
		return param_dict

