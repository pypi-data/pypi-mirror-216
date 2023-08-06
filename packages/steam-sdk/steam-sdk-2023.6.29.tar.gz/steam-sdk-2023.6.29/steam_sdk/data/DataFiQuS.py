from pydantic import BaseModel
import pydantic
from typing import (Union, Dict, List, Literal)

from steam_sdk.data.DataConductor import ConstantJc, Bottura, CUDI3, Bordini, BSCCO_2212_LBNL, CUDI1, Summers, Round, \
    Rectangular, Rutherford, Mono, Ribbon
from steam_sdk.data.DataRoxieParser import RoxieData


from steam_sdk.data.DataModelCommon import Circuit
from steam_sdk.data.DataModelCommon import PowerSupply

class CCTGeometryCWSInputs(BaseModel):
    """
        Level 3: Class for controlling if and where the conductor files and brep files are written for the CWS (conductor with step) workflow
    """
    write: bool = False             # if true only conductor and brep files are written, everything else is skipped.
    output_folder: str = None       # this is relative path to the input file location


class CCTGeometryWinding(BaseModel):  # Geometry related windings _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = None  # name to use in gmsh and getdp
    r_wms: List[float] = None  # radius of the middle of the winding
    n_turnss: List[float] = None  # number of turns
    ndpts: List[int] = None  # number of divisions of turn, i.e. number of hexagonal elements for each turn
    ndpt_ins: List[int] = None  # number of divisions of terminals ins
    ndpt_outs: List[int] = None  # number of divisions of terminals outs
    lps: List[float] = None  # layer pitch
    alphas: List[float] = None  # tilt angle
    wwws: List[float] = None  # winding wire widths (assuming rectangular)
    wwhs: List[float] = None  # winding wire heights (assuming rectangular)


