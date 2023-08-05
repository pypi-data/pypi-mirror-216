from pydantic import BaseModel
from typing import List

from steam_sdk.data.DataFiQuS import RunFiQuS

from steam_sdk.data.DataFiQuS import CCTGeometryCWSInputs
from steam_sdk.data.DataFiQuS import CCTGeometryAir
from steam_sdk.data.DataFiQuS import CCTMesh
from steam_sdk.data.DataFiQuS import CCTSolveWinding
from steam_sdk.data.DataFiQuS import CCTSolveFormer
from steam_sdk.data.DataFiQuS import CCTSolveAir

from steam_sdk.data.DataFiQuS import CWSGeometry
from steam_sdk.data.DataFiQuS import CWSMesh
from steam_sdk.data.DataFiQuS import CWSSolve
from steam_sdk.data.DataFiQuS import CWSPostproc

from steam_sdk.data.DataFiQuS import MultipoleGeometry
from steam_sdk.data.DataFiQuS import MultipoleMesh
from steam_sdk.data.DataFiQuS import MultipoleSolve
from steam_sdk.data.DataFiQuS import MultipolePostProc

from steam_sdk.data.DataFiQuS import Pancake3DGeometry
from steam_sdk.data.DataFiQuS import Pancake3DMesh
from steam_sdk.data.DataFiQuS import Pancake3DSolve


class CCTGeometryCWSInputsOptions(CCTGeometryCWSInputs):
    pass

class CCTGeometryWindingOptions(BaseModel):  # Geometry related windings _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = None  # name to use in gmsh and getdp
    r_wms: List[float] = None  # radius of the middle of the winding
    ndpts: List[int] = None  # number of divisions of turn, i.e. number of hexagonal elements for each turn
    ndpt_ins: List[int] = None  # number of divisions of terminals in
    ndpt_outs: List[int] = None  # number of divisions of terminals in
    lps: List[float] = None  # layer pitch
    alphas: List[float] = None  # tilt angle
    wwws: List[float] = None  # winding wire widths (assuming rectangular)
    wwhs: List[float] = None  # winding wire heights (assuming rectangular)


class CCTGeometryFormerOptions(BaseModel):  # Geometry related formers _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = None  # name to use in gmsh and getdp
    z_mins: List[float] = None  # extend of former  in negative z direction
    z_maxs: List[float] = None  # extend of former in positive z direction
    rotates: List[float] = None  # rotation of the former around its axis in degrees


class CCTGeometryAirOptions(CCTGeometryAir):  # Geometry related air_region _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    pass


class CCTGeometryOptions(BaseModel):
    """
        Level 2: Class for FiQuS CCT for FiQuS input
    """
    CWS_inputs: CCTGeometryCWSInputsOptions = CCTGeometryCWSInputsOptions()
    windings: CCTGeometryWindingOptions = CCTGeometryWindingOptions()
    formers: CCTGeometryFormerOptions = CCTGeometryFormerOptions()
    air: CCTGeometryAirOptions = CCTGeometryAirOptions()


class CCTMeshOptions(CCTMesh):
    pass


class CCTSolveWindingOptions(CCTSolveWinding):  # Solution time used windings _inputs (materials and BC)
    pass


class CCTSolveFormerOptions(CCTSolveFormer):  # Solution time used formers _inputs (materials and BC)
    pass


class CCTSolveAirOptions(CCTSolveAir):  # Solution time used air _inputs (materials and BC)
    pass


class CCTSolveOptions(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    windings: CCTSolveWindingOptions = CCTSolveWindingOptions()  # windings solution time _inputs
    formers: CCTSolveFormerOptions = CCTSolveFormerOptions()  # former solution time _inputs
    air: CCTSolveAirOptions = CCTSolveAirOptions()  # air solution time _inputs
    pro_template: str = None  # file name of .pro template file
    variables: List[str] = None  # Name of variable to post-process by GetDP, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by GetDP, line Winding_1
    file_exts: List[str] = None  # Name of file extensions to post-process by GetDP, like .pos


class CCTPostprocOptions(BaseModel):
    """
        Class for FiQuS CCT input file
    """
    additional_outputs: List[str] = None  # Name of software specific input files to prepare, like :LEDET3D
    fqpcs_export_trim_tol: List[float] = None  # this multiplier times winding extend gives 'z' coordinate above(below) which hexes are exported for LEDET, length of this list must match number of fqpls
    variables: List[str] = None  # Name of variable to post-process by python Gmsh API, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by python Gmsh API, line Winding_1
    file_exts: List[str] = None  # Name of file extensions o post-process by python Gmsh API, like .pos


class CCT_MagnetOptions(BaseModel):
    """
        Class for FiQuS CCT
    """
    geometry: CCTGeometryOptions = CCTGeometryOptions()
    mesh: CCTMeshOptions = CCTMeshOptions()
    solve: CCTSolveOptions = CCTSolveOptions()
    postproc: CCTPostprocOptions = CCTPostprocOptions()


class MultipoleGeometryOptions(MultipoleGeometry):
    pass


class MultipoleMeshOptions(MultipoleMesh):
    pass


class MultipoleSolveOptions(MultipoleSolve):
    pass


class MultipolePostProcOptions(MultipolePostProc):
    pass


class Multipole_magnetOptions(BaseModel):
    geometry: MultipoleGeometryOptions = MultipoleGeometryOptions()
    mesh: MultipoleMeshOptions = MultipoleMeshOptions()
    solve: MultipoleSolveOptions = MultipoleSolveOptions()
    postproc: MultipolePostProcOptions = MultipolePostProcOptions()



class Pancake3DGeometryOptions(Pancake3DGeometry):
    pass


class Pancake3DMeshOptions(Pancake3DMesh):
    pass


class Pancake3DSolveOptions(Pancake3DSolve):
    pass


class Pancake3D_magnetOptions(BaseModel):
    geometry: Pancake3DGeometryOptions = Pancake3DGeometryOptions()
    mesh: Pancake3DMeshOptions = Pancake3DMeshOptions()
    solve: Pancake3DSolveOptions = Pancake3DSolveOptions()


class RunFiQuS(RunFiQuS):
    pass


class CWSGeometryOptions(CWSGeometry):
    pass

class CWSMeshOptions(CWSMesh):
    pass

class CWSSolveOptions(CWSSolve):
    pass

class CWSPostprocOptions(CWSPostproc):
    pass

class CWS_MagnetOptions(BaseModel):
    """
        Class for FiQuS CWS
    """
    geometry: CWSGeometryOptions = CWSGeometryOptions()
    mesh: CWSMeshOptions = CWSMeshOptions()
    solve: CWSSolveOptions = CWSSolveOptions()
    postproc: CWSPostprocOptions = CWSPostprocOptions()


class FiQuSOptions(BaseModel):
    """
        This is data structure of FiQuS Options in STEAM SDK
    """
    run: RunFiQuS = RunFiQuS()
    cct: CCT_MagnetOptions = CCT_MagnetOptions()
    cws: CWS_MagnetOptions = CWS_MagnetOptions()
    multipole: Multipole_magnetOptions = Multipole_magnetOptions()
    Pancake3D: Pancake3D_magnetOptions = Pancake3D_magnetOptions()