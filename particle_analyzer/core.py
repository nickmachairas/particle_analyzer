import xml.etree.ElementTree as ETree
from tqdm import tqdm
import pandas as pd


class ParticleData(object):
    """Class to represent a particle data set

    Attributes
    ----------
    file_path : str
        The path to the XML file

    Methods
    -------
    parse_file()
        Parses input file and saves values in a Pandas data frame
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.date, self.product, self.filter, self.particle_num, self.df = \
            self.parse_file()

    def parse_file(self):
        """Parses input file and saves values in a Pandas data frame

        Returns
        -------
        date : str
            The date and time that the experiment was performed
            TODO: check if this is the date of data export instead
        product : str
            The project name, which is usually the sample name
        filter : str
            TODO: find the proper definition
        particle_num : int
            Total number of particles within the file
        DataFrame
            A Pandas data frame with all values from the XML input file
        """

        print("Parsing input file...")
        tree = ETree.parse(self.file_path)
        root = tree.getroot()
        date = root[0].attrib['measurement']
        product = root[0].attrib['product']
        test_filter = root[0].attrib['filter']
        particle_num = len(root) - 1

        print("File Header")
        print("-----------")
        print("Date:", date)
        print("Product:", product)
        print("Filter:", test_filter)
        print("Detected data for {} particles within {}".format(particle_num,
                                                                self.file_path))
        print("------------------")
        print("Loading particle data in a data frame...")

        # Instantiate DataFrame
        df = pd.DataFrame()

        # Loop and load rows
        with tqdm(total=particle_num) as pbar:
            for child in root:
                if child.tag == "particle":
                    data = child.attrib
                    image = child[0].attrib
                    data.update(image)
                    df = df.append(data, ignore_index=True)
                    pbar.update(1)

        # Fix data types in df
        for column in df.columns:
            if column != "pixel":
                df[column] = pd.to_numeric(df[column], errors='coerce')

        return date, product, test_filter, particle_num, df
