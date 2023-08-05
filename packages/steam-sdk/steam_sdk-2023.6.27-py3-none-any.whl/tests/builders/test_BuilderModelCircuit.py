import unittest
import os

from steam_sdk.builders.BuilderModel import BuilderModel
from steam_sdk.parsers.ParserPSPICE import ParserPSPICE


class TestBuilderModel_Circuits(unittest.TestCase):

    def setUp(self) -> None:
        """
            This function is executed before each test in this class
        """
        self.current_path = os.getcwd()
        os.chdir(os.path.dirname(__file__))  # move the directory where this file is located
        print('\nCurrent folder:          {}'.format(self.current_path))
        print('Test is run from folder: {}'.format(os.getcwd()))

    def tearDown(self) -> None:
        """
            This function is executed after each test in this class
        """
        os.chdir(self.current_path)  # go back to initial folder


    def test_BuilderModel_initialization(self):
        """
            Check that BuilderData object can be initialized without providing any input
        """
        BM = BuilderModel(file_model_data=None, software=None, case_model='circuit', flag_build=False, verbose=True)


    def test_BuilderModel_PSPICE_multiple(self):
        circuit_names = ['ROD', 'IPQ_2magnets', 'IPQ_4magnets', 'RB', 'RCD_RCO', 'RCS',
                         'RQD_47magnets', 'RQD_51magnets', 'RQX', 'RQX_HL-LHC', 'RU',
                         'SIS100_DP', 'SIS100_F1', 'SIS100_F2', 'SIS100_QD']
        for circuit_name in circuit_names:
            print('Circuit: {}'.format(circuit_name))
            self.compare_to_reference_PSPICE(circuit_name, verbose=False)


    def test_BuilderModel_load_circuit_parameters_from_csv(self):
        # arrange
        file_model_data = os.path.join('input', 'file_circuit_model_TEST_LOAD_PARAMETERS.yaml')
        path_file_circuit_parameters = os.path.join('input', 'file_circuit_parameters_TEST_LOAD_PARAMETERS.csv')
        BM = BuilderModel(file_model_data=file_model_data, software=['PSPICE'], case_model='circuit',
                          output_path=os.path.join('output', 'PSPICE'), flag_build=True, flag_dump_all=False, flag_plot_all=False, verbose=True)

        # check that the initial value is unchanged
        self.assertEqual(BM.circuit_data.GlobalParameters.global_parameters['dummy_1'], '654.321')

        # act
        BM.load_circuit_parameters_from_csv(input_file_name=path_file_circuit_parameters, selected_circuit_name='DUMMY_NAME')

        # assert - # check that the initial value is now changed
        self.assertEqual(BM.circuit_data.GlobalParameters.global_parameters['dummy_1'], '123.456')


    ###############################################################################################
    # Helper methods
    def compare_to_reference_PSPICE(self, circuit_name, verbose=False, flag_plot_all=False):
        """
            Helper method called by other methods
            Check that BuilderModel object can be initialized, read a model input yaml file, and generate a PSPICE netlist
            This test checks:
             - NOTHING YET

            circuit_name: can be any circuit name in the library
        """

        # arrange
        max_relative_error = 1e-6  # Maximum accepted relative error for excel, csv and map2d file comparison

        file_model_data      = os.path.join('model_library', 'circuits', circuit_name, 'input',  'modelData_' + circuit_name + '.yaml')
        output_path          = os.path.join('model_library', 'circuits', circuit_name, 'output')
        input_file_REFERENCE = os.path.join('references',    'circuits', circuit_name,           circuit_name + '_REFERENCE.cir')
        input_file_GENERATED = os.path.join('model_library', 'circuits', circuit_name, 'output', circuit_name + '.cir')

        # act
        BM = BuilderModel(file_model_data=file_model_data, software=['PSPICE'], case_model='circuit',
                          flag_build=True, flag_dump_all=False, flag_plot_all=flag_plot_all,
                          output_path=output_path,
                          verbose=verbose)

        # assert 1 - Check that the generated PSPICE file has the same input as the reference
        # TODO: Add ParserPSPICE.ComparePSPICEParameters()
        pPSPICE_1 = ParserPSPICE(None)
        pPSPICE_1.read_netlist(input_file_GENERATED, verbose=False)
        pPSPICE_2 = ParserPSPICE(None)
        pPSPICE_2.read_netlist(input_file_REFERENCE, verbose=False)
        self.assertEqual(pPSPICE_1.circuit_data, pPSPICE_2.circuit_data)
