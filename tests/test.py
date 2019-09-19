from yamlstats import yamlstats
import unittest


class TestYamlStats(unittest.TestCase):

    def test_name_is_not_duplicated_in_files_1_and_2(self):
        # arrange
        ys = yamlstats.YamlStats()
        ys.load('examples/file1.yaml', 'examples/file2.yaml')
        # act
        response = yamlstats.run('examples/file1.yaml', 'examples/file2.yaml')

        # assert
        self.assertNotIn("name is the same in both files", response)

    def test_name_is_duplicated_in_files_2_and_3(self):
        # act
        response = yamlstats.run('examples/file2.yaml', 'examples/file3.yaml')

        # assert
        self.assertIn("name is the same in both files", response)
