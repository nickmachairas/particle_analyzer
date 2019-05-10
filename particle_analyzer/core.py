import xml.etree.ElementTree as ETree
from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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

        print("Parsing input file...\n")
        tree = ETree.parse(self.file_path)
        root = tree.getroot()
        date = root[0].attrib['measurement']
        product = root[0].attrib['product']
        test_filter = root[0].attrib['filter']
        particle_num = len(root) - 1

        print("===========")
        print("File Header")
        print("===========")
        print("Date:", date)
        print("Product:", product)
        print("Filter:", test_filter)
        print("Detected data for {} particles within '{}'"
              "".format(particle_num, self.file_path))
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

        # Fix data types in df (all numerical except for 'pixel' string)
        for column in df.columns:
            if column != "pixel":
                df[column] = pd.to_numeric(df[column], errors='coerce')

        return date, product, test_filter, particle_num, df

    def show_image(self, index):
        """Decodes pixel string and plots a particle image

        """

        # Initial parameters
        width = self.df.width[self.df.frame == index].values[0]
        height = self.df.height[self.df.frame == index].values[0]
        pixel_string = self.df.pixel[self.df.frame == index].values[0]

        # Run decoder
        hex_row = []
        hex_str = ''
        pixel_table = []
        pixel_row = []

        for i in pixel_string:
            hex_str = hex_str + i
            if len(hex_str) == 4:
                hex_str = hex_str[2:] + hex_str[:2]  # flip hex
                hex_row.append(hex_str)
                hex_num = int(hex_str, 16)
                pixel_row.append(hex_num)
                hex_str = ''
            if len(hex_row) == 3:
                pixel_table.append(pixel_row)
                hex_row = []
                pixel_row = []

        pixel_table = np.array(pixel_table)

        X = pixel_table[:, 0]
        Y = pixel_table[:, 1]
        Z = pixel_table[:, 2]

        fig = plt.figure(figsize=(3, 3))
        plt.subplots_adjust(0.02, 0.02, 0.98, 0.98)  # removes margins from savefig
        ax = fig.add_subplot(111, aspect='equal')
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        for x, y, z in zip(X, Y, Z):
            ax.add_patch(patches.Rectangle((x, y), z, 1, facecolor="black"))
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.axis('off')
        # fig.savefig('pict.png', cmap='Greys')
        fig.show()
