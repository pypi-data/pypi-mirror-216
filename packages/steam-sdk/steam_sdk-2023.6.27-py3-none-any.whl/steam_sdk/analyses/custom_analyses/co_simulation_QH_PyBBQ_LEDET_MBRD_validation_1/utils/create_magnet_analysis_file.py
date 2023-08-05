from steam_sdk.data.DataAnalysis import SetUpFolder, MakeModel, RunSimulation, RunViewer, CalculateMetrics

def create_magnet_analysis_file(aSTEAM, magnet_name, software, simulation_numbers, viewer_path, list_events, metrics_to_calculate, variables_to_analyze):

    """
    Function to fill the before created analysis file for the magnet simulation
    :param aSTEAM: Dictionary that contains all variable input variables
    :param magnet_name: Name of the magnet of the analyzed magnet
    :param software: used software
    :param simulation_numbers: list of simulation numbers
    :param viewer_path: path where the csv.file for the viewer is saved
    :param list_events: list of the events given in the viewer csv which should be plotted and used for metrics
    :param metrics_to_calculate: list of the metrics which should be conducted
    :param variables_to_analyze: signal names given in the viewer config file which should be used for the metrics
    :return:
    """

    aSTEAM.data_analysis.GeneralParameters.model.name = magnet_name

    # Add step to set up LEDET folder model
    step_setup_folder = 'setup_folder'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_setup_folder] = SetUpFolder(type='SetUpFolder')
    aSTEAM.data_analysis.AnalysisStepDefinition[step_setup_folder].simulation_name = f'{magnet_name}'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_setup_folder].software = [software[1]]
    aSTEAM.data_analysis.AnalysisStepSequence.append(step_setup_folder)

    # Add step to import reference model
    step_ref_model = 'make_reference_model'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model] = MakeModel(type='MakeModel')
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].model_name = 'BM'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].file_model_data = f'{magnet_name}'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].case_model = 'magnet'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].software = []
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].simulation_name = None
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].simulation_number = None
    aSTEAM.data_analysis.AnalysisStepDefinition[
        step_ref_model].flag_build = True  # important to keep True since it calculates the edited map2d file
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].flag_dump_all = False
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].verbose = False
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].flag_plot_all = False
    aSTEAM.data_analysis.AnalysisStepDefinition[step_ref_model].flag_json = False
    aSTEAM.data_analysis.AnalysisStepSequence.append(step_ref_model)

    # prepare step run_simulation
    step_run_simulation = f'RunSimList_{software[1]}'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation] = RunSimulation(type='RunSimulation')
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].software = software[1]
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].simulation_name = f'{magnet_name}'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].simulation_numbers = simulation_numbers
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].simFileType = None

    # prepare step run_viewer
    step_run_simulation = 'run_viewer'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation] = RunViewer(type='RunViewer')
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].viewer_name = 'V'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].file_name_transients = f'{viewer_path}'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].list_events = list_events
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].flag_analyze = True
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].flag_display = False
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].flag_save_figures = True
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].verbose = True

    # prepare calculate_metrics
    step_run_simulation = 'calculate_metrics'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation] = CalculateMetrics(type='CalculateMetrics')
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].metrics_name = 'metrics_validation_MBRD'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].viewer_name = 'V'
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].metrics_to_calculate = metrics_to_calculate
    aSTEAM.data_analysis.AnalysisStepDefinition[step_run_simulation].variables_to_analyze =variables_to_analyze