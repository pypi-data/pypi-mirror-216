import unittest
import os
from deepdiff import DeepDiff

from steam_sdk.data import DataModelMagnet as md
from steam_sdk.data.DataConductor import Conductor
from steam_sdk.parsers.ParserYAML import dict_to_yaml
from steam_sdk.parsers.ParserYAML import yaml_to_data

class TestDataModel(unittest.TestCase):

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
            Check that DataModelMagnet generates a structure with the same keys as a reference file
        """
        # arrange
        generated_file = os.path.join('output',      'model_data_magnet_TEST_default.yaml')
        reference_file = os.path.join('references', 'data_model_magnet_REFERENCE_default.yaml')

        # If test output file already exists, delete it
        if os.path.isfile(generated_file) == True:
            os.remove(generated_file)

        # act
        data: md.DataModelMagnet = md.DataModelMagnet()
        dict_to_yaml(data.dict(by_alias=True), generated_file, list_exceptions=['Conductors'])
        # assert
        # Check that the generated file exists
        self.assertTrue(os.path.isfile(generated_file))

        # Check that the generated file is identical to the reference
        # TODO: Check that order of the keys is the same
        a = yaml_to_data(generated_file)
        b = yaml_to_data(reference_file)
        ddiff = DeepDiff(a, b, ignore_order=False)
        if len(ddiff) > 0:
            [print(ddiff[i]) for i in ddiff]
        self.assertTrue(len(ddiff)==0)


    def test_writeToFile_ribbon(self):
        """
            Check that DataModelMagnet generates a structure with the same keys as a reference file
        """
        # arrange
        generated_file = os.path.join('output',      'model_data_magnet_TEST_ribbon.yaml')
        reference_file =  os.path.join('references', 'data_model_magnet_REFERENCE_ribbon.yaml')

        # If test output file already exists, delete it
        if os.path.isfile(generated_file) == True:
            os.remove(generated_file)

        # act
        data: md.DataModelMagnet = md.DataModelMagnet()
        data.Conductors[0] = Conductor(cable={'type': 'Ribbon'}, strand={'type': 'Rectangular'}, Jc_fit={'type': 'CUDI1'})
        dict_to_yaml(data.dict(by_alias=True), generated_file, list_exceptions=['Conductors'])

        # assert
        # Check that the generated file exists
        self.assertTrue(os.path.isfile(generated_file))

        # Check that the generated file is identical to the reference
        # TODO: Check that order of the keys is the same
        a = yaml_to_data(generated_file)
        b = yaml_to_data(reference_file)
        ddiff = DeepDiff(a, b, ignore_order=False)
        if len(ddiff) > 0:
            [print(ddiff[i]) for i in ddiff]
        self.assertTrue(len(ddiff)==0)


    def test_writeToFile_mono(self):
        """
            Check that DataModelMagnet generates a structure with the same keys as a reference file
        """
        # arrange
        generated_file = os.path.join('output', 'model_data_magnet_TEST_mono.yaml')
        reference_file = os.path.join('references', 'data_model_magnet_REFERENCE_mono.yaml')

        # If test output file already exists, delete it
        if os.path.isfile(generated_file) == True:
            os.remove(generated_file)

        # arrange - assign values to a few keys
        data_model: md.DataModelMagnet = md.DataModelMagnet()
        data_model.Conductors[0] = Conductor(cable={'type': 'Mono'}, strand={'type': 'Rectangular'}, Jc_fit={'type': 'CUDI1'})
        data_model.Power_Supply.I_control_LUT = [0, 0]  # example of list
        data_model.CoilWindings.electrical_pairs.group_together = [[1, 2], [3, 4]]  # example of list of lists

        # act
        # data_to_yaml(data_model, generated_file, list_exceptions=['Conductors'])
        data_dict = data_model.dict()  # Convert the DataModelMagnet object to a dictionary
        dict_to_yaml(data_dict, generated_file, list_exceptions=['Conductors'])

        # assert
        # Check that the generated file exists
        self.assertTrue(os.path.isfile(generated_file))

        # Check that the generated file is identical to the reference
        # TODO: Check that order of the keys is the same
        a = yaml_to_data(generated_file)
        b = yaml_to_data(reference_file)
        ddiff = DeepDiff(a, b, ignore_order=False)
        if len(ddiff) > 0:
            [print(ddiff[i]) for i in ddiff]
        self.assertTrue(len(ddiff) == 0)


    def test_loadYamlFile(self):
        """
            Check that a yaml file can be loaded
        """
        # arrange
        reference_file =  os.path.join('references', 'data_model_magnet_REFERENCE_default.yaml')

        # act
        dictionary = yaml_to_data(reference_file)
        magnet_input = md.DataModelMagnet(**dictionary)

        # assert
        # TODO Test always passes! Need to add a check of loaded variables.
        print('\nTest always passes! Need to add a check of loaded variables.\n')
        print(magnet_input)
        print(magnet_input.Sources)
        print(magnet_input.Options_LEDET)

