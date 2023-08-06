import os
import sys
import subprocess


class DriverFiQuS:
    """
        Class to drive FiQuS models
    """
    def __init__(self, FiQuS_path='', path_folder_FiQuS=None, path_folder_FiQuS_input=None, verbose=False, GetDP_path=None):
        self.FiQuS_path = FiQuS_path
        self.path_folder_FiQuS = path_folder_FiQuS
        self.path_folder_FiQuS_input = path_folder_FiQuS_input
        self.verbose = verbose
        self.GetDP_path = GetDP_path
        if verbose:
            print('path_exe =          {}'.format(FiQuS_path))
            print('path_folder_FiQuS = {}'.format(path_folder_FiQuS))

        # now fiqus is called with subprocess call
        # if FiQuS_path !='pypi':
        #     sys.path.insert(0, FiQuS_path)
        # from fiqus.MainFiQuS import MainFiQuS as MF
        # self.MainFiQuS = MF

    def run_FiQuS(self, sim_file_name: str, output_directory: str = 'output', verbose: bool = False):
        full_path_input = os.path.join(self.path_folder_FiQuS_input, sim_file_name + '.yaml')
        full_path_output = os.path.join(self.path_folder_FiQuS, output_directory)

        # This old way of running fiqus does not work due to issues with matlab runtime engine after getdp gets used for solve.
        #return self.MainFiQuS(input_file_path=full_path_input, model_folder=full_path_output, GetDP_path=self.GetDP_path).summary

        # For now this way of running fiqus is needed due to matlab runtime engine issue
        subprocess.call([
            'python',
            os.path.join(self.FiQuS_path, 'fiqus', 'MainFiQuS.py'),
            '--in', full_path_input,
            '--out', full_path_output,
            '--getdp', self.GetDP_path,
            ])
