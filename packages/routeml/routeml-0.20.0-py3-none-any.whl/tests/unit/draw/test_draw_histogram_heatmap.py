import unittest
import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

# assuming write_histogram and write_heatmap are in a file called visualizations.py
from routeml.draw import plot_dmatrix_heatmap, plot_dmatrix_histogram

class TestVisualizations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        np.random.seed(0)
        cls.distance_matrix = np.random.randint(1, 10, size=(10, 10))
        cls.distance_matrix = (cls.distance_matrix + cls.distance_matrix.T)/2  # making it symmetric
        np.fill_diagonal(cls.distance_matrix, 0)
        os.makedirs("test_output", exist_ok=True)

    def test_write_histogram(self):
        path = "test_output/histogram.png"
        plot_dmatrix_histogram(self.distance_matrix, save_path=path)
        img = mpimg.imread(path)
        self.assertEqual(img.shape[2], 4)  # Check if the image has RGBA channels

    def test_write_heatmap(self):
        path = "test_output/heatmap.png"
        plot_dmatrix_heatmap(self.distance_matrix, save_path=path)
        img = mpimg.imread(path)
        self.assertEqual(img.shape[2], 4)  # Check if the image has RGBA channels

    @classmethod
    def tearDownClass(cls):
        plt.close('all')  # Close all open pyplot figures

if __name__ == "__main__":
    unittest.main()
