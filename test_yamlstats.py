import unittest
from . import main


class TestYamlStats(unittest.TestCase):

    def test_name_is_not_duplicated_in_files_1_and_2(self):
        # act
        response = main.run('examples/file1.yaml', 'examples/file2.yaml')

        # assert
        self.assertNotIn("name is the same in both files", response)

    def test_name_is_duplicated_in_files_2_and_3(self):
        # act
        response = main.run('examples/file2.yaml', 'examples/file3.yaml')

        # assert
        self.assertIn("name is the same in both files", response)

    def test_name_has_different_values_in_files_1_and_3(self):
        # arrange
        ys = main.YamlStats()
        ys.load('examples/file1.yaml', 'examples/file3.yaml')
        # act
        response = ys.check_for_differences()

        # assert
        self.assertIn({'file_a': {'file_name': 'examples/file1.yaml', 'value': 'Martin Devloper'}, 'key': 'name',
                       'file_b': {'file_name': 'examples/file3.yaml', 'value': "Martin D'vloper"}}, response)

    def test_it_prints_out_a_table(self):
        # arrange
        ys = main.YamlStats()

        # act
        response = ys.run('examples/file1.yaml', 'examples/file3.yaml', True)

        # assert
        self.assertIn('examples/file1.yaml', response.__str__())
