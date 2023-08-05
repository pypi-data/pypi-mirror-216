import unittest
import os
from deepdiff import DeepDiff

from steam_sdk.data.DataModelConductor import DataModelConductor
from steam_sdk.parsers.ParserYAML import yaml_to_data
from steam_sdk.parsers.ParserYAML import dict_to_yaml


class TestDataModelConductor(unittest.TestCase):

    def setUp(self) -> None:
        """
            This function is executed before each test in this class
        """
        self.current_path = os.getcwd()
        os.chdir(os.path.dirname(__file__))  # move to the directory where this file is located
        print('\nCurrent folder:          {}'.format(self.current_path))
        print('\nTest is run from folder: {}'.format(os.getcwd()))

    def tearDown(self) -> None:
        """
            This function is executed after each test in this class
        """
        os.chdir(self.current_path)  # go back to initial folder


    def test_writeToFile_default(self):
        """
            Check that DataModelCircuit generates a structure with the same keys as a reference file
        """
        # arrange
        generated_file = os.path.join('output',      'data_model_conductor_TEST.yaml')
        reference_file =  os.path.join('references', 'data_model_conductor_REFERENCE.yaml')

        # If test output file already exists, delete it
        if os.path.isfile(generated_file) == True:
            os.remove(generated_file)

        # act
        data: DataModelConductor = DataModelConductor()
        dict_to_yaml(data.dict(), generated_file, list_exceptions=['Conductors'])
        # with open(generated_file, 'w') as yaml_file:
        #     yaml.dump(data.dict(), yaml_file, default_flow_style=False, sort_keys=False)

        # assert
        # Check that the generated file exists
        self.assertTrue(os.path.isfile(generated_file))

        # Check that the generated file is identical to the reference
        # TODO: Check that order of the keys is the same
        a = yaml_to_data(generated_file)
        b = yaml_to_data(reference_file)
        print(f'Comparing: output file: {generated_file} with reference file {reference_file}')
        ddiff = DeepDiff(a, b, ignore_order=False)
        if len(ddiff) > 0:
            print('Diffence found:')
            [print(ddiff[i]) for i in ddiff]
        self.assertTrue(len(ddiff)==0)