class CCTGeometryFQPCs(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = []  # name to use in gmsh and getdp
    fndpls: List[int] = None  # fqpl number of divisions per length
    fwws: List[float] = None  # fqpl wire widths (assuming rectangular) for theta = 0 this is x dimension
    fwhs: List[float] = None  # fqpl wire heights (assuming rectangular) for theta = 0 this is y dimension
    r_ins: List[float] = None  # radiuses for inner diameter for fqpl (radial (or x direction for theta=0) for placing the fqpl
    r_bs: List[float] = None  # radiuses for bending the fqpl by 180 degrees
    n_sbs: List[int] = None  # number of 'bending segmetns' for the 180 degrees turn
    thetas: List[float] = None  # rotation in deg from x+ axis towards y+ axis about z axis.
    z_starts: List[str] = None  # which air boundary to start at. These is string with either: z_min or z_max key from the Air region.
    z_ends: List[float] = None  # z coordinate of loop end


class CCTGeometryFormer(BaseModel):  # Geometry related formers _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = None  # name to use in gmsh and getdp
    r_ins: List[float] = None  # inner radius
    r_outs: List[float] = None  # outer radius
    z_mins: List[float] = None  # extend of former  in negative z direction
    z_maxs: List[float] = None  # extend of former in positive z direction
    rotates: List[float] = None  # rotation of the former around its axis in degrees


class CCTGeometryAir(BaseModel):  # Geometry related air_region _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    name: str = None  # name to use in gmsh and getdp
    sh_type: str = None  # cylinder or cuboid are possible
    ar: float = None  # if box type is cuboid a is taken as a dimension, if cylinder then r is taken
    z_min: float = None  # extend of air region in negative z direction
    z_max: float = None  # extend of air region in positive z direction


class CCTGeometry(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    CWS_inputs: CCTGeometryCWSInputs = CCTGeometryCWSInputs()
    windings: CCTGeometryWinding = CCTGeometryWinding()
    fqpcs: CCTGeometryFQPCs = CCTGeometryFQPCs()
    formers: CCTGeometryFormer = CCTGeometryFormer()
    air: CCTGeometryAir = CCTGeometryAir()


class CCTMesh(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    MaxAspectWindings: float = None  # used in transfinite mesh_generators settings to define mesh_generators size along two longer lines of hex elements of windings
    ThresholdSizeMin: float = None  # sets field control of Threshold SizeMin
    ThresholdSizeMax: float = None  # sets field control of Threshold SizeMax
    ThresholdDistMin: float = None  # sets field control of Threshold DistMin
    ThresholdDistMax: float = None  # sets field control of Threshold DistMax


class CCTSolveWinding(BaseModel):  # Solution time used windings _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    currents: List[float] = None  # current in the wire
    sigmas: List[float] = None  # electrical conductivity
    mu_rs: List[float] = None  # relative permeability

class CCTSolveFormer(BaseModel):  # Solution time used formers _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    sigmas: List[float] = None  # electrical conductivity
    mu_rs: List[float] = None  # relative permeability

class CCTSolveFQPCs(BaseModel):  # Solution time used windings _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    currents: List[float] = []  # current in the wire
    sigmas: List[float] = []  # electrical conductivity
    mu_rs: List[float] = []  # relative permeability

class CCTSolveAir(BaseModel):  # Solution time used air _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    sigma: float = None  # electrical conductivity
    mu_r: float = None  # relative permeability


class CCTSolve(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    windings: CCTSolveWinding = CCTSolveWinding()  # windings solution time _inputs
    formers: CCTSolveFormer = CCTSolveFormer()  # former solution time _inputs
    fqpcs: CCTSolveFQPCs = CCTSolveFQPCs()  # fqpls solution time _inputs
    air: CCTSolveAir = CCTSolveAir()  # air solution time _inputs
    pro_template: str = None  # file name of .pro template file
    variables: List[str] = None  # Name of variable to post-process by GetDP, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by GetDP, line Winding_1
    file_exts: List[str] = None  # Name of file extensions to post-process by GetDP, like .pos


class CCTPostproc(BaseModel):
    """
        Level 2: Class for  FiQuS CCT
    """
    windings_wwns: List[int] = None  # wires in width direction numbers
    windings_whns: List[int] = None  # wires in height direction numbers
    additional_outputs: List[str] = None  # Name of software specific input files to prepare, like :LEDET3D
    winding_order: List[int] = None
    fqpcs_export_trim_tol: List[
        float] = None  # this multiplier times winding extend gives 'z' coordinate above(below) which hexes are exported for LEDET, length of this list must match number of fqpls
    variables: List[str] = None  # Name of variable to post-process by python Gmsh API, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by python Gmsh API, line Winding_1
    file_exts: List[str] = None  # Name of file extensions o post-process by python Gmsh API, like .pos


class CCT(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    type: Literal['CCT_straight']
    geometry: CCTGeometry = CCTGeometry()
    mesh: CCTMesh = CCTMesh()
    solve: CCTSolve = CCTSolve()
    postproc: CCTPostproc = CCTPostproc()


class CWSGeometryConductors(BaseModel):  # Conductor file data for geometry building
    """
        Level 2: Class for FiQuS CWS
    """
    resample: List[int] = None
    skip_middle_from: List[int] = None  # decides which bricks are skipped in fuse operation, basically only a few bricks should overlap with the former.
    skip_middle_to: List[int] = None  # decides which bricks are skipped in fuse operation, basically only a few bricks should overlap with the former.
    combine_from: List[List[int]] = None
    combine_to: List[List[int]] = None
    file_names_large: List[str] = None
    file_names: List[str] = None  # Inner_17.1mm #[inner_FL, outer_FL] #
    ends_need_trimming: bool = False    # If there are windings "sticking out" of the air region this needs to set to True. It removes 2 volumes per winding after the fragment operation


class CWSGeometryFormers(BaseModel):  # STEP file data for geometry building
    """
        Level 2: Class for FiQuS CWS
    """
    file_names: List[str] = None    # STEP file names to use
    air_pockets: List[int] = None   # number of air pockets (for e.g. for heater or temperature sensor pads) on the formers


class CWSGeometryShells(BaseModel):  # STEP file data for geometry building
    """
        Level 2: Class for FiQuS CWS
    """
    file_names: List[str] = None    # STEP file names to use


class CWSGeometryAir(BaseModel):  # Geometry related air_region _inputs
    """
        Level 2: Class for FiQuS CWS
    """
    name: str = None  # name to use in gmsh and getdp
    sh_type: str = None  # cylinder or cuboid are possible
    ar: float = None  # if box type is cuboid 'a' is taken as a dimension, if cylinder then 'r' is taken
    z_min: float = None  # extend of air region in negative z direction, for cylinder_cov this is ignored
    z_max: float = None  # extend of air region in positive z direction, for cylinder_cov this is ignored


class CWSGeometry(BaseModel):
    """
        Level 2: Class for FiQuS CWS for FiQuS input
    """
    conductors: CWSGeometryConductors = CWSGeometryConductors()
    formers: CWSGeometryFormers = CWSGeometryFormers()
    shells: CWSGeometryShells = CWSGeometryShells()
    air: CWSGeometryAir = CWSGeometryAir()


class CWSSolveConductors(BaseModel):  # Solution time used Conductor _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CWS
    """
    currents: List[float] = None  # current in the wire
    sigmas: List[float] = None  # electrical conductivity
    mu_rs: List[float] = None  # relative permeability


class CWSSolveFormers(BaseModel):  # Solution time used fqpls _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CWS
    """
    sigmas: List[float] = []  # electrical conductivity
    mu_rs: List[float] = []  # relative permeability


class CWSSolveShells(BaseModel):  # Solution time used fqpls _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CWS
    """
    sigmas: List[float] = []  # electrical conductivity
    mu_rs: List[float] = []  # relative permeability


class CWSSolveAir(BaseModel):  # Solution time used air _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CWS
    """
    sigma: float = None  # electrical conductivity
    mu_r: float = None  # relative permeability


class CWSSolve(BaseModel):
    """
        Level 2: Class for FiQuS CWS
    """
    conductors: CWSSolveConductors = CWSSolveConductors()  # windings solution time _inputs
    formers: CWSSolveFormers = CWSSolveFormers()  # formers solution time _inputs
    shells: CWSSolveShells = CWSSolveShells()   # shells solution time _inputs
    air: CWSSolveAir = CWSSolveAir()  # air solution time _inputs
    pro_template: str = None  # file name of .pro template file
    variables: List[str] = None  # Name of variable to post-process by GetDP, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by GetDP, line Winding_1
    file_exts: List[str] = None  # Name of file extensions to post-process by GetDP, like .pos


class CWSMesh(BaseModel):
    """
        Level 2: Class for FiQuS CWS
    """
    MaxAspectWindings: float = None  # used in transfinite mesh_generators settings to define mesh_generators size along two longer lines of hex elements of windings
    Min_length_windings: float = None  # sets how small the edge length for the winding geometry volumes could be used. Overwrites the calculated value if it is smaller than this number.
    ThresholdSizeMinWindings: float = None  # sets field control of Threshold SizeMin
    ThresholdSizeMaxWindings: float = None  # sets field control of Threshold SizeMax
    ThresholdDistMinWindings: float = None  # sets field control of Threshold DistMin
    ThresholdDistMaxWindings: float = None  # sets field control of Threshold DistMax
    ThresholdSizeMinFormers: float = None  # sets field control of Threshold SizeMin
    ThresholdSizeMaxFormers: float = None  # sets field control of Threshold SizeMax
    ThresholdDistMinFormers: float = None  # sets field control of Threshold DistMin
    ThresholdDistMaxFormers: float = None  # sets field control of Threshold DistMax


class CWSPostproc(BaseModel):
    """
        Class for FiQuS CWS input file
    """
    conductors_wwns: List[int] = None  # wires in width direction numbers
    conductors_whns: List[int] = None  # wires in height direction numbers
    winding_order: List[int] = None
    trim_from: List[List[int]] = None
    trim_to: List[List[int]] = None
    variables: List[str] = None  # Name of variable to post-process by python Gmsh API, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by python Gmsh API, line Winding_1
    file_exts: List[str] = None  # Name of file extensions o post-process by python Gmsh API, like .pos


class CWS(BaseModel):
    """
        Level 1: Class for FiQuS CWS
    """
    type: Literal['CWS']
    geometry: CWSGeometry = CWSGeometry()
    mesh: CWSMesh = CWSMesh()
    solve: CWSSolve = CWSSolve()
    postproc: CWSPostproc = CWSPostproc()


# Multipole
class MultipoleSolveConvectionBoundaryCondition(BaseModel):
    """
        Level 5: Class for FiQuS Multipole
    """
    boundaries: List[str] = []
    heat_transfer_coefficient: float = None
    coolant_temperature: float = None


class MultipoleSolveOneParBoundaryCondition(BaseModel):
    """
        Level 5: Class for FiQuS Multipole
    """
    boundaries: List[str] = []
    value: float = None


class MultipoleSolveTimeParameters(BaseModel):
    """
        Level 5: Class for FiQuS Multipole
    """
    initial_time: float = None
    final_time: float = None
    time_step: float = None


class MultipoleSolveQuenchInitiation(BaseModel):
    """
        Level 5: Class for FiQuS Multipole
    """
    turns: List[int] = []
    temperatures: List[float] = []


class MultipoleSolveBoundaryConditionsElectromagnetics(BaseModel):
    """
        Level 4: Class for FiQuS Multipole
    """
    currents: List[float] = []


class MultipoleSolveBoundaryConditionsThermal(BaseModel):
    """
        Level 4: Class for FiQuS Multipole
    """
    temperature: Dict[str, MultipoleSolveOneParBoundaryCondition] = {}
    heat_flux: Dict[str, MultipoleSolveOneParBoundaryCondition] = {}
    cooling: Dict[str, MultipoleSolveConvectionBoundaryCondition] = {}


class MultipoleSolveTransientElectromagnetics(BaseModel):
    """
        Level 4: Class for FiQuS Multipole
    """
    time_pars: MultipoleSolveTimeParameters = MultipoleSolveTimeParameters()
    initial_current: float = None


class MultipoleSolveTransientThermal(BaseModel):
    """
        Level 4: Class for FiQuS Multipole
    """
    time_pars: MultipoleSolveTimeParameters = MultipoleSolveTimeParameters()
    initial_temperature: float = None
    quench_initiation: MultipoleSolveQuenchInitiation = MultipoleSolveQuenchInitiation()


class MultipoleSolveElectromagnetics(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    solved: str = None
    boundary_conditions: MultipoleSolveBoundaryConditionsElectromagnetics = MultipoleSolveBoundaryConditionsElectromagnetics()
    transient: MultipoleSolveTransientElectromagnetics = MultipoleSolveTransientElectromagnetics()


class MutlipoleSolveThermal(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    solved: str = None
    boundary_conditions: MultipoleSolveBoundaryConditionsThermal = MultipoleSolveBoundaryConditionsThermal()
    transient: MultipoleSolveTransientThermal = MultipoleSolveTransientThermal()


class MultipoleMeshThreshold(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    SizeMin: float = None
    SizeMax: float = None
    DistMin: float = None
    DistMax: float = None


class MultipoleGeometry(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    simplified_coil: bool = None
    with_iron_yoke: bool = None
    with_wedges: bool = None
    symmetry: str = None


class MultipoleMesh(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    default_mesh: bool = None
    mesh_iron: MultipoleMeshThreshold = MultipoleMeshThreshold()
    mesh_coil: MultipoleMeshThreshold = MultipoleMeshThreshold()
    Algorithm: int = None  # sets gmsh Mesh.Algorithm
    ElementOrder: int = None  # sets gmsh Mesh.ElementOrder
    Optimize: int = None  # sets gmsh Mesh.Optimize


class MultipoleSolve(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    electromagnetics: MultipoleSolveElectromagnetics = MultipoleSolveElectromagnetics()
    thermal: MutlipoleSolveThermal = MutlipoleSolveThermal()
    thin_shells: bool = None
    pro_template: str = None  # file name of .pro template file


class MultipolePostProc(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    compare_to_ROXIE: str = None
    plot_all: str = None
    variables: List[str] = None  # Name of variables to post-process, like "b" for magnetic flux density
    volumes: List[str] = None  # Name of domains to post-process, like "powered"
    file_exts: List[str] = None  # Name of file extensions to output to, like "pos"
    additional_outputs: List[str] = None  # Name of software specific input files to prepare, like "LEDET3D"


class Multipole(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    type: Literal['multipole']
    geometry: MultipoleGeometry = MultipoleGeometry()
    mesh: MultipoleMesh = MultipoleMesh()
    solve: MultipoleSolve = MultipoleSolve()
    postproc: MultipolePostProc = MultipolePostProc()


class Pancake3DGeometryWinding(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    r_i: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="innerRadius", description="inner radius of the winding"
    )
    t: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="thickness", description="tape thickness of the winding"
    )
    N: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="numberOfTurns", description="number of turns of the winding"
    )
    h: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="height", description="height or tape width of the winding"
    )

    # Optionals:
    name: str = pydantic.Field(
        default="winding", description="name to be used in the mesh"
    )
    NofVolPerTurn: pydantic.PositiveInt = pydantic.Field(
        default=2,
        alias="numberOfVolumesPerTurn",
        description="number of volumes per turn (CAD related, not physical)",
    )
    theta_i: float = pydantic.Field(
        default=0.0,
        alias="startAngle",
        description="start angle of the first pancake coil in radians",
    )

    # 2) To be calculated:
    r_o: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="outerRadius", description="outer radius of the winding"
    )
    turnTol: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        alias="turnTolerance",
        description=(
            "turn tolerance (CAD related, not physical) (to be calculated by FiQuS)"
        ),
    )
    spt: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        alias="sectionsPerTurn",
        description=(
            "sections per turn (CAD related, not physical) (to be calculated by FiQuS)"
        ),
    )


class Pancake3DGeometryInsulation(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    tsa: bool = pydantic.Field(
        default=None,
        alias="thinShellApproximation",
        description="thin shell approximation (TSA) for insulations or full 3D model",
    )
    t: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="thickness", description="insulation thickness"
    )

    # Optionals:
    name: str = pydantic.Field(
        default="insulation", description="name to be used in the mesh"
    )


class Pancake3DGeometryTerminal(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    name: str = pydantic.Field(default=None, description="name to be used in the mesh")
    t: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="thickness", description="terminal's tube thickness"
    )  # thickness

    # 2) To be calculated:
    r: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        alias="radius",
        description=(
            "inner radius of the inner terminal or outer radius of the outer terminal"
            " (to be calculated by FiQuS)"
        ),
    )


class Pancake3DGeometryTerminals(pydantic.BaseModel):
    # 1) User inputs:
    i: Pancake3DGeometryTerminal = pydantic.Field(Pancake3DGeometryTerminal(), alias="inner", description="inner terminal")
    o: Pancake3DGeometryTerminal = pydantic.Field(Pancake3DGeometryTerminal(), alias="outer", description="outer terminal")

    # Optionals:
    firstName: str = pydantic.Field(
        default="firstTerminal", description="name of the first terminal"
    )
    lastName: str = pydantic.Field(
        default="lastTerminal", description="name of the last terminal"
    )


class Pancake3DGeometryAir(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    r: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="radius", description="radius (for cylinder type air)"
    )
    a: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        alias="sideLength",
        description="side length (for cuboid type air)",
    )
    margin: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        alias="axialMargin",
        description=(
            "axial margin between the ends of the air and first/last pancake coils"
        ),
    )  # axial margin

    # Optionals:
    name: str = pydantic.Field(default="air", description="name to be used in the mesh")
    type: Literal["cylinder", "cuboid"] = pydantic.Field(
        default="cylinder", description="either cylinder or cuboid"
    )
    shellTransformation: bool = pydantic.Field(
        default=False,
        alias="shellTransformation",
        description="apply shell transformation if True (GetDP related, not physical)",
    )
    shellTransformationMultiplier: pydantic.PositiveFloat = pydantic.Field(
        default=1.2,
        alias="shellTransformationMultiplier",
        description=(
            "multiply the air's outer dimension by this value to get the shell's outer"
            " dimension (GetDP related, not physical)"
        ),
    )
    cutName: str = pydantic.Field(
        default="AirCut", description="name of the cut (cochain) to be used in the mesh"
    )
    shellVolumeName: str = pydantic.Field(
        default="airShellVolume",
        description="name of the shell volume to be used in the mesh",
    )
    fragment: bool = pydantic.Field(
        default=False,
        alias="generateGapAirWithFragment",
        description=(
            "generate the gap air with gmsh/model/occ/fragment if true (CAD related,"
            " not physical)"
        ),
    )

    # 2) To be calculated:
    h: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        alias="height",
        description="total height of the air (to be calculated by FiQuS)",
    )


class Pancake3DMeshWinding(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    axne: List[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        alias="axialNumberOfElements",
        description="axial number of elements (list of integers)",
    )

    ane: List[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        alias="azimuthalNumberOfElementsPerTurn",
        description="azimuthal number of elements per turn (list of integers)",
    )

    rne: List[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        alias="radialNumberOfElementsPerTurn",
        description="radial number of elements per turn (list of integers)",
    )

    # Optionals:
    axbc: List[pydantic.PositiveFloat] = pydantic.Field(
        default=[1],
        alias="axialBumpCoefficients",
        description=(
            "axial bump coefficient (axial elemnt distribution, smaller values for more"
            " elements at the ends) (list of floats)"
        ),
    )

    recombine: List[bool] = pydantic.Field(
        default=[False],
        alias="recombineIntoHexahedra",
        description=(
            "recombine tetrahedor elements into hexahedron elements if True (list of"
            " booleans)"
        ),
    )


class Pancake3DMeshInsulation(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:

    rne: List[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        alias="radialNumberOfElementsPerTurn",
        description=(
            "radial number of elements per turn (list of integers) (only used if TSA is"
            " False)"
        ),
    )


class Pancake3DMeshAir(pydantic.BaseModel):
    # 1) User inputs:

    # Optionals:
    structured: bool = pydantic.Field(
        default=False,
        alias="structureTopAndBottomParts",
        description=(
            "structure the top and bottom parts of the first and last pancake coils if"
            " True"
        ),
    )


class Pancake3DSolveAir(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    permeability: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        description="permeability of air"
    )


class Pancake3DSolveConductor(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    resistivity: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        description="electrical resistivity"
    )


class Pancake3DSolveTime(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    start: float = pydantic.Field(default=None, description="start time of the simulation")
    end: float = pydantic.Field(default=None, description="end time of the simulation")
    step: float = pydantic.Field(default=None, description="time step")
    rampEnd: float = pydantic.Field(default=None, description="ramp end time")
    plateauEnd: float = pydantic.Field(default=None, description="plateau end time")
    rampDownEnd: float = pydantic.Field(default=None, description="ramp down end time")

    # Optionals:
    timesToBeSaved: List[float] = pydantic.Field(
        default=None, description="list of times that wanted to be saved"
    )


class Pancake3DGeometry(pydantic.BaseModel):
    # 1) User inputs:

    wi: Pancake3DGeometryWinding = pydantic.Field(
        default=Pancake3DGeometryWinding(), alias="winding", description="winding related inputs"
    )

    ii: Pancake3DGeometryInsulation = pydantic.Field(
        default=Pancake3DGeometryInsulation(), alias="insulation", description="insulation related inputs"
    )

    ti: Pancake3DGeometryTerminals = pydantic.Field(
        default=Pancake3DGeometryTerminals(), alias="terminals", description="terminals related inputs"
    )

    ai: Pancake3DGeometryAir = pydantic.Field(default=Pancake3DGeometryAir(), alias="air", description="air related inputs")

    # Mandatory:

    N: pydantic.PositiveInt = pydantic.Field(
        default=None,
        alias="numberOfPancakes",
        description="number of pancake coils stacked on top of each other",
    )

    gap: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="gapBetweenPancakes", description="gap distance between the pancake coils"
    )

    # Optionals:
    dimTol: pydantic.PositiveFloat = pydantic.Field(
        default=1e-8,
        alias="dimensionTolerance",
        description=(
            "dimension tolerance (every dimension is a multiple of this) (CAD related,"
            " not physical)"
        ),
    )
    pancakeBoundaryName: str = pydantic.Field(
        default="PancakeBoundary",
        description=(
            "name of the pancake's curves that touches the air to be used in the mesh"
        ),
    )
    insulationBoundaryName: str = pydantic.Field(
        default="InsulationBoundary",
        description=(
            "name of the insulation's curves that touches the air to be used in the"
            " mesh (only for TSA)"
        ),
    )


class Pancake3DMesh(pydantic.BaseModel):
    sizeMin: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        alias="minimumMaximumElementSize",
        description=(
            "minimum value of the maximum element size option to be used in the outer"
            " parts"
        ),
    )
    sizeMax: pydantic.PositiveFloat = pydantic.Field(
        default=None,
        alias="maximumMaximumElementSize",
        description=(
            "maximum value of the maximum element size option to be used in the inner"
            " parts"
        ),
    )

    wi: Pancake3DMeshWinding = pydantic.Field(
        default=Pancake3DMeshWinding(), alias="winding", description="winding related inputs"
    )
    ii: Pancake3DMeshInsulation = pydantic.Field(
        default=Pancake3DMeshInsulation(), alias="insulation", description="insulation related inputs"
    )
    ai: Pancake3DMeshAir = pydantic.Field(default=Pancake3DMeshAir(), alias="air", description="terminals related inputs")


class Pancake3DSolve(pydantic.BaseModel):
    proTemplate: str = pydantic.Field(default=None, description="file name of the .pro template file")
    t: Pancake3DSolveTime = pydantic.Field(default=Pancake3DSolveTime(), alias="time", description="time related inputs")
    wi: Pancake3DSolveConductor = pydantic.Field(
        default=Pancake3DSolveConductor(), alias="winding", description="winding related inputs"
    )
    ii: Pancake3DSolveConductor = pydantic.Field(
        default=Pancake3DSolveConductor(), alias="insulation", description="insulation related inputs"
    )
    ti: Pancake3DSolveConductor = pydantic.Field(
        default=Pancake3DSolveConductor(), alias="terminals", description="terminals related inputs"
    )
    ai: Pancake3DSolveAir = pydantic.Field(default=Pancake3DSolveAir(), alias="air", description="air related inputs")


class Pancake3D(pydantic.BaseModel):
    """
    Level 1: Class for FiQuS Pancake3D
    """
    type: Literal['Pancake3D']
    geometry: Pancake3DGeometry = Pancake3DGeometry()
    mesh: Pancake3DMesh = Pancake3DMesh()
    solve: Pancake3DSolve = Pancake3DSolve()

# ---- cable properties ----

class MultipoleMonoSet(BaseModel):
    """
        Rutherford cable type for settings (.set)
    """
    type: Literal['Mono']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class MultipoleRibbonSet(BaseModel):
    """
        Rutherford cable type for settings (.set)
    """
    type: Literal['Ribbon']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class MultipoleRutherfordSet(BaseModel):
    """
        Rutherford cable type for settings (.set)
    """
    type: Literal['Rutherford']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class MultipoleConductorSet(BaseModel):
    """
        Class for conductor type for settings (.set)
    """
    cable: Union[MultipoleRutherfordSet, MultipoleRibbonSet, MultipoleMonoSet] = {'type': 'Rutherford'}


class MultipoleConductor(BaseModel):
    """
        Class for conductor type for FiQuS input (.yaml)
    """
    version: str = None
    case: str = None
    state: str = None
    cable: Union[Rutherford, Ribbon, Mono] = {'type': 'Rutherford'}
    strand: Union[Round, Rectangular] = {'type': 'Round'}  # TODO: Tape, WIC
    Jc_fit: Union[ConstantJc, Bottura, CUDI1, CUDI3, Summers, Bordini, BSCCO_2212_LBNL] = {
        'type': 'CUDI1'}  # TODO: CUDI other numbers? , Roxie?


class MultipoleRoxieGeometry(BaseModel):
    """
        Class for FiQuS multipole Roxie data (.geom)
    """
    Roxie_Data: RoxieData = RoxieData()


class MultipoleGeneralSetting(BaseModel):
    """
        Class for general information on the case study
    """
    I_ref: List[float] = None


class MultipoleModelDataSetting(BaseModel):
    """
        Class for model data for settings (.set)
    """
    general_parameters: MultipoleGeneralSetting = MultipoleGeneralSetting()
    conductors: Dict[str, MultipoleConductorSet] = {}


class MultipoleSettings(BaseModel):
    """
        Class for FiQuS multipole settings (.set)
    """
    Model_Data_GS: MultipoleModelDataSetting = MultipoleModelDataSetting()


class RunFiQuS(BaseModel):
    """
        Class for FiQuS run
    """
    type: str = None
    geometry: str = None
    mesh: str = None
    solution: str = None
    launch_gui: bool = None
    overwrite: bool = None


class General(BaseModel):
    """
        Class for FiQuS general
    """
    magnet_name: str = None


class EnergyExtraction(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    t_trigger: float = None
    R_EE: float = None
    power_R_EE: float = None
    L: float = None
    C: float = None


class QuenchHeaters(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    N_strips: int = None
    t_trigger: List[float] = None
    U0: List[float] = None
    C: List[float] = None
    R_warm: List[float] = None
    w: List[float] = None
    h: List[float] = None
    s_ins: List[float] = None
    type_ins: List[str] = None
    s_ins_He: List[float] = None
    type_ins_He: List[str] = None
    l: List[float] = None
    l_copper: List[float] = None
    l_stainless_steel: List[float] = None
    ids: List[int] = None
    turns: List[int] = None
    turns_sides: List[str] = None


class Cliq(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    t_trigger: float = None
    current_direction: List[int] = None
    sym_factor: int = None
    N_units: int = None
    U0: float = None
    C: float = None
    R: float = None
    L: float = None
    I0: float = None


class QuenchProtection(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    energy_extraction:  EnergyExtraction = EnergyExtraction()
    quench_heaters: QuenchHeaters = QuenchHeaters()
    cliq: Cliq = Cliq()


class DataFiQuS(BaseModel):
    """
        This is data structure of FiQuS Input file
    """
    general: General = General()
    run: RunFiQuS = RunFiQuS()
    magnet: Union[CCT, CWS, Multipole, Pancake3D] = {'type': 'multipole'}
    circuit: Circuit = Circuit()
    power_supply: PowerSupply = PowerSupply()
    quench_protection: QuenchProtection = QuenchProtection()
    conductors: Dict[str, MultipoleConductor] = {}








