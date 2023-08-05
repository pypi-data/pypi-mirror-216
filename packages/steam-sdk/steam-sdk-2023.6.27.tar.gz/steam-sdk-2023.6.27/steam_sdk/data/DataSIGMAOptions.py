from pathlib import Path
from typing import (Dict, List, Union, Literal)

from pydantic import BaseModel

from steam_sdk.data.DataRoxieParser import RoxieData


class MultipoleRoxieGeometry(BaseModel):
    """
        Class for FiQuS multipole Roxie data (.geom)
    """
    Roxie_Data: RoxieData = RoxieData()

class Jc_FitSIGMA(BaseModel):
    type: str = None
    C1_CUDI1: str = None
    C2_CUDI1: str = None

class StrandSIGMA(BaseModel):
        filament_diameter: float = None
        diameter: float = None
        f_Rho_effective: float = None
        fil_twist_pitch: float = None
        RRR: float = None
        T_ref_RRR_high: float = None
        Cu_noCu_in_strand: float = None


class TimeVectorSolutionSIGMA(BaseModel):
    time_step: List[List[float]] = None


class Simulation(BaseModel):
    generate_study: bool = None
    study_type: str = None
    make_batch_mode_executable: bool = None
    nbr_elements_mesh_width: int = None
    nbr_elements_mesh_height: int = None


class Physics(BaseModel):
    FLAG_M_pers: int = None
    FLAG_ifcc: int = None
    FLAG_iscc_crossover: int = None
    FLAG_iscc_adjw: int = None
    FLAG_iscc_adjn: int = None
    tauCC_PE: int = None


class QuenchInitialization(BaseModel):
    PARAM_time_quench: float = None
    FLAG_quench_all: int = None
    FLAG_quench_off: int = None
    num_qh_div: List[int] = None
    quench_init_heat: float = None
    quench_init_HT: List[str] = None
    quench_stop_temp: float = None


class Out2DAtPoints(BaseModel):
    coordinate_source: Path = None
    variables: List[str] = None
    time: List[List[float]] = None
    map2d: str = None


class Out1DVsTimes(BaseModel):
    variables: List[str] = None
    time: List[List[float]] = None


class Out1DVsAllTimes(BaseModel):
    variables: List[str] = None


class Postprocessing(BaseModel):
    out_2D_at_points: Out2DAtPoints = Out2DAtPoints()
    out_1D_vs_times: Out1DVsTimes = Out1DVsTimes()
    out_1D_vs_all_times: Out1DVsAllTimes = Out1DVsAllTimes()


class QuenchHeatersSIGMA(BaseModel):
    quench_heater_positions: List[List[int]] = None
    th_coils: List[float] = None


class SIGMAOptions(BaseModel):
    time_vector_solution: TimeVectorSolutionSIGMA = TimeVectorSolutionSIGMA()
    simulation: Simulation = Simulation()
    physics: Physics = Physics()
    quench_initialization: QuenchInitialization = QuenchInitialization()
    postprocessing: Postprocessing = Postprocessing()
    quench_heaters: QuenchHeatersSIGMA = QuenchHeatersSIGMA()


