import unittest
from . import main


class TestYamlStats(unittest.TestCase):

    def test_name_is_not_duplicated_in_files_1_and_2(self):
        # act
        response = main.run('examples/file1.yaml', 'examples/file2.yaml')

        # assert
        self.assertNotRegex(response.__str__(), r'name')

    def test_name_is_duplicated_in_files_2_and_3(self):
        # act
        response = main.run('examples/file2.yaml', 'examples/file3.yaml')

        # assert
        self.assertRegex(response.__str__(), r'name')

    def test_name_has_different_values_in_files_1_and_3(self):
        # arrange
        ys = main.YamlStats()
        ys.load('examples/file1.yaml', 'examples/file3.yaml')
        # act
        response = ys.check_for_differences()

        # assert
        self.assertIn({'file_a': {'file_name': 'examples/file1.yaml', 'value': 'Martin Devloper'}, 'key': 'name',
                       'file_b': {'file_name': 'examples/file3.yaml', 'value': "Martin D'vloper"}}, response)

    def test_there_are_additional_keys_in_files_2_and_3(self):
        # arrange
        ys = main.YamlStats()
        ys.load('examples/file2.yaml', 'examples/file3.yaml')
        # act
        response = ys.check_for_additional_keys()

        # assert
        self.assertEqual({'file_a': ['location'], 'file_b': ['university']}, response)

    def test_it_prints_out_a_table_of_differences(self):
        # arrange
        ys = main.YamlStats()

        # act
        response = ys.run('examples/file1.yaml', 'examples/file3.yaml', show_differences=True, show_additional=False)

        # assert
        self.assertRegex(response.__str__(), r'languages')

    def test_it_prints_out_a_table_of_additional_keys(self):
        # arrange
        ys = main.YamlStats()

        # act
        response = ys.run('examples/file2.yaml', 'examples/file3.yaml', show_differences=False, show_additional=True)

        # assert
        self.assertIn('university', response.__str__())
        self.assertIn('location', response.__str__())
