"""Parent class to handle data files, in .h5, .mat, or whatever, and to recover
settings from miscellaneous data formats (PICMUS, db-sas, custom, ...).
"""
from ...utils.print import dict_to_list_str


class FileLoader(object):
    """FileLoader class, parent class, main code should use the children.

    :ivar str filepath: The path where to find the data
    :ivar dict data: The dictionary where to store the data, with the same
        architecture as the data file. Every data is stored in a numpy.array
        (if relevant), or raw data otherwise
    :ivar list skip_elements: The list of the elements to skip in our data file
    """

    def __init__(self, filepath):
        """Set the filepath and empty data dict.

        :param str filepath: The path where to find the data
        """
        self.filepath = filepath
        self.data = {}
        self.skip_elements = ['TFMdata']

    def __str__(self):
        """String sentence to recursively display the data. Note that it is
        using pretty_print functions, not all data are displayed for ease of
        read.

        :returns: A pretty print of the data info
        :return type: str
        """
        return '\n'.join(dict_to_list_str(self.data))
