# import os
import os
from pathlib import Path
import math
from math import *
import numpy as np
import yaml
from typing import Dict, Union
from steam_sdk.builders import geometricFunctions as gf
from steam_sdk.data import DataRoxieParser as pd
from matplotlib.patches import Arc
from steam_sdk.data.DataModelMagnet import DataModelMagnet
from steam_sdk.data.DataModelConductor import DataModelConductor
from steam_sdk.parsers.ParserMap2d import getParametersFromMap2d
from steam_sdk.parsers.ParserYamlToRoxie import ParserYamlToRoxie
from steam_sdk.utils.ParserRoxieHelpers import find_iH_oH_iL_oL


def arc_angle_between_point_and_abscissa(p, c):
    """
        Returns the angle of an arc with center c and endpoints at (cx + radius, cy) and (px, py)
        :param p: list of x and y coordinates of a point
        :param c: list of x and y coordinates of the arc center
    """
    theta = np.arctan2(p[1] - c[1], p[0] - c[0])
    return theta + (2 * np.pi if theta < 0 else 0)


def arcCenter(C, iH, oH, iL, oL, diff_radius=None):
    inner_radius = (np.sqrt(np.square(iH.x - C.x) + np.square(iH.y - C.y)) +
                    np.sqrt(np.square(iL.x - C.x) + np.square(iL.y - C.y))) / 2
    if diff_radius:
        outer_radius = inner_radius + diff_radius
    else:
        outer_radius = (np.sqrt(np.square(oH.x - C.x) + np.square(oH.y - C.y)) +
                        np.sqrt(np.square(oL.x - C.x) + np.square(oL.y - C.y))) / 2
    d_inner = [0.5 * abs((iL.x - iH.x)), 0.5 * abs((iH.y - iL.y))]
    d_outer = [0.5 * abs((oL.x - oH.x)), 0.5 * abs((oH.y - oL.y))]
    aa = [np.sqrt(np.square(d_inner[0]) + np.square(d_inner[1])),
          np.sqrt(np.square(d_outer[0]) + np.square(d_outer[1]))]
    bb = [np.sqrt(np.square(inner_radius) - np.square(aa[0])), np.sqrt(np.square(outer_radius) - np.square(aa[1]))]
    if iL.y < iH.y:
        M_inner = [iH.x + d_inner[0], iL.y + d_inner[1]]
        M_outer = [oH.x + d_outer[0], oL.y + d_outer[1]]
        if iL.y >= 0.:
            sign = [-1, -1]
        else:
            sign = [1, 1]
    else:
        M_inner = [iH.x + d_inner[0], iH.y + d_inner[1]]
        M_outer = [oH.x + d_outer[0], oH.y + d_outer[1]]
        if iL.y >= 0.:
            sign = [1, -1]
        else:
            sign = [-1, 1]
    inner = [M_inner[0] + sign[0] * bb[0] * d_inner[1] / aa[0], M_inner[1] + sign[1] * bb[0] * d_inner[0] / aa[0]]
    outer = [M_outer[0] + sign[0] * bb[1] * d_outer[1] / aa[1], M_outer[1] + sign[1] * bb[1] * d_outer[0] / aa[1]]
    return inner, outer


def sigDig(n):
    return np.format_float_positional(n, precision=8)


def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def evalContent(s, g):
    if isFloat(s):
        value = float(s)
    else:
        if any(item in s for item in '+-*/.(^'):
            if '^' in s:
                s = s.replace('^', '**')
            value = eval(s, g)
        else:
            value = g[s]
    return value


class RoxieList:
    def __init__(self, roxie_data):
        """ Returns conductor corner positions (insulated and bare) and conductor currents in list form """
        self.x_insulated = []
        self.y_insulated = []
        self.x_bare = []
        self.y_bare = []
        self.i_conductor = []
        self.x_strand = []
        self.y_strand = []
        self.i_strand = []
        self.strand_to_halfTurn = []
        self.strand_to_group = []
        self.idx_half_turn = 0
        for idx_group, eo in enumerate(roxie_data.coil.physical_order):
            winding = roxie_data.coil.coils[eo.coil].poles[eo.pole].layers[eo.layer].windings[eo.winding]
            block = winding.blocks[eo.block]
            for halfTurn_nr, halfTurn in block.half_turns.items():
                self.idx_half_turn = self.idx_half_turn + 1
                insulated = halfTurn.corners.insulated
                bare = halfTurn.corners.bare
                self.x_insulated.append([insulated.iH.x, insulated.oH.x, insulated.oL.x, insulated.iL.x])
                self.y_insulated.append([insulated.iH.y, insulated.oH.y, insulated.oL.y, insulated.iL.y])
                self.x_bare.append([bare.iH.x, bare.oH.x, bare.oL.x, bare.iL.x])
                self.y_bare.append([bare.iH.y, bare.oH.y, bare.oL.y, bare.iL.y])
                self.i_conductor.append(block.current_sign)

                for strand_gr_nr, strand_gr in halfTurn.strand_groups.items():
                    for strand_nr, strand in strand_gr.strand_positions.items():
                        self.x_strand.append(strand.x)
                        self.y_strand.append(strand.y)
                        self.i_strand.append(block.current_sign)
                        self.strand_to_halfTurn.append(self.idx_half_turn)
                        self.strand_to_group.append(idx_group + 1)


class ParserRoxie:
    """
        Class for the roxie parser
    """

    data: pd.RoxieData = pd.RoxieData()
    roxieData: pd.RoxieRawData = pd.RoxieRawData()
    rawData: pd.RoxieRawData = pd.RoxieRawData()

    dir_iron: Path = None
    dir_data: Path = None
    dir_cadata: Path = None

    cond_tot: int = 0
    no: int = None
    shift_flag: int = 0
    block: pd.Block = pd.Block()
    group: pd.Group = pd.Group()
    trans: pd.Trans = pd.Trans()
    cond_name: str = None
    conductor: pd.Cadata = pd.Cadata()
    cond_parameters: pd.CondPar = pd.CondPar()
    layer_radius = []

    def __init__(self):
        self.symmetric_coil = False
        self.windings = []


    def loadParametersFromMap2d(self, model_data: Union[DataModelMagnet, DataModelConductor], path_magnet: Path =None, path_map2d: Path =None, verbose=False):
        """
            ** Returns auxiliary parameters using map2d file from ROXIE **

            :param path_map2d: Input .map2d file. Note: By default, read the .map2d file defined in the yaml input file
            :param model_data: Model_data object to access parametrs
            :param path_magnet: Path to magnet folder to access params

            :type path_map2d: Path
            :type model_data: DataModelMagnet or DataModelConductor
            :type path_magnet: Path

            :return: None
        """
        # Acquire required parameters
        if path_map2d is None:
            path_map2d: Path = Path.joinpath(path_magnet, model_data.Sources.magnetic_field_fromROXIE)  # By default, read the .map2d file defined in the yaml input file
        headerLines: int = model_data.Options_LEDET.field_map_files.headerLines

        nT, nStrands_inGroup_ROXIE, polarities_inGroup, strandToHalfTurn, strandToGroup, x_strands, y_strands, I_strands \
            = getParametersFromMap2d(map2dFile=path_map2d, headerLines=headerLines, verbose=verbose)

        indexTstop = np.cumsum(nT).tolist()
        indexTstart = [1]
        for i in range(len(nT) - 1):
            indexTstart.extend([indexTstart[i] + nT[i]])

        return nT, nStrands_inGroup_ROXIE, polarities_inGroup, strandToHalfTurn, strandToGroup, indexTstart, indexTstop, x_strands, y_strands, I_strands

    def getIronYokeDataFromIronFile(self, iron_content: str = None, verbose: bool = False):
        """
            **Parse the content of the entire .iron file and store it in a IronDatabase object**

            Function returns a IronDatabase object that contains information about the iron yoke

            :param iron_content: .iron file content
            :type iron_content: str
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: IronDatabase
        """
        if verbose:
            print('File with iron database: {}'.format(self.dir_iron))

        functions = {'Cos': cos, 'Sin': sin, 'Tan': tan, 'Acos': acos, 'Asin': asin, 'Atan': atan, 'Sqrt': sqrt}

        data = self.data.iron

        designVariables = {}
        scalarVariables = {}
        corners = []
        notches = []
        bars = []

        if iron_content:
            fileNames = [1]
        else:
            fileNames = [self.dir_iron]
            path_iron = self.dir_iron.parent
            with open(fileNames[0]) as file:  # include .mod files
                fileContent = file.read()
                if 'include' in fileContent:
                    for i in fileContent.split('\n'):  # content by row
                        if i.strip()[:7] == 'include':
                            fileNames.append(Path.joinpath(path_iron, i.strip()[8:].strip(' )')))

        for f in fileNames:
            if isinstance(f, Path):
                file = open(f, "r")
                fileContent = file.read()
            else:
                fileContent = iron_content

            for i in fileContent.split('\n'):  # content by row
                fc = i.strip().strip(';')
                if (fc.strip()[:2] != '--' and fc != '' and fc.strip() != 'HyperMesh' and fc.strip()[:6] != 'Mirror'
                        and fc.strip()[:7] != 'include' and fc.strip()[0] != '#'):
                    if '--' in fc:  # is there a comment?
                        fc = fc[:fc.find('--')].strip().strip(';')

                    for j in fc.strip().split(';'):  # row content
                        statement = j.strip().split('=')
                        state0 = statement[0].strip()

                        if j[:3] == 'dv ':  # design variable
                            designVariables[statement[0][3:].strip()] = \
                                evalContent(statement[1].strip(),
                                            {**designVariables, **scalarVariables, **data.key_points, **functions})

                        elif j[:2] == 'kp':  # key point
                            all_global = {**designVariables, **scalarVariables, **data.key_points, **functions}

                            if '@' in statement[1]:  # then the angle is specified
                                arg = statement[1].strip(' []').split('@')
                                A = [evalContent(arg[0].strip(), all_global), evalContent(arg[1].strip(), all_global)]
                                A = [A[0] * cos(A[1]), A[0] * sin(A[1])]
                            else:  # otherwise coordinates
                                arg = statement[1].strip(' []').split(',')
                                A = [evalContent(arg[0].strip(), all_global), evalContent(arg[1].strip(), all_global)]

                            data.key_points[state0] = pd.Coord(x=sigDig(A[0]), y=sigDig(A[1]))

                        elif j[:2] == 'ln':  # hyper line
                            statement[1] = statement[1].strip()
                            if statement[1][:5] == 'Hyper':
                                arguments = statement[1][10:-1].split(',')
                                arg0 = arguments[0].strip()
                                arg1 = arguments[1].strip()
                                lineType = arguments[2].strip(' "')

                                if lineType == 'Line':
                                    data.hyper_lines[state0] = pd.HyperLine(type='line', kp1=arg0, kp2=arg1)

                                elif lineType[:6] == 'Corner':
                                    if data.key_points[arg0].y < data.key_points[arg1].y:
                                        lower = [data.key_points[arg0].x, data.key_points[arg0].y]
                                        higher = [data.key_points[arg1].x, data.key_points[arg1].y]
                                    else:
                                        lower = [data.key_points[arg1].x, data.key_points[arg1].y]
                                        higher = [data.key_points[arg0].x, data.key_points[arg0].y]

                                    if lineType[6:] == 'Out':
                                        arg = arg0 + arg1 + 'Out'  # intersection point
                                        data.key_points[arg] = pd.Coord(x=lower[0], y=higher[1])
                                    else:
                                        arg = arg0 + arg1 + 'In'
                                        data.key_points[arg] = pd.Coord(x=higher[0], y=lower[1])

                                    corners.append(state0)
                                    data.hyper_lines[state0 + 'b'] = pd.HyperLine(type='line', kp1=arg0, kp2=arg)
                                    data.hyper_lines[state0 + 'a'] = pd.HyperLine(type='line', kp1=arg, kp2=arg1)

                                elif lineType[:5] == 'Notch':
                                    all_global = {**designVariables, **scalarVariables, **data.key_points, **functions}
                                    A = [data.key_points[arg0].x, data.key_points[arg0].y]
                                    B = [data.key_points[arg1].x, data.key_points[arg1].y]

                                    alpha = evalContent(arguments[3].strip(), all_global)
                                    beta = evalContent(arguments[4].strip(), all_global)
                                    arg = arg0 + arg1 + 'Notch'  # intersection point

                                    if alpha != 0:
                                        case = [(abs(alpha) < np.pi / 2) & (alpha > 0),
                                                (abs(alpha) > np.pi / 2) & (alpha > 0),
                                                (abs(alpha) < np.pi / 2) & (alpha < 0),
                                                (abs(alpha) > np.pi / 2) & (alpha < 0)]
                                        line_a = gf.findLineThroughTwoPoints(
                                            A, [((case[1] | case[2]) - (case[0] | case[3])) * A[1] /
                                                np.tan((case[1] | case[3]) * np.pi +
                                                       ((case[0] | case[3]) - (case[1] | case[2])) * alpha) + A[0], 0.])
                                    else:
                                        line_a = [0., 1., - A[1]]

                                    if beta != 0:
                                        case = [(abs(beta) < np.pi / 2) & (beta > 0),
                                                (abs(beta) > np.pi / 2) & (beta > 0),
                                                (abs(beta) < np.pi / 2) & (beta < 0),
                                                (abs(beta) > np.pi / 2) & (beta < 0)]
                                        line_b = gf.findLineThroughTwoPoints(
                                            B, [((case[1] | case[2]) - (case[0] | case[3])) * B[1] /
                                                np.tan((case[1] | case[3]) * np.pi +
                                                       ((case[0] | case[3]) - (case[1] | case[2])) * beta) + B[0], 0.])
                                    else:
                                        line_b = [0., 1., - B[1]]

                                    data.key_points[arg] = pd.Coord(x=(line_a[1] * line_b[2] - line_b[1] * line_a[2]) /
                                                                      (line_a[0] * line_b[1] - line_b[0] * line_a[1]),
                                                                    y=(line_a[2] * line_b[0] - line_b[2] * line_a[0]) /
                                                                      (line_a[0] * line_b[1] - line_b[0] * line_a[1]))

                                    notches.append(state0)
                                    data.hyper_lines[state0 + 'b'] = pd.HyperLine(type='line', kp1=arg0, kp2=arg)
                                    data.hyper_lines[state0 + 'a'] = pd.HyperLine(type='line', kp1=arg, kp2=arg1)

                                elif lineType == 'Bar':
                                    arg = [arg0 + arg1 + 'a', arg0 + arg1 + 'b']  # rectangle corner points

                                    A = [data.key_points[arg1].x, data.key_points[arg1].y]
                                    B = [data.key_points[arg0].x, data.key_points[arg0].y]
                                    if A[0] - B[0] != 0.0:
                                        alpha = math.atan((A[1] - B[1]) / (B[0] - A[0]))
                                    else:  # is the bar horizontal?
                                        alpha = math.pi / 2

                                    if len(arguments) == 3:  # is the height of the bar not specified?
                                        if alpha == math.pi / 2:
                                            h = (A[1] - B[1]) / 2
                                        else:
                                            h = (B[0] - A[0]) / 2 / math.cos(alpha)
                                    else:
                                        h = (((B[0] > A[0]) | ((B[0] == A[0]) & (B[1] < A[1]))) -
                                             ((B[0] < A[0]) | ((B[0] == A[0]) & (B[1] > A[1])))) * \
                                            evalContent(arguments[3].strip(), {**designVariables, **scalarVariables,
                                                                               **data.key_points, **functions})

                                    data.key_points[arg[1]] = pd.Coord(x=sigDig(B[0] - h * math.sin(alpha)),
                                                                       y=sigDig(B[1] - h * math.cos(alpha)))
                                    data.key_points[arg[0]] = pd.Coord(
                                        x=sigDig(data.key_points[arg[1]].x + A[0] - B[0]),
                                        y=sigDig(data.key_points[arg[1]].y + A[1] - B[1]))

                                    bars.append(state0)
                                    data.hyper_lines[state0 + ('c' * (B[0] <= A[0]) + 'a' * (B[0] > A[0]))] = \
                                        pd.HyperLine(type='line', kp1=arg0, kp2=arg[1])
                                    data.hyper_lines[state0 + 'b'] = pd.HyperLine(type='line', kp1=arg[1], kp2=arg[0])
                                    data.hyper_lines[state0 + ('a' * (B[0] <= A[0]) + 'c' * (B[0] > A[0]))] = \
                                        pd.HyperLine(type='line', kp1=arg[0], kp2=arg1)

                                elif lineType == 'Arc':
                                    arg = [arg0, arg1]
                                    if arguments[3].strip()[:2] == 'kp':
                                        arg.append(arguments[3].strip())

                                    else:  # is the radius of the arc provided?
                                        arg.append(arg[0] + arg[1][2:] + 'P3')
                                        D = 2 * evalContent(arguments[3].strip(),
                                                            {**designVariables, **scalarVariables,
                                                             **data.key_points, **functions})  # diameter

                                        A = [data.key_points[arg[1]].x, data.key_points[arg[1]].y]
                                        B = [data.key_points[arg[0]].x, data.key_points[arg[0]].y]
                                        M = [(B[0] + A[0]) / 2, (B[1] + A[1]) / 2]  # mid point
                                        dd = np.square(A[0] - B[0]) + np.square(A[1] - B[1])  # squared distance
                                        Dd = D * D - dd

                                        if Dd > 0.0:
                                            ss = (abs(D) - np.sqrt(Dd)) / 2  # compute sagitta
                                        else:
                                            ss = D / 2

                                        if M[1] - B[1] != 0.0:
                                            alpha = math.atan((B[0] - M[0]) / (M[1] - B[1]))
                                        else:
                                            alpha = math.pi / 2

                                        if A[0] == B[0]:
                                            # if B[0] == 0.0:
                                            #     sign = np.sign(ss)
                                            # else:
                                            sign = np.sign(B[1] - A[1])
                                        elif A[1] == B[1]:
                                            sign = np.sign(A[0] - B[0])
                                        else:
                                            if A[0] > B[0]:
                                                sign = np.sign((A[0] - B[0]) / (B[1] - A[1]))
                                            else:
                                                sign = np.sign((A[0] - B[0]) / (A[1] - B[1]))

                                        data.key_points[arg[2]] = pd.Coord(x=sigDig(M[0] + sign * ss * math.cos(alpha)),
                                                                           y=sigDig(M[1] + sign * ss * math.sin(alpha)))

                                    data.hyper_lines[state0] = \
                                        pd.HyperLine(type='arc', kp1=arg[0], kp2=arg[1], kp3=arg[2])

                                elif lineType == 'Circle':
                                    data.hyper_lines[state0] = pd.HyperLine(type='circle', kp1=arg0, kp2=arg1)

                                elif lineType == 'EllipticArc':
                                    all_global = {**designVariables, **scalarVariables, **data.key_points, **functions}
                                    arg = [evalContent(arguments[3].strip(), all_global),
                                           evalContent(arguments[4].strip(), all_global)]  # axes of the ellipse
                                    data.hyper_lines[state0] = \
                                        pd.HyperLine(type='ellipticArc', kp1=arg0, kp2=arg1, arg1=arg[0], arg2=arg[1])

                                else:
                                    print(arguments[2].strip() + ' needs to be implemented')

                            elif statement[1][:4] == 'Line':
                                arguments = statement[1][5:-1].split(',')
                                data.hyper_lines[state0] = pd.HyperLine(type='line', kp1=arguments[0].strip(),
                                                                        kp2=arguments[1].strip())

                            else:
                                print(statement[1][:statement[1].find('(')] + ' needs to be implemented')

                        elif j[:2] == 'ar':  # area enclosed by hyper lines
                            statement[1] = statement[1].strip()
                            arguments = statement[1][10:-1].split(',')
                            arg = []
                            pre_line = []
                            for k in range(len(arguments) - 1):
                                name = arguments[k].strip()
                                if name in corners or name in notches:  # 2 lines are introduced for corners and notches
                                    if (data.hyper_lines[name + 'a'].kp1 in pre_line or
                                            data.hyper_lines[name + 'a'].kp2 in pre_line):
                                        arg.extend([name + 'a', name + 'b'])
                                    else:
                                        arg.extend([name + 'b', name + 'a'])
                                elif name in bars:  # 3 lines are introduced for bars
                                    if (data.hyper_lines[name + 'a'].kp1 in pre_line or
                                            data.hyper_lines[name + 'a'].kp2 in pre_line):
                                        arg.extend([name + 'a', name + 'b', name + 'c'])
                                    else:
                                        arg.extend([name + 'c', name + 'b', name + 'a'])
                                else:
                                    arg.append(name)
                                pre_line = [data.hyper_lines[arg[-1]].kp1, data.hyper_lines[arg[-1]].kp2]

                            data.hyper_areas[state0] = pd.HyperArea(material=arguments[-1].strip(), lines=arg)

                        elif j[:2] == 'BH':
                            print('BH')

                        elif j[:11] == 'HyperHoleOf':
                            arguments = state0[12:-1].split(',')
                            data.hyper_holes[len(data.hyper_holes) + 1] = \
                                pd.HyperHole(areas=[arguments[0].strip(), arguments[1].strip()])

                        elif j[:5] == 'Lmesh':
                            arguments = state0[6:-1].split(',')
                            name = arguments[0].strip()
                            if name in corners or name in notches:
                                data.hyper_lines[name + 'a'].elements = round(int(arguments[1].strip()) / 2)
                                data.hyper_lines[name + 'b'].elements = round(int(arguments[1].strip()) / 2)
                            elif name in bars:
                                data.hyper_lines[name + 'a'].elements = round(int(arguments[1].strip()) / 3)
                                data.hyper_lines[name + 'b'].elements = round(int(arguments[1].strip()) / 3)
                                data.hyper_lines[name + 'c'].elements = round(int(arguments[1].strip()) / 3)
                            else:
                                data.hyper_lines[name].elements = int(arguments[1].strip())

                        else:  # scalar variables
                            scalarVariables[state0] = \
                                evalContent(statement[1].strip(),
                                            {**designVariables, **scalarVariables, **data.key_points, **functions})
            if isinstance(f, Path):
                file.close()

        return data

    def getConductorDataFromCadataFile(self, cadata_content: str = None, verbose: bool = False):
        """
            **Parse the content of the entire .cadata file and store it in a CableDatabase object**

            Function returns a CableDatabase object that contains information about all conductors

            :param cadata_content: .cadata file content
            :type cadata_content: str
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: CableDatabase
        """
        if verbose:
            print('File with cable database: {}'.format(self.dir_cadata))

        data = self.rawData.cadata  # self.data.cadata

        if cadata_content:
            fileContent = cadata_content
        else:
            file = open(self.dir_cadata, "r")
            fileContent = file.read()
        # separate rows
        fileContentByRow = fileContent.split("\n")

        for index in range(len(fileContentByRow)):
            fc = fileContentByRow[index]

            if fc[0:5] == "CABLE":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.cable[arg[1]] = pd.Cable(height=float(arg[2]), width_i=float(arg[3]), width_o=float(arg[4]),
                                                  ns=float(arg[5]), transp=float(arg[6]), degrd=float(arg[7]),
                                                  comment=" ".join(arg[8:]))

            elif fc[0:9] == "CONDUCTOR":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.conductor[arg[1]] = pd.Conductor(type=int(arg[2]), cableGeom=arg[3], strand=arg[4],
                                                          filament=arg[5], insul=arg[6], trans=arg[7], quenchMat=arg[8],
                                                          T_0=float(arg[9]), comment=" ".join(arg[10:]))
            elif fc[0:8] == "FILAMENT":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.filament[arg[1]] = pd.Filament(fildiao=float(arg[2]), fildiai=float(arg[3]), Jc_fit=arg[4],
                                                        fit=arg[5], comment=" ".join(arg[6:]))

            elif fc[0:5] == "INSUL":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.insul[arg[1]] = pd.Insulation(radial=float(arg[2]), azimut=float(arg[3]),
                                                       comment=" ".join(arg[4:]))

            elif fc[0:6] == "QUENCH":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.quench[arg[1]] = pd.Quench(SCHeatCapa=float(arg[2]), CuHeatCapa=float(arg[3]),
                                                    CuThermCond=float(arg[4]), CuElecRes=float(arg[5]),
                                                    InsHeatCapa=float(arg[6]), InsThermCond=float(arg[7]),
                                                    FillHeatCapa=float(arg[8]), He=float(arg[9]),
                                                    comment=" ".join(arg[10:]))
                # Add entry "NONE"
                data.quench["NONE"] = pd.Quench(SCHeatCapa=None, CuHeatCapa=None, CuThermCond=None, CuElecRes=None,
                                                InsHeatCapa=None, InsThermCond=None, FillHeatCapa=None,
                                                He=None, comment="")

            elif fc[0:6] == "STRAND":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.strand[arg[1]] = pd.Strand(diam=float(arg[2]), cu_sc=float(arg[3]), RRR=float(arg[4]),
                                                    Tref=float(arg[5]), Bref=float(arg[6]),
                                                    dJc_dB=float(arg[8]), comment=" ".join(arg[9:]))

            elif fc[0:9] == "TRANSIENT":
                keywordAndRowNumber = fc.split()
                rowNumber = int(keywordAndRowNumber[1])
                for fcTemp in fileContentByRow[index + 1:index + 1 + rowNumber]:
                    arg = fcTemp.split()
                    data.transient[arg[1]] = pd.Transient(Rc=float(arg[2]), Ra=float(arg[3]), filTwistp=float(arg[4]),
                                                          filR0=float(arg[5]), fil_dRdB=float(arg[6]),
                                                          strandfillFac=float(arg[7]), comment=" ".join(arg[8:]))
                # Add entry "NONE"
                data.transient["NONE"] = pd.Transient(Rc=None, Ra=None, filTwistp=None, filR0=None,
                                                      fil_dRdB=None, strandfillFac=None, comment="")

            else:
                pass

        return data

    def getCoilDataFromDataFile(self, coil_content: str = None, verbose: bool = False):
        """
            **Parse the content of the entire .data file and store it in a Database object**

            Function returns a Database object that contains information about all conductors

            :param coil_content: .data file content
            :type coil_content: str
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: Database
        """
        if verbose:
            print('File with coil database: {}'.format(self.dir_data))

        data = self.rawData.coil

        # Define keywords
        keywords = {'group': {'key': 'LAYER ', 'index': 0},
                    'trans': {'key': 'EULER ', 'index': 0},
                    'block': {'key': 'BLOCK ', 'index': 0}}

        if coil_content:
            fileContent = coil_content
        else:
            file = open(self.dir_data, "r")
            fileContent = file.read()

        # Separate rows
        fileContentByRow = fileContent.split("\n")

        # Find group definition
        for i, row in enumerate(fileContentByRow):
            if keywords['group']['key'] in row:
                keywords['group']['index'] = i
            elif keywords['trans']['key'] in row:
                keywords['trans']['index'] = i
            elif keywords['block']['key'] in row:
                keywords['block']['index'] = i
            else:
                pass

        self.symmetric_coil = True # Check if coil have symmetry
        for key in keywords:
            firstRow = fileContentByRow[keywords[key]['index']]
            nRowsParameters = int(firstRow[5:])
            if verbose:
                print('{} definition parameters have {} row(s)'.format(key, nRowsParameters))

            # Separate part of the data with group definition information
            parameters = fileContentByRow[keywords[key]['index'] + 1:keywords[key]['index'] + 1 + nRowsParameters]

            if key == 'block':
                self.layer_radius = list(set([float(row.split()[3]) for row in parameters]))
                self.layer_radius.sort()
            # Assign parameters to a list of parameters objects
            for row in parameters:
                rowSplitStr = row.split()

                if key == 'group':
                    data.groups[rowSplitStr[0]] = pd.Group(symm=int(rowSplitStr[1]), typexy=int(rowSplitStr[2]),
                                                           blocks=list(map(int, rowSplitStr[3:-1])))
                    if int(rowSplitStr[2]) == 0:
                        self.symmetric_coil = False # If rows contains 0 then no symmetry - assumption but let's start from there
                elif key == 'trans':
                    data.transs[rowSplitStr[0]] = pd.Trans(x=float(rowSplitStr[1]), y=float(rowSplitStr[2]),
                                                           alph=float(rowSplitStr[3]), bet=float(rowSplitStr[4]),
                                                           string=str(rowSplitStr[5]), act=int(rowSplitStr[6]),
                                                           bcs=list(map(int, rowSplitStr[7:-1])))
                    if data.transs[rowSplitStr[0]].string == 'SHIFT2':
                        self.shift_flag += 1
                else:  # block
                    block_nr = int(rowSplitStr[0])
                    blocks_list = []

                    if not data.groups:
                        coil = 1
                    else:
                        for group in data.groups:
                            blocks_list += data.groups[group].blocks
                            if block_nr in data.groups[group].blocks:
                                group_nr = int(group)
                                symm = data.groups[group].symm

                                if not data.transs or self.shift_flag <= 1:
                                    coil = 1
                                else:
                                    groups_list = []
                                    trans_blocks_list = []
                                    for trans in data.transs:
                                        if data.transs[trans].act == 1:
                                            groups_list += data.transs[trans].bcs
                                            if int(group) in data.transs[trans].bcs and data.transs[trans].string == \
                                                    'SHIFT2':
                                                coil = int(trans)
                                        elif data.transs[trans].act == 3:
                                            trans_blocks_list += data.transs[trans].bcs
                                            if data.transs[trans].string == 'SHIFT2':
                                                coil = int(trans)
                                        else:
                                            raise Exception('Type of transformation not supported: check "ACT" under '
                                                            '"EULER" in the .data file.')
                    if 'coil' not in locals():
                        if block_nr not in blocks_list:
                            raise Exception('The current block does not belong to any group: check "LAYER" in the '
                                            '.data file.')
                        else:
                            if group_nr not in groups_list and block_nr not in trans_blocks_list:
                                raise Exception('The current block is not transformed or belongs to a group that is not'
                                                'transformed: check "BCS" under "EULER" in the .data file.')

                    radius = float(rowSplitStr[3])
                    layer = self.layer_radius.index(radius) + 1
                    imag = int(rowSplitStr[10])
                    turn = float(rowSplitStr[11])
                    current_sign = np.sign(float(rowSplitStr[6]))
                    if 'symm' in locals():
                        Avalue= turn * symm / 360 + 1
                        pole = floor(turn * symm / 360 + 1)
                        # How to fix this?
                    else:
                        pole = block_nr

                    if self.symmetric_coil == False:
                        if imag == 1 and turn == 0 or imag == 0 and turn == 180:
                            pole = 2
                        else:
                            pole = 1
                         # if current_sign==-1:
                         #    pole = 2
                         # else:
                         #    pole = 1

                    data.blocks[rowSplitStr[0]] = pd.Block(type=int(rowSplitStr[1]), nco=int(rowSplitStr[2]),
                                                           radius=radius, phi=float(rowSplitStr[4]),
                                                           alpha=float(rowSplitStr[5]), current=float(rowSplitStr[6]),
                                                           condname=rowSplitStr[7], n1=int(rowSplitStr[8]),
                                                           n2=int(rowSplitStr[9]), imag=int(rowSplitStr[10]),
                                                           turn=turn, coil=coil, pole=pole, layer=layer,
                                                           winding=block_nr, shift2=pd.Coord(x=0., y=0.),
                                                           roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))
        if not self.symmetric_coil:
            print("NO SYMMETRY")
        # Print each parameters object in the list
        if verbose:
            for no in data.groups:
                arg = data.groups[no]  # group
                print('Parameters of group {}: (symmetry type: {}, group type: {}, block list: {}).'
                      .format(int(no), arg.symm, arg.typexy, arg.blocks))
            for no in data.transs:
                arg = data.transs[no]  # transformation
                print('Parameters of transformation {}:'
                      '(x: {}, y: {}, alpha: {}, bet: {}, string: {}, act: {}, bcs: {}).'
                      .format(int(no), arg.x, arg.y, arg.alph, arg.bet, arg.string, arg.act, arg.bcs))
            for no in data.blocks:
                arg = data.blocks[no]  # block
                print('Parameters of block {}:'
                      '(type: {}, nco: {}, radius: {}, phi: {}, alpha: {}, current: {}, condname: {},'
                      'n1: {}, n2: {}, imag: {}, turn: {}).'
                      .format(int(no), arg.type, arg.nco, arg.radius, arg.phi, arg.alpha,
                              arg.current, arg.condname, arg.n1, arg.n2, arg.imag, arg.turn))

        return data

    def applyMultipoleSymmetry(self, blocks: Dict[str, pd.Block] = None, group: pd.Group = None, verbose: bool = False):
        """
            **Apply N-order multipole symmetry to a list of blocks**

            Function returns the input list of blocks with new block appended

            :param blocks: list of blocks
            :type blocks: Dict
            :param group: group of blocks
            :type group: Group
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: list
        """
        if group:
            data = blocks
            self.group = group
            self.no = 1
        else:
            data = self.roxieData.coil.blocks

        # This index will increase with each added block
        nb = len(data)

        # Blocks to add to the attribute group.blocks
        blockToAddToGroup = []

        # Apply multipole geometry
        if self.group.typexy == 0:
            if verbose:
                print('typexy = {}: No symmetry action.'.format(self.group.typexy)) ## Pull winding data from yaml files.
                # here get the winding data from the yaml file. Overwrite the already defined windings in the data.
                # Function is placed outside this file.
            if self.path_to_yaml is not None:
                pyr = ParserYamlToRoxie(self.path_to_yaml)
                self.windings = pyr.read_model_data_yaml()['CoilWindings']['electrical_pairs']['group_together']
            else:
                filename = os.path.splitext(os.path.basename(self.dir_data))[0]
                raise ValueError(f"For {filename} you must need to input a path to the yaml file because coil is asymmetric.")
        elif self.group.typexy == 1:
            if verbose:
                print('typexy = {}: All.'.format(self.group.typexy))

            for additionalBlock in self.group.blocks:
                nOriginalBlocks = nb
                # idxBlock = additionalBlock - 1
                if verbose:
                    print('additionalBlock = {}'.format(additionalBlock))
                    print('pole={} of {}'.format(1, self.group.symm))

                block = data[str(additionalBlock)]  # self.blockParametersList[idxBlock]
                # Add return block to the original block
                nb += 1

                data[str(nb)] = pd.Block(type=block.type, nco=block.nco, radius=block.radius, phi=block.phi,
                                         alpha=block.alpha, current=-block.current, condname=block.condname,
                                         n1=block.n1, n2=block.n2, imag=1 - block.imag,
                                         turn=block.turn + 360 / self.group.symm, coil=self.no,
                                         pole=int((nb - nOriginalBlocks + 1) / 2), layer=block.layer,
                                         winding=additionalBlock, shift2=pd.Coord(x=0., y=0.),
                                         roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))

                # Add return-line block index to group parameter list
                blockToAddToGroup = blockToAddToGroup + [nb]

                # This variable will switch between +1 and -1 for each pole
                signCurrent = +1

                # Add symmetric blocks
                for p in range(1, self.group.symm):
                    if verbose:
                        print('pole={} of {}'.format(p + 1, self.group.symm))

                    # Update current sign for this pole
                    signCurrent = signCurrent - 2 * np.sign(signCurrent)

                    # Add go-line block
                    nb += 1

                    data[str(nb)] = pd.Block(type=block.type, nco=block.nco, radius=block.radius, phi=block.phi,
                                             alpha=block.alpha, current=float(block.current * signCurrent),
                                             condname=block.condname, n1=block.n1, n2=block.n2, imag=block.imag,
                                             turn=block.turn + 360 / self.group.symm * p, coil=self.no, pole=int(p + 1),
                                             layer=block.layer, winding=additionalBlock, shift2=pd.Coord(x=0., y=0.),
                                             roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))

                    tempBlock = data[str(nb)]

                    # Add return-line block index to group parameter list
                    blockToAddToGroup = blockToAddToGroup + [nb]

                    # Add return-line block to block parameter list
                    nb += 1

                    data[str(nb)] = pd.Block(type=tempBlock.type, nco=tempBlock.nco, radius=tempBlock.radius,
                                             phi=tempBlock.phi, alpha=tempBlock.alpha, current=-tempBlock.current,
                                             condname=tempBlock.condname, n1=tempBlock.n1, n2=tempBlock.n2,
                                             imag=1 - tempBlock.imag, turn=tempBlock.turn + 360 / self.group.symm,
                                             coil=self.no, pole=int((nb - nOriginalBlocks + 1) / 2),
                                             layer=tempBlock.layer, winding=additionalBlock,
                                             shift2=pd.Coord(x=0., y=0.),
                                             roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))

                    # Add return-line block index to group parameter list
                    blockToAddToGroup = blockToAddToGroup + [nb]

        elif self.group.typexy == 2:
            if verbose:
                print('typexy = {}: One coil.'.format(self.group.typexy))

            for additionalBlock in self.group.blocks:
                # nOriginalBlocks = nb
                if verbose:
                    print('additionalBlock = {}'.format(additionalBlock))

                block = data[str(additionalBlock)]
                nb += 1
                data[str(nb)] = pd.Block(type=block.type, nco=block.nco, radius=block.radius, phi=block.phi,
                                         alpha=block.alpha, current=-block.current, condname=block.condname,
                                         n1=block.n1, n2=block.n2, imag=1 - block.imag,
                                         turn=block.turn + 360 / self.group.symm, coil=self.no,
                                         pole=block.pole, layer=block.layer,
                                         winding=additionalBlock, shift2=pd.Coord(x=0., y=0.),
                                         roll2=pd.Roll(coor=pd.Coord(x=0., y=0.), alph=0.))

                # Add return-line block index to group parameter list
                blockToAddToGroup = blockToAddToGroup + [nb]

        elif self.group.typexy == 3:
            print('typexy = {}: Connection side: NOT SUPPORTED.'.format(self.group.typexy))

        else:
            print('typexy = {}: NOT SUPPORTED.'.format(self.group.typexy))

        self.group.blocks = self.group.blocks + blockToAddToGroup

        return data

    def applyCoilTransformation(self, coil: pd.Coil = None, trans: pd.Trans = None, verbose: bool = False):
        """
            **Apply shift2 transformation (shift in x and y direction) to a list of blocks,
            apply roll2 transformation (counterclockwise rotation) to a list of blocks**
            Function returns the input list of blocks with the attributes shift2 and roll2 set to new values

            :param trans: transformation data
            :type trans: Trans
            :param coil: blocks and groups data
            :type: coil: Coil
            :param verbose: flag that determines whether the outputs are printed
            :type verbose: bool

            :return: list
        """
        if trans:
            data = coil
            self.trans = trans
        else:
            data = self.roxieData.coil

        if self.trans.act == 0:
            if verbose:
                print('Act on All blocks.')
            for block in data.blocks:
                if self.trans.string == 'SHIFT2':
                    data.blocks[block].shift2.x = self.trans.x
                    data.blocks[block].shift2.y = self.trans.y
                elif self.trans.string == 'ROLL2':
                    data.blocks[block].roll2.coor.x = self.trans.x
                    data.blocks[block].roll2.coor.y = self.trans.y
                    data.blocks[block].roll2.alph = self.trans.alph

        elif self.trans.act == 1:
            if verbose:
                print('Act on All blocks of these groups: {}.'.format(self.trans.bcs))
            for group in data.groups:
                if int(group) in self.trans.bcs:
                    for block in data.blocks:
                        if int(block) in data.groups[group].blocks:
                            if self.trans.string == 'SHIFT2':
                                data.blocks[block].shift2.x = self.trans.x
                                data.blocks[block].shift2.y = self.trans.y
                            elif self.trans.string == 'ROLL2':
                                data.blocks[block].roll2.coor.x = self.trans.x
                                data.blocks[block].roll2.coor.y = self.trans.y
                                data.blocks[block].roll2.alph = self.trans.alph

        elif self.trans.act == 2:
            if verbose:
                print('Act on Parent and offspring blocks of these groups {}: Not supported!'.format(self.trans.bcs))

        elif self.trans.act == 3:
            if verbose:
                print('Act on Specified block only: Block {}'.format(self.trans.bcs))
            for block in data.blocks:
                if int(block) in self.trans.bcs:
                    if self.trans.string == 'SHIFT2':
                        data.blocks[block].shift2.x = self.trans.x
                        data.blocks[block].shift2.y = self.trans.y
                    elif self.trans.string == 'ROLL2':
                        data.blocks[block].roll2.coor.x = self.trans.x
                        data.blocks[block].roll2.coor.y = self.trans.y
                        data.blocks[block].roll2.alph = self.trans.alph

        elif self.trans.act == 4:
            print('Act on Conductors {}. Not supported!'.format(self.trans.bcs))

        else:
            print('Act on N/a: Not supported!')

        return data

    def applySymmetryConditions(self, coil: pd.Coil = None, verbose: bool = False):
        """
            **Returns updated list of blockParametersList objects, and sets attribute blockParametersList**

            Apply symmetry conditions to blocks

            :param coil: blocks, groups, and transformation data
            :type coil: Coil
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        if coil:
            self.roxieData.coil = coil

        data = self.roxieData.coil

        symmetryTypes = {2: 'Dipole', 4: 'Quadrupole', 6: 'Sextupole', 8: 'Octupole', 10: 'Decapole', 12: 'Dodecapole',
                         31: 'Window frame dipole', 33: 'Window frame quadrupole', 41: 'Solenoid',
                         71: 'Periodic structure (wiggler)'}

        # Apply symmetry conditions to blocks
        for g, no in enumerate(data.groups):
            if not data.transs or self.shift_flag <= 1:
                self.no = 1
            else:
                for trans in data.transs:
                    if data.transs[trans].act == 1:
                        if int(no) in data.transs[trans].bcs and data.transs[trans].string == 'SHIFT2':
                            self.no = int(trans)
                        else:
                            self.no = 1
                    elif data.transs[trans].act == 3:
                        self.no = int(trans)

            self.group = data.groups[no]
            if self.group.symm == 0:
                if verbose:
                    print('Group {} has symmetry of type {} --> No symmetry.'.format(self.no, self.group.symm))

            elif 1 < self.group.symm < 13:
                if verbose:
                    print('Group {} has symmetry of type {} --> {} symmetry.'
                          .format(self.no, self.group.symm, symmetryTypes[self.group.symm]))
                self.applyMultipoleSymmetry(verbose=verbose)

            elif self.group.symm > 13:
                if verbose:
                    print('Group {} has symmetry of type {} --> {} symmetry. Not currently supported.'
                          .format(self.no, self.group.symm, symmetryTypes[self.group.symm]))

            else:
                if verbose:
                    print('Group {} has symmetry of type {} --> Not currently supported.'.format(self.no,
                                                                                                 self.group.symm))

        if verbose:
            print('Total number of blocks: {}'.format(len(data.blocks)))
            # Print each BlockParameters object in the list
            for bValue in data.blocks:
                print(str(bValue))

        return data

    def applyTransformations(self, coil: pd.Coil = None, verbose: bool = False):
        """
            **Returns updated list of blockParametersList objects, and sets attribute blockParametersList**

            Apply transformations to blocks

            :param coil: blocks, groups, and transformation data
            :type coil: Coil
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        if coil:
            self.roxieData.coil = coil

        # Apply transformations to blocks/transformations/conductors
        for no in self.roxieData.coil.transs:
            self.no = int(no)
            self.trans = self.roxieData.coil.transs[no]
            if self.trans.string == 'SHIFT2':
                if verbose:
                    print('trans {} applies a transformation of type {} --> Cartesian shift of x={} mm and y={} mm.'
                          .format(self.no, self.trans.string, self.trans.x, self.trans.y))
                self.applyCoilTransformation(verbose=verbose)

            elif self.trans.string == 'ROLL2':
                if verbose:
                    print('trans {} applies a transformation of type {} -->'
                          'Counterclockwise rotation of alpha={} deg around point x={} mm and y={} mm.'
                          .format(self.no, self.trans.string, self.trans.alph, self.trans.x, self.trans.y))
                self.applyCoilTransformation(verbose=verbose)

            elif self.trans.string == 'CONN2':
                if verbose:
                    print('trans {} applies a transformation of type {} -->'
                          'Connection of block vertices. Not currently supported. '.format(self.no, self.trans.string))

            elif self.trans.string == 'CONN2P':
                if verbose:
                    print('trans {} applies a transformation of type {} -->'
                          'Connection of block vertices to point XY. Not currently supported.'
                          .format(self.no, self.trans.string))

            else:
                if verbose:
                    print('trans {} applies a transformation of type {} --> Not currently supported.'
                          .format(self.no, self.trans.string))

        if verbose:
            print('Total number of blocks: {}'.format(len(self.roxieData.coil.blocks)))

        if verbose:
            # Print each BlockParameters object in the list
            for no in self.roxieData.coil.blocks:
                print(self.roxieData.coil.blocks[no])  # modify for printing content

        return self.roxieData.coil

    def getConductorFromCableDatabase(self, cadata: pd.Cadata = None):
        """
            ** Get the parameters of the selected conductor from an existing CableDatabase object **

            Function returns an outputConductorSigma object with the parameters of the selected conductor

            return: data
        """
        data = self.conductor

        if cadata:
            self.rawData.cadata = cadata

        # Import selected conductor data from cadata dictionary
        if self.cond_name not in data.conductor:
            data.conductor[self.cond_name] = self.rawData.cadata.conductor[self.cond_name]
            cond = data.conductor[self.cond_name]
            if cond.insul not in data.insul:
                data.insul[cond.insul] = self.rawData.cadata.insul[cond.insul]
            if cond.filament not in data.filament:
                data.filament[cond.filament] = self.rawData.cadata.filament[cond.filament]
            if cond.strand not in data.strand:
                data.strand[cond.strand] = self.rawData.cadata.strand[cond.strand]
            if cond.trans not in data.transient:
                data.transient[cond.trans] = self.rawData.cadata.transient[cond.trans]
            if cond.quenchMat not in data.quench:
                data.quench[cond.quenchMat] = self.rawData.cadata.quench[cond.quenchMat]
            if cond.cableGeom not in data.cable:
                data.cable[cond.cableGeom] = self.rawData.cadata.cable[cond.cableGeom]
        else:  # Select conductor by name
            cond = data.conductor[self.cond_name]

        # Parameters defining Insulation
        cond.parameters.wInsulNarrow = data.insul[cond.insul].radial * 1e-3
        cond.parameters.wInsulWide = data.insul[cond.insul].azimut * 1e-3

        # Parameters defining Filament
        cond.parameters.dFilament = data.filament[cond.filament].fildiao * 1e-6

        # Parameters defining Strand
        cond.parameters.dstrand = data.strand[cond.strand].diam * 1e-3
        cond.parameters.fracCu = data.strand[cond.strand].cu_sc / (1 + data.strand[cond.strand].cu_sc)
        cond.parameters.fracSc = 1 / (1 + data.strand[cond.strand].cu_sc)
        cond.parameters.RRR = data.strand[cond.strand].RRR
        cond.parameters.TupRRR = data.strand[cond.strand].Tref

        # Parameters defining Transient
        if cond.trans == 'NONE':
            cond.parameters.Rc = 0.
            cond.parameters.Ra = 0.
            cond.parameters.fRhoEff = 0.
            cond.parameters.lTp = 0.
        else:
            cond.parameters.Rc = data.transient[cond.trans].Rc
            cond.parameters.Ra = data.transient[cond.trans].Ra
            cond.parameters.fRhoEff = 1.
            cond.parameters.lTp = data.transient[cond.trans].filTwistp

        # Parameters defining Cable
        cond.parameters.wBare = data.cable[cond.cableGeom].height * 1e-3
        cond.parameters.hInBare = data.cable[cond.cableGeom].width_i * 1e-3
        cond.parameters.hOutBare = data.cable[cond.cableGeom].width_o * 1e-3
        cond.parameters.noOfStrands = int(data.cable[cond.cableGeom].ns)
        if cond.parameters.noOfStrands == 1:
            cond.parameters.noOfStrandsPerLayer = 1
            cond.parameters.noOfLayers = 1
        else:  # Rutherford cable assumed
            cond.parameters.noOfStrandsPerLayer = int(cond.parameters.noOfStrands / 2)
            cond.parameters.noOfLayers = 2

        cond.parameters.lTpStrand = data.cable[cond.cableGeom].transp * 1e-3
        # cond.parameters.wCore = 0.
        # cond.parameters.hCore = 0.
        if cond.parameters.lTpStrand != 0:
            cond.parameters.thetaTpStrand = math.atan2((cond.parameters.wBare - cond.parameters.dstrand),
                                                       (cond.parameters.lTpStrand / 2))
        else:
            cond.parameters.thetaTpStrand = 0.

        cond.parameters.degradation = data.cable[cond.cableGeom].degrd / 100
        # cond.parameters.C1 = 0.
        # cond.parameters.C2 = 0.
        # cond.parameters.fracHe = 0.
        # cond.parameters.fracFillInnerVoids = 1.
        # cond.parameters.fracFillOuterVoids = 1.

        cond.parameters.Top = cond.T_0

        self.cond_parameters = cond.parameters

        return data

    def findConductorPositions(self, block: pd.Block = None, conductor: pd.CondPar = None, verbose: bool = False):
        """
            **Returns conductor positions**

            Function to find conductor corner x-y positions and conductor current if the block has type "cos-theta"

            :param conductor: conductor parameters
            :type conductor: CondPar
            :param block: block data
            :type block: Block
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: CoilData
        """
        if block:
            self.block = block
            self.data = pd.RoxieData()
            self.cond_parameters = conductor
            self.no = 1
            self.cond_tot = 0

        radius = self.block.radius / 1000  # in [m]
        phi = self.block.phi / 180 * math.pi  # in [rad]
        alpha = self.block.alpha / 180 * math.pi  # in [rad]
        # current = self.block.current
        # imag = block.imag
        turn = self.block.turn / 180 * math.pi  # in [rad]
        # x0Cond = block.radius / 1000  # in [m]
        y0Cond = self.block.phi / 1000  # in [m]
        # xTemp = x0Cond
        yTemp = y0Cond

        shiftX = self.block.shift2.x / 1e3  # in [m]
        shiftY = self.block.shift2.y / 1e3  # in [m]
        x0Roll = self.block.roll2.coor.x / 1e3  # in [m]
        y0Roll = self.block.roll2.coor.y / 1e3  # in [m]
        alphaRoll = self.block.roll2.alph / 180 * math.pi  # in [rad]

        wBare = self.cond_parameters.wBare
        hInBare = self.cond_parameters.hInBare
        hOutBare = self.cond_parameters.hOutBare
        # hBare = (hInBare + hOutBare) / 2
        wInsulNarrow = self.cond_parameters.wInsulNarrow
        wInsulWide = self.cond_parameters.wInsulWide
        nColumns = self.cond_parameters.noOfStrandsPerLayer
        nLayers = self.cond_parameters.noOfLayers

        # Define the coefficients of the circle on which the x2 points (bottom-left) of each conductor rest
        # R, x0, and y0 coefficients of the circle, as in: (x-x0)**2 + (y-y0)**2 = R**2
        circle = [radius, 0, 0]

        # Define x/y positions, including conductor rotation of angle=alpha around origin (x0Cond,y0Cond)
        alphaTemp = alpha
        # phiTemp = phi
        if verbose:
            print('Initial alpha = {} deg'.format(alpha / math.pi * 180))
            print('Initial phi = {} deg'.format(phi / math.pi * 180))

        # Create coil, pole, layer, and winding keys if they are not present
        if self.block.coil not in self.data.coil.coils:
            self.data.coil.coils[self.block.coil] = pd.Pole()
        coil = self.data.coil.coils[self.block.coil]
        coil.bore_center = pd.Coord(x=shiftX, y=shiftY)
        if self.block.pole not in coil.poles:
            coil.poles[self.block.pole] = pd.Layer()
        pole = coil.poles[self.block.pole]
        if self.block.layer not in pole.layers:
            pole.layers[self.block.layer] = pd.Winding()
        layer = pole.layers[self.block.layer]
        if self.block.winding not in layer.windings:
            layer.windings[self.block.winding] = \
                pd.WindingData(conductors_number=self.block.nco, conductor_name=self.block.condname)
                # pd.WindingData(nco=self.block.nco, cable_current=float(sigDig(abs(self.block.current))),
                #                conductor_name=self.block.condname,
                #                strand_current=float(sigDig(abs(self.block.current / self.cond_parameter.noOfStrands))))
        winding = layer.windings[self.block.winding]

        # Initialize object for this block
        winding.blocks[self.no] = pd.BlockData(block_corners=pd.Corner(), current_sign=int(np.sign(self.block.current)))
        block = winding.blocks[self.no]

        for c in range(1, self.block.nco + 1):
            if self.no - 2>=0:
                ht_nr = c + self.half_turn_number_start_index_per_block[self.no-2]
            else:
                ht_nr = c
            block.half_turns[ht_nr] = pd.HalfTurn(corners=pd.HalfTurnCorner())

            # Calculate coordinates of four corner of bare and insulated conductor
            if self.block.type == 1:  # cos-theta
                xR = radius * math.cos(phi)
                yR = radius * math.sin(phi)
                sinAlpha = math.sin(alphaTemp)
                cosAlpha = math.cos(alphaTemp)

                xBareCable = [xR + wInsulNarrow * cosAlpha - (hInBare + wInsulWide) * sinAlpha,
                              xR + wInsulNarrow * cosAlpha - wInsulWide * sinAlpha,
                              xR + (wBare + wInsulNarrow) * cosAlpha - wInsulWide * sinAlpha,
                              xR + (wBare + wInsulNarrow) * cosAlpha - (hOutBare + wInsulWide) * sinAlpha]
                yBareCable = [yR + wInsulNarrow * sinAlpha + (hInBare + wInsulWide) * cosAlpha,
                              yR + wInsulNarrow * sinAlpha + wInsulWide * cosAlpha,
                              yR + (wBare + wInsulNarrow) * sinAlpha + wInsulWide * cosAlpha,
                              yR + (wBare + wInsulNarrow) * sinAlpha + (hOutBare + wInsulWide) * cosAlpha]

                xCable = [xR - (hInBare + 2 * wInsulWide) * sinAlpha,
                          xR,
                          xR + (wBare + 2 * wInsulNarrow) * cosAlpha,
                          xR - (hOutBare + 2 * wInsulWide) * sinAlpha + (wBare + 2 * wInsulNarrow) * cosAlpha]
                yCable = [yR + (hInBare + 2 * wInsulWide) * cosAlpha,
                          yR,
                          yR + (wBare + 2 * wInsulNarrow) * sinAlpha,
                          yR + (wBare + 2 * wInsulNarrow) * sinAlpha + (hOutBare + 2 * wInsulWide) * cosAlpha]

                # Increase inclination angle by atan( (h2-h1)/w )
                alphaTemp = alphaTemp + math.atan2((hOutBare - hInBare), (wBare + 2 * wInsulNarrow))

                # Find line through points 1 and 4 of the current conductor (top-left and top-right)
                # A, B, and C coefficients of the line, as in: A*x + B*y + C = 0
                line = gf.findLineThroughTwoPoints([xCable[0], yCable[0]], [xCable[3], yCable[3]], verbose=verbose)

                # Find the intersection points between the circle and the line just defined
                xy = gf.intersectLineCircle(line, circle, verbose=verbose)

                # Find the one of two intersection points that is closest to the x2 point of the current conductor
                if xy[0] == [None, None] and xy[1] == [None, None]:
                    raise ValueError('No intersection points were found! [{},{}] and [{},{}].'
                                     .format(xCable[0], yCable[0], xCable[1], yCable[1]))
                elif xy[0] == [None, None] and xy[1] != [None, None]:
                    next_x2, next_y2 = xy[0][0], xy[0][1]
                    if verbose:
                        print('One intersection point was found and selected: [{},{}].'.format(next_x2, next_y2))
                else:
                    dist1 = math.sqrt((xCable[1] - xy[0][0]) ** 2 + (yCable[1] - xy[0][1]) ** 2)
                    dist2 = math.sqrt((xCable[1] - xy[1][0]) ** 2 + (yCable[1] - xy[1][1]) ** 2)
                    if dist1 <= dist2:
                        next_x2, next_y2 = xy[0][0], xy[0][1]
                    else:
                        next_x2, next_y2 = xy[1][0], xy[1][1]
                    if verbose:
                        print('Two intersection points were found: [{},{}] and [{},{}].'.format(xy[0][0], xy[0][1],
                                                                                                xy[1][0], xy[1][1]))
                        print('The closest point was selected: [{},{}].'.format(next_x2, next_y2))

                # Find new phi angle: the angle between the X-axis and the line joining [next_x2,next_y2] and [x0,y0]
                phi = math.atan2(next_y2, next_x2)

                if verbose:
                    print('phi = {} rad'.format(phi))
                    print('phi = {} deg'.format(phi / math.pi * 180))

            elif self.block.type == 2:  # block-coil
                xBareCable = [radius + wInsulNarrow, radius + wInsulNarrow,  # x0Cond + wInsulNarrow
                              radius + (wBare + wInsulNarrow), radius + (wBare + wInsulNarrow)]
                yBareCable = [yTemp + (hInBare + wInsulWide), yTemp + wInsulWide,
                              yTemp + wInsulWide, yTemp + (hInBare + wInsulWide)]

                xCable = [radius, radius,  # x0Cond
                          radius + (wBare + 2 * wInsulNarrow), radius + (wBare + 2 * wInsulNarrow)]
                yCable = [yTemp + (hInBare + 2 * wInsulWide), yTemp,
                          yTemp, yTemp + (hInBare + 2 * wInsulWide)]

                # Update xTemp and yTemp (using insulated conductor positions)
                # xTemp = xTemp
                yTemp += hInBare + 2 * wInsulWide

            else:
                raise Exception('Block {} is of unknown type: {}. Not supported'.format(self.no, self.block.type))

            if self.block.type == 2:  # block-coil
                # Apply conductor rotation of angle=alpha around origin (x0Cond,y0Cond)
                for i, arg in enumerate(xBareCable):
                    xBareCable[i], yBareCable[i] = gf.rotatePoint((xBareCable[i], yBareCable[i]), (radius, y0Cond), alpha)
                    xCable[i], yCable[i] = gf.rotatePoint((xCable[i], yCable[i]), (radius, y0Cond), alpha)

            # Mirror conductor about the X-axis
            if self.block.imag == 1:
                yBareCable = [-i for i in yBareCable]
                yCable = [-i for i in yCable]
            elif self.block.imag == 0:
                pass
            else:
                raise Exception('Value of variable imag must be either 0 or 1. It is {} instead.'
                                .format(self.block.imag))

            for i, arg in enumerate(xBareCable):
                # Apply conductor rotation of angle=turn around the origin
                xBareCable[i], yBareCable[i] = gf.rotatePoint((xBareCable[i], yBareCable[i]), (0, 0), turn)
                xCable[i], yCable[i] = gf.rotatePoint((xCable[i], yCable[i]), (0, 0), turn)

                # Apply roll2 counterclockwise rotation transformation
                xBareCable[i], yBareCable[i] = gf.rotatePoint((xBareCable[i], yBareCable[i]), (x0Roll, y0Roll), alphaRoll)
                xCable[i], yCable[i] = gf.rotatePoint((xCable[i], yCable[i]), (x0Roll, y0Roll), alphaRoll)

                # Apply shift2 cartesian shift transformation
                xBareCable[i], yBareCable[i] = xBareCable[i] + shiftX, yBareCable[i] + shiftY
                xCable[i], yCable[i] = xCable[i] + shiftX, yCable[i] + shiftY

            # Store cable positions
            block.half_turns[ht_nr].corners.insulated = pd.Corner(iH=pd.Coord(x=sigDig(xCable[0 if self.block.imag == 0 else 1]),
                                                                              y=sigDig(yCable[0 if self.block.imag == 0 else 1])),
                                                                  iL=pd.Coord(x=sigDig(xCable[1 if self.block.imag == 0 else 0]),
                                                                               y=sigDig(yCable[1 if self.block.imag == 0 else 0])),
                                                                  oL=pd.Coord(x=sigDig(xCable[2 if self.block.imag == 0 else 3]),
                                                                               y=sigDig(yCable[2 if self.block.imag == 0 else 3])),
                                                                  oH=pd.Coord(x=sigDig(xCable[3 if self.block.imag == 0 else 2]),
                                                                              y=sigDig(yCable[3 if self.block.imag == 0 else 2])))
            block.half_turns[ht_nr].corners.bare = pd.Corner(
                iH=pd.Coord(x=sigDig(xBareCable[0 if self.block.imag == 0 else 1]), y=sigDig(yBareCable[0 if self.block.imag == 0 else 1])),
                iL=pd.Coord(x=sigDig(xBareCable[1 if self.block.imag == 0 else 0]), y=sigDig(yBareCable[1 if self.block.imag == 0 else 0])),
                oL=pd.Coord(x=sigDig(xBareCable[2 if self.block.imag == 0 else 3]), y=sigDig(yBareCable[2 if self.block.imag == 0 else 3])),
                oH=pd.Coord(x=sigDig(xBareCable[3 if self.block.imag == 0 else 2]), y=sigDig(yBareCable[3 if self.block.imag == 0 else 2])))

            # if c == self.block.nco - 1:
            #     block.block_corners.iH = pd.Coord(x=sigDig(xCable[0]), y=sigDig(yCable[0]))  # 1
            #     block.block_corners.oH = pd.Coord(x=sigDig(xCable[3]), y=sigDig(yCable[3]))  # 4
            # elif c == 0:
            #     block.block_corners.iL = pd.Coord(x=sigDig(xCable[1]), y=sigDig(yCable[1]))  # 2
            #     block.block_corners.oL = pd.Coord(x=sigDig(xCable[2]), y=sigDig(yCable[2]))  # 3
            # else:
            #     pass

            if c == self.block.nco and c == 1:
                corner0 = [xCable[0], yCable[0]]  # 1
                corner3 = [xCable[3], yCable[3]]  # 4
                corner1 = [xCable[1], yCable[1]]  # 2
                corner2 = [xCable[2], yCable[2]]  # 3
            elif c == self.block.nco and c == 2:
                corner0 = [xCable[0], yCable[0]]  # 1
                corner3 = [xCable[3], yCable[3]]  # 4
                corner_aux_i_next = [xCable[1], yCable[1]]
                corner_aux_o_next = [xCable[2], yCable[2]]
            elif c == self.block.nco:
                corner0 = [xCable[0], yCable[0]]  # 1
                corner3 = [xCable[3], yCable[3]]  # 4
            elif c == 2:
                corner_aux_i_next = [xCable[1], yCable[1]]
                corner_aux_o_next = [xCable[2], yCable[2]]
            elif c == 1:
                corner1 = [xCable[1], yCable[1]]  # 2
                corner2 = [xCable[2], yCable[2]]  # 3
                corner_aux_i = [xCable[0], yCable[0]]
                corner_aux_o = [xCable[3], yCable[3]]
            else:
                pass

                # pd.BlockData(corner={'1': pd.Coord(x=x[-1][0], y=y[-1][0]),
                #                      '2': pd.Coord(x=x[0][1], y=y[0][1]),
                #                      '3': pd.Coord(x=x[0][2], y=y[0][2]),
                #                      '4': pd.Coord(x=x[-1][3], y=y[-1][3])})

            # Find strand positions
            alphaS = math.atan2(yBareCable[2] - yBareCable[1], xBareCable[2] - xBareCable[1])
            sinAlphaS = math.sin(alphaS)
            cosAlphaS = math.cos(alphaS)
            for j in range(nLayers):
                block.half_turns[ht_nr].strand_groups[j + 1] = pd.StrandGroup()

                for k in range(nColumns):
                    arg = [wBare / nColumns * (k + 1 / 2),
                           (hInBare + (hOutBare - hInBare) * (k + 1 / 2) / nColumns) * (j + 1 / 2) / nLayers]
                    if self.block.imag == 0:
                        xStrand = xBareCable[1] + arg[0] * cosAlphaS - arg[1] * sinAlphaS
                        yStrand = yBareCable[1] + arg[0] * sinAlphaS + arg[1] * cosAlphaS
                    elif self.block.imag == 1:
                        xStrand = xBareCable[1] + arg[0] * cosAlphaS + arg[1] * sinAlphaS
                        yStrand = yBareCable[1] + arg[0] * sinAlphaS - arg[1] * cosAlphaS
                    else:
                        raise Exception('Value of variable imag must be either 0 or 1. It is {} instead.'
                                        .format(self.block.imag))

                    # Store strand position
                    block.half_turns[ht_nr].strand_groups[j + 1].strand_positions[k + 1] =\
                        pd.Coord(x=sigDig(xStrand), y=sigDig(yStrand))
                    # xS.append(xStrand)
                    # yS.append(yStrand)
                    # # iS.append(currentStrand)
        self.cond_tot += self.block.nco

        # Compute two new corners to make concentric blocks by intersecting a circle (having a radius equal to the
        # distance between the bore center and the starting inner/outer block corner) with the straight line
        # passing through the ending block corners that need to be replaced
        # self.ax.add_patch(patches.Circle((coil.bore_center.x, coil.bore_center.y), radius=radius, color='b'))
        # self.ax.add_line(lines.Line2D([corner0[0], corner3[0]], [corner0[1], corner3[1]], color='red'))
        # self.ax.add_line(lines.Line2D([corner3[0], corner2[0]], [corner3[1], corner2[1]], color='red'))
        # self.ax.add_line(lines.Line2D([corner2[0], corner1[0]], [corner2[1], corner1[1]], color='red'))
        # self.ax.add_line(lines.Line2D([corner1[0], corner0[0]], [corner1[1], corner0[1]], color='red'))
        # plt.show()
        if self.block.type == 2 or self.block.nco == 1:
            # block.block_corners.iH = pd.Coord(x=sigDig(corner0[0]), y=sigDig(corner0[1]))  # 1
            # block.block_corners.oH = pd.Coord(x=sigDig(corner3[0]), y=sigDig(corner3[1]))  # 4
            # block.block_corners.iL = pd.Coord(x=sigDig(corner1[0]), y=sigDig(corner1[1]))  # 2
            # block.block_corners.oL = pd.Coord(x=sigDig(corner2[0]), y=sigDig(corner2[1]))  # 3
            # block.block_corners_ins.iH = pd.Coord(x=sigDig(corner0[0]), y=sigDig(corner0[1]))  # 1
            # block.block_corners_ins.oH = pd.Coord(x=sigDig(corner3[0]), y=sigDig(corner3[1]))  # 4
            # block.block_corners_ins.iL = pd.Coord(x=sigDig(corner1[0]), y=sigDig(corner1[1]))  # 2
            # block.block_corners_ins.oL = pd.Coord(x=sigDig(corner2[0]), y=sigDig(corner2[1]))  # 3
            bore_center = (0.0,0.0)
            p1 = (corner0[0], corner0[1])
            p2 = (corner1[0], corner1[1])
            p3 = (corner2[0], corner2[1])
            p4 = (corner3[0], corner3[1])
            point_oH, point_oL, point_iH, point_iL = find_iH_oH_iL_oL(p1, p2, p3, p4, bore_center)
            point_oH_ins, point_oL_ins, point_iH_ins, point_iL_ins = find_iH_oH_iL_oL(p1, p2, p3, p4, bore_center)

            block.block_corners.iH = pd.Coord(x=sigDig(point_iH[0]), y=sigDig(point_iH[1]))  # 1
            block.block_corners.oH = pd.Coord(x=sigDig(point_oH[0]), y=sigDig(point_oH[1]))  # 4
            block.block_corners.iL = pd.Coord(x=sigDig(point_iL[0]), y=sigDig(point_iL[1]))  # 2
            block.block_corners.oL = pd.Coord(x=sigDig(point_oL[0]), y=sigDig(point_oL[1]))  # 3
            block.block_corners_ins.iH = pd.Coord(x=sigDig(point_iH_ins[0]), y=sigDig(point_iH_ins[1]))  # 1
            block.block_corners_ins.oH = pd.Coord(x=sigDig(point_oH_ins[0]), y=sigDig(point_oH_ins[1]))  # 4
            block.block_corners_ins.iL = pd.Coord(x=sigDig(point_iL_ins[0]), y=sigDig(point_iL_ins[1]))  # 2
            block.block_corners_ins.oL = pd.Coord(x=sigDig(point_oL_ins[0]), y=sigDig(point_oL_ins[1]))  # 3

        else:
            new_corners_inner = gf.intersectLineCircle(gf.findLineThroughTwoPoints(corner0, corner3),
                                                       [radius, coil.bore_center.x, coil.bore_center.y])
            if min(abs(new_corners_inner[0][0] - corner0[0]),
                   abs(new_corners_inner[1][0] - corner0[0])) == abs(new_corners_inner[0][0] - corner0[0]):
                new_inner = new_corners_inner[0]
            else:
                new_inner = new_corners_inner[1]
            mid_inner_end = [(corner0[0] + new_inner[0]) / 2, (corner0[1] + new_inner[1]) / 2]
            inner_line_mid_point = [(corner1[0] + corner_aux_i[0]) / 2, (corner1[1] + corner_aux_i[1]) / 2]
            mid_point_next = [(corner_aux_i_next[0] + corner_aux_i[0]) / 2,
                              (corner_aux_i_next[1] + corner_aux_i[1]) / 2]
            mid_inner_beg = gf.intersectTwoLines(gf.findLineThroughTwoPoints(mid_point_next, inner_line_mid_point),
                                                 gf.findLineThroughTwoPoints(corner1, corner2))

            # new_inner_radius = np.sqrt(np.square(mid_inner_end[0] - coil.bore_center.x) +
            #                            np.square(mid_inner_end[1] - coil.bore_center.y))
            # new_corners_inner_mid = gf.intersectLineCircle(
            #     gf.findLineThroughTwoPoints(corner1, corner2),
            #     [new_inner_radius, coil.bore_center.x, coil.bore_center.y])
            # if min(abs(new_corners_inner_mid[0][0] - corner1[0]),
            #        abs(new_corners_inner_mid[1][0] - corner1[0])) == abs(new_corners_inner_mid[0][0] - corner1[0]):
            #     mid_inner_beg = new_corners_inner_mid[0]
            # else:
            #     mid_inner_beg = new_corners_inner_mid[1]

            outer_radius = np.sqrt(np.square(corner2[0] - coil.bore_center.x) +
                                   np.square(corner2[1] - coil.bore_center.y))
            new_corners_outer = gf.intersectLineCircle(
                gf.findLineThroughTwoPoints(corner0, corner3),
                [outer_radius, coil.bore_center.x, coil.bore_center.y])
            if min(abs(new_corners_outer[0][0] - corner3[0]),
                   abs(new_corners_outer[1][0] - corner3[0])) == abs(new_corners_outer[0][0] - corner3[0]):
                new_outer = new_corners_outer[0]
            else:
                new_outer = new_corners_outer[1]
            mid_outer_end = [(corner3[0] + new_outer[0]) / 2, (corner3[1] + new_outer[1]) / 2]
            outer_line_mid_point = [(corner2[0] + corner_aux_o[0]) / 2, (corner2[1] + corner_aux_o[1]) / 2]
            mid_point_next = [(corner_aux_o_next[0] + corner_aux_o[0]) / 2,
                              (corner_aux_o_next[1] + corner_aux_o[1]) / 2]
            mid_outer_beg = gf.intersectTwoLines(gf.findLineThroughTwoPoints(mid_point_next, outer_line_mid_point),
                                                 gf.findLineThroughTwoPoints(corner1, corner2))
            # new_outer_radius = np.sqrt(np.square(mid_outer_end[0] - coil.bore_center.x) +
            #                            np.square(mid_outer_end[1] - coil.bore_center.y))
            # new_corners_outer_mid = gf.intersectLineCircle(
            #     gf.findLineThroughTwoPoints(corner1, corner2),
            #     [new_outer_radius, coil.bore_center.x, coil.bore_center.y])
            # if min(abs(new_corners_outer_mid[0][0] - corner2[0]),
            #        abs(new_corners_outer_mid[1][0] - corner2[0])) == abs(new_corners_outer_mid[0][0] - corner2[0]):
            #     mid_outer_beg = new_corners_outer_mid[0]
            # else:
            #     mid_outer_beg = new_corners_outer_mid[1]
            bore_center = (coil.bore_center.x,coil.bore_center.y)
            p1 = (mid_inner_end[0], mid_inner_end[1])
            p2 = (mid_outer_end[0], mid_outer_end[1])
            p3 = (mid_inner_beg[0], mid_inner_beg[1])
            p4 = (mid_outer_beg[0], mid_outer_beg[1])

            point_oH, point_oL, point_iH, point_iL = find_iH_oH_iL_oL(p1, p2, p3, p4, bore_center)
            p1 = (corner0[0], corner0[1])
            p2 = (corner1[0], corner1[1])
            p3 = (corner2[0], corner2[1])
            p4 = (corner3[0], corner3[1])
            point_oH_ins, point_oL_ins, point_iH_ins, point_iL_ins = find_iH_oH_iL_oL(p1, p2, p3, p4, bore_center)


        if point_oH is None or point_oL is None or point_iH is None or point_iL is None:
            print("Error!!!")

        block.block_corners_ins.iH = pd.Coord(x=sigDig(point_iH_ins[0]), y=sigDig(point_iH_ins[1]))  # 1
        block.block_corners_ins.oH = pd.Coord(x=sigDig(point_oH_ins[0]), y=sigDig(point_oH_ins[1]))  # 4
        block.block_corners_ins.iL = pd.Coord(x=sigDig(point_iL_ins[0]), y=sigDig(point_iL_ins[1]))  # 2
        block.block_corners_ins.oL = pd.Coord(x=sigDig(point_oL_ins[0]), y=sigDig(point_oL_ins[1]))  # 3

        block.block_corners.iH = pd.Coord(x=sigDig(point_iH[0]), y=sigDig(point_iH[1]))  # 1
        block.block_corners.oH = pd.Coord(x=sigDig(point_oH[0]), y=sigDig(point_oH[1]))  # 4
        block.block_corners.iL = pd.Coord(x=sigDig(point_iL[0]), y=sigDig(point_iL[1]))  # 2
        block.block_corners.oL = pd.Coord(x=sigDig(point_oL[0]), y=sigDig(point_oL[1]))  # 3
        # OLD CODE
            # if self.block.imag == 0:
            #     block.block_corners.iH = pd.Coord(x=sigDig(mid_inner_end[0]), y=sigDig(mid_inner_end[1]))  # 1
            #     block.block_corners.oH = pd.Coord(x=sigDig(mid_outer_end[0]), y=sigDig(mid_outer_end[1]))  # 4
            #     block.block_corners.iL = pd.Coord(x=sigDig(mid_inner_beg[0]), y=sigDig(mid_inner_beg[1]))  # 2
            #     block.block_corners.oL = pd.Coord(x=sigDig(mid_outer_beg[0]), y=sigDig(mid_outer_beg[1]))  # 3
            #     block.block_corners_ins.iH = pd.Coord(x=sigDig(corner0[0]), y=sigDig(corner0[1]))  # 1
            #     block.block_corners_ins.oH = pd.Coord(x=sigDig(corner3[0]), y=sigDig(corner3[1]))  # 4
            #     block.block_corners_ins.iL = pd.Coord(x=sigDig(corner1[0]), y=sigDig(corner1[1]))  # 2
            #     block.block_corners_ins.oL = pd.Coord(x=sigDig(corner2[0]), y=sigDig(corner2[1]))  # 3
            # else:
            #
            #
            #     block.block_corners.iL = pd.Coord(x=sigDig(mid_inner_end[0]), y=sigDig(mid_inner_end[1]))
            #     block.block_corners.oL = pd.Coord(x=sigDig(mid_outer_end[0]), y=sigDig(mid_outer_end[1]))
            #     block.block_corners.iH = pd.Coord(x=sigDig(mid_inner_beg[0]), y=sigDig(mid_inner_beg[1]))
            #     block.block_corners.oH = pd.Coord(x=sigDig(mid_outer_beg[0]), y=sigDig(mid_outer_beg[1]))
            #     block.block_corners_ins.iL = pd.Coord(x=sigDig(corner0[0]), y=sigDig(corner0[1]))  # 1
            #     block.block_corners_ins.oL = pd.Coord(x=sigDig(corner3[0]), y=sigDig(corner3[1]))  # 4
            #     block.block_corners_ins.iH = pd.Coord(x=sigDig(corner1[0]), y=sigDig(corner1[1]))  # 2
            #     block.block_corners_ins.oH = pd.Coord(x=sigDig(corner2[0]), y=sigDig(corner2[1]))  # 3

            # new_corners_inner = gf.intersectLineCircle(
            #     gf.findLineThroughTwoPoints(corner0, corner3),
            #     [radius, coil.bore_center.x, coil.bore_center.y])
            # if min(abs(new_corners_inner[0][0] - corner0[0]),
            #        abs(new_corners_inner[1][0] - corner0[0])) == abs(new_corners_inner[0][0] - corner0[0]):
            #     new_inner = new_corners_inner[0]
            # else:
            #     new_inner = new_corners_inner[1]
            # outer_radius = (np.sqrt(np.square(corner2[0] - coil.bore_center.x) +
            #                         np.square(corner2[1] - coil.bore_center.y)))
            # new_corners_outer = gf.intersectLineCircle(
            #     gf.findLineThroughTwoPoints(corner0, corner3),
            #     [outer_radius, coil.bore_center.x, coil.bore_center.y])
            # if min(abs(new_corners_outer[0][0] - corner0[0]),
            #        abs(new_corners_outer[1][0] - corner0[0])) == abs(new_corners_outer[0][0] - corner0[0]):
            #     new_outer = new_corners_outer[0]
            # else:
            #     new_outer = new_corners_outer[1]
            # if corner0[0] < corner1[0]:
            #     block.block_corners.iH = pd.Coord(x=sigDig(new_inner[0]), y=sigDig(new_inner[1]))  # 1
            #     block.block_corners.oH = pd.Coord(x=sigDig(new_outer[0]), y=sigDig(new_outer[1]))  # 4
            #     block.block_corners.iL = pd.Coord(x=sigDig(corner1[0]), y=sigDig(corner1[1]))  # 2
            #     block.block_corners.oL = pd.Coord(x=sigDig(corner2[0]), y=sigDig(corner2[1]))  # 3
            # else:
            #     block.block_corners.iL = pd.Coord(x=sigDig(new_inner[0]), y=sigDig(new_inner[1]))
            #     block.block_corners.oL = pd.Coord(x=sigDig(new_outer[0]), y=sigDig(new_outer[1]))
            #     block.block_corners.iH = pd.Coord(x=sigDig(corner1[0]), y=sigDig(corner1[1]))
            #     block.block_corners.oH = pd.Coord(x=sigDig(corner2[0]), y=sigDig(corner2[1]))

        # ((block.pole % 2 == 0) * np.sign(-I[0]) +
        #  (block.pole % 2 != 0) * np.sign(I[0])) * block.radius / 1e3]
        return self.data.coil

    def getCablePositions(self, blocks: Dict[str, pd.Block] = None, cadata: pd.Cadata = None, verbose: bool = False):
        """
            **Returns insulated and bare conductor positions, and strand positions**

            Find insulated and bare conductor positions, and strand positions

            :param cadata: conductor data
            :type cadata: Cadata
            :param blocks: blocks data
            :type blocks: Dict[str, Block]
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        blockTypes = {1: 'Cos-theta', 2: 'Block-coil'}

        if blocks:
            self.roxieData.coil.blocks = blocks



        blk_layers = [[no, blk.layer] for no, blk in self.roxieData.coil.blocks.items()]
        blk_layers.sort(key=lambda x: x[1])
        block_list = self.roxieData.coil.blocks.items()
        half_turn_number_start_index_per_block = []
        for key, value in block_list:
            half_turn_number_start_index_per_block.append(value.nco)
        self.half_turn_number_start_index_per_block = np.cumsum(half_turn_number_start_index_per_block).tolist()

        # plt.figure(figsize=(10, 10))
        # self.ax = plt.axes()
        # self.ax.set_xlim(-0.2, 0.2)
        # self.ax.set_ylim(-0.2, 0.2)
        for pair in blk_layers:
            self.no = int(pair[0])
            self.block = self.roxieData.coil.blocks[pair[0]]
            # Double check that the winding is correct.
            index = None
            for i, sublist in enumerate(self.windings):
                if self.no in sublist:
                    index = i
                    break

            if index is not None:
                #print(f"The block {self.no} is present at index {index+1}.")
                self.block.winding = index + 1
                self.roxieData.coil.blocks[str(self.no)].winding = self.block.winding

            #else:
                #print(f"The block {self.no} is not present in the list.")

            # Get desired conductor data
            self.cond_name = self.block.condname
            self.getConductorFromCableDatabase(cadata=cadata)

            # Calculate x/y positions of the conductor corners and strands
            if verbose:
                print('Block {} is of type {} --> {}.'.format(self.no, self.block.type, blockTypes[self.block.type]))

            self.findConductorPositions(verbose=verbose)
        for no, blk in self.roxieData.coil.blocks.items():
            self.data.coil.physical_order.append(pd.Order(coil=blk.coil, pole=blk.pole, layer=blk.layer,
                                                          winding=blk.winding, block=int(no)))
        # if verbose:
        #     print('Total number of conductors (half-turns): {}'.format(len(self.xPos)))
        # plt.show()
        return self.data.coil

    def getWedgePositions(self, coil: pd.CoilData = None, verbose: bool = False):
        """
            **Returns wedge positions**

            Find wedge positions

            :param coil: coil data
            :type coil: CoilData
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        if coil:
            self.data = pd.RoxieData()
            self.data.coil = coil

        # xPos = []
        # yPos = []
        # xBarePos = []
        # yBarePos = []
        # iPos = []
        # xblockCorners = []
        # yblockCorners = []
        # colormap = cm.get_cmap('nipy_spectral')
        # ht_coil = []
        # block_coil = []
        #
        # for eo in self.data.coil.physical_order:
        #     out = self.data.coil.coils[eo.coil].poles[eo.pole].layers[eo.layer].windings[eo.winding].blocks[eo.block]
        #     winding = self.data.coil.coils[eo.coil].poles[eo.pole].layers[eo.layer].windings[eo.winding]
        #     block = winding.blocks[eo.block]
        #     xblockCorners.append([block.block_corners.iH.x, block.block_corners.oH.x, block.block_corners.oL.x,
        #                           block.block_corners.iL.x])
        #     yblockCorners.append([block.block_corners.iH.y, block.block_corners.oH.y, block.block_corners.oL.y,
        #                           block.block_corners.iL.y])
        #     block_coil.append(eo.coil)
        #     # Save half turn corners
        #     for halfTurn_nr, halfTurn in block.half_turns.items():
        #         insu = halfTurn.corners.insulated
        #         bare = halfTurn.corners.bare
        #         xPos.append([insu.iH.x, insu.oH.x, insu.oL.x, insu.iL.x])
        #         yPos.append([insu.iH.y, insu.oH.y, insu.oL.y, insu.iL.y])
        #         xBarePos.append([bare.iH.x, bare.oH.x, bare.oL.x, bare.iL.x])
        #         yBarePos.append([bare.iH.y, bare.oH.y, bare.oL.y, bare.iL.y])
        #         iPos.append(block.current_sign)
        #
        # # Create normalized scale between zero and number of half turns.
        # normalize = Normalize(vmin=0, vmax=len(xPos))
        #
        # # Plot blocks and block number in coil
        # max_size = max(max(xblockCorners, key=max))    # Plot bare half turns
        # for c, (cXBarePos, cYBarePos) in enumerate(zip(xBarePos, yBarePos)):
        #     pt1, pt2, pt3, pt4 = (cXBarePos[0], cYBarePos[0]), (cXBarePos[1], cYBarePos[1]), \
        #                          (cXBarePos[2], cYBarePos[2]), (cXBarePos[3], cYBarePos[3])
        #     if iPos[c] > 0:
        #         line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=True, facecolor='r', edgecolor='k',
        #                            alpha=.25)
        #     else:
        #         line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=True, facecolor='b', edgecolor='k',
        #                            alpha=.25)
        #     plt.gca().add_line(line)
        # for c, (xblockCorners, yblockCorners) in enumerate(zip(xblockCorners, yblockCorners)):
        #     pt1, pt2, pt3, pt4 = (xblockCorners[0], yblockCorners[0]), (xblockCorners[1], yblockCorners[1]), \
        #                          (xblockCorners[2], yblockCorners[2]), (xblockCorners[3], yblockCorners[3])
        #     line = Line2D([pt1[0], pt2[0]], [pt1[1], pt2[1]], color='b')
        #     plt.gca().add_line(line)
        #     line = Line2D([pt3[0], pt4[0]], [pt3[1], pt4[1]], color='b')
        #     plt.gca().add_line(line)
        #     bore_center_x, bore_center_y = (
        #     self.data.coil.coils[block_coil[c]].bore_center.x, self.data.coil.coils[block_coil[c]].bore_center.y)
        #     plot_arcs(pt4, pt1, (bore_center_x, bore_center_y), plt.gca())
        #     plot_arcs(pt3, pt2, (bore_center_x, bore_center_y), plt.gca())
        #     x_ave_cond, y_ave_cond = sum(xblockCorners) / len(xblockCorners), sum(yblockCorners) / len(yblockCorners)
        #     plt.text(x_ave_cond, y_ave_cond, '{}'.format(c + 1), color='b', fontsize=14)

        #ax = plt.axes()

        wedge_no = 0
        for coil_nr, coil in self.data.coil.coils.items():
            for pole_nr, pole in coil.poles.items():
                for layer_nr, layer in pole.layers.items():
                    for winding_key, winding in layer.windings.items():
                        if winding_key < max(layer.windings.keys()) and winding_key + 1 in layer.windings.keys():
                            adj_winding = layer.windings[winding_key + 1]
                            blocks = list(winding.blocks.keys())
                            adj_blocks = list(adj_winding.blocks.keys())
                            try: x=self.symmetric_coil
                            except: self.symmetric_coil = False
                            for block_key, block in winding.blocks.items():
                                wedge_no += 1
                                self.data.wedges[wedge_no] = pd.Wedge()
                                wedge = self.data.wedges[wedge_no]
                                # Instead - start from bore center
                                if self.symmetric_coil:
                                    if blocks.index(block_key) == 0:
                                        wedge.corners = pd.Corner(iH=adj_winding.blocks[adj_blocks[0]].block_corners.iL, iL=block.block_corners.iH,
                                                                  oH=adj_winding.blocks[adj_blocks[0]].block_corners.oL, oL=block.block_corners.oH)
                                        wedge.corners_ins = pd.Corner(iH=adj_winding.blocks[adj_blocks[0]].block_corners_ins.iL, iL=block.block_corners_ins.iH,
                                                                      oH=adj_winding.blocks[adj_blocks[0]].block_corners_ins.oL, oL=block.block_corners_ins.oH)
                                        wedge.order_l = pd.Order(coil=coil_nr, pole=pole_nr, layer=layer_nr, winding=winding_key, block=block_key)
                                        wedge.order_h = pd.Order(coil=coil_nr, pole=pole_nr, layer=layer_nr, winding=winding_key + 1, block=adj_blocks[0])
                                    else:
                                        wedge.corners = pd.Corner(iH=block.block_corners.iL, iL=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners.iH,
                                                                  oH=block.block_corners.oL, oL=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners.oH)
                                        wedge.corners_ins = pd.Corner(iH=block.block_corners_ins.iL, iL=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners_ins.iH,
                                                                      oH=block.block_corners_ins.oL, oL=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners_ins.oH)
                                        wedge.order_h = pd.Order(coil=coil_nr, pole=pole_nr, layer=layer_nr, winding=winding_key, block=block_key)
                                        wedge.order_l = pd.Order(coil=coil_nr, pole=pole_nr, layer=layer_nr, winding=winding_key + 1, block=adj_blocks[blocks.index(block_key)])
                                else:
                                    Ax, Ay = (block.block_corners.iH.x, block.block_corners.iH.y)
                                    if blocks.index(block_key) == 0:
                                        Bx, By = (adj_winding.blocks[adj_blocks[0]].block_corners.iH.x, adj_winding.blocks[adj_blocks[0]].block_corners.iH.y)
                                    else:
                                        Bx, By = (adj_winding.blocks[adj_blocks[1]].block_corners.iH.x, adj_winding.blocks[adj_blocks[1]].block_corners.iH.y)

                                    Cx, Cy = (coil.bore_center.x, coil.bore_center.y)
                                    AC = (Cx - Ax, Cy - Ay)
                                    BC = (Cx - Bx, Cy - By)
                                    cross_product = AC[0] * BC[1] - AC[1] * BC[0]
                                    if cross_product > 0:
                                        anticlockwise = True

                                    else:
                                        anticlockwise=False

                                    if anticlockwise:
                                        wedge.corners = pd.Corner(iH=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners.iL, iL=block.block_corners.iH,
                                                                  oH=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners.oL, oL=block.block_corners.oH)
                                        wedge.corners_ins = pd.Corner(iH=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners_ins.iL, iL=block.block_corners_ins.iH,
                                                                      oH=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners_ins.oL, oL=block.block_corners_ins.oH)
                                        wedge.order_l = pd.Order(coil=coil_nr, pole=pole_nr, layer=layer_nr, winding=winding_key, block=block_key)
                                        wedge.order_h = pd.Order(coil=coil_nr, pole=pole_nr, layer=layer_nr, winding=winding_key + 1, block=adj_blocks[0])
                                    else:
                                        wedge.corners = pd.Corner(iH=block.block_corners.iL, iL=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners.iH,
                                                                  oH=block.block_corners.oL, oL=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners.oH)
                                        wedge.corners_ins = pd.Corner(iH=block.block_corners_ins.iL, iL=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners_ins.iH,
                                                                      oH=block.block_corners_ins.oL, oL=adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners_ins.oH)
                                        wedge.order_h = pd.Order(coil=coil_nr, pole=pole_nr, layer=layer_nr, winding=winding_key, block=block_key)
                                        wedge.order_l = pd.Order(coil=coil_nr, pole=pole_nr, layer=layer_nr, winding=winding_key + 1, block=adj_blocks[blocks.index(block_key)])

                                # color='k'
                                # arg = [(wedge.corners.iH.x, wedge.corners.iH.y),
                                #        (wedge.corners.iL.x, wedge.corners.iL.y),
                                #        (wedge.corners.oH.x, wedge.corners.oH.y),
                                #        (wedge.corners.oL.x, wedge.corners.oL.y)]
                                # line = Line2D([arg[0][0], arg[1][0]], [arg[0][1], arg[1][1]], color=color)
                                # plt.gca().add_line(line)
                                # line = Line2D([arg[3][0], arg[2][0]], [arg[3][1], arg[2][1]], color=color)
                                # plt.gca().add_line(line)
                                # line = Line2D([arg[0][0], arg[2][0]], [arg[0][1], arg[2][1]], color=color)
                                # plt.gca().add_line(line)
                                # line = Line2D([arg[3][0], arg[1][0]], [arg[3][1], arg[1][1]], color=color)
                                # plt.gca().add_line(line)
                                # if block_key>5:
                                #     break

                                # ax.text(wedge.corners.iH.x, wedge.corners.iH.y, 'iH', style='italic', bbox={'facecolor': 'red', 'pad': 2})
                                # ax.text(wedge.corners.oH.x, wedge.corners.oH.y, 'oH', style='italic', bbox={'facecolor': 'red', 'pad': 2})
                                # ax.text(wedge.corners.iL.x, wedge.corners.iL.y, 'iL', style='italic', bbox={'facecolor': 'red', 'pad': 2})
                                # ax.text(wedge.corners.oL.x, wedge.corners.oL.y, 'oL', style='italic', bbox={'facecolor': 'red', 'pad': 2})
                                # if blocks.index(block_key) == 0:
                                #     corners1 = block.block_corners
                                #     corners2 = adj_winding.blocks[adj_blocks[0]].block_corners
                                # else:
                                #     corners2 = block.block_corners
                                #     corners1 = adj_winding.blocks[adj_blocks[blocks.index(block_key)]].block_corners
                                #
                                # if corners1.iL.y >= 0.:
                                #     wedge.corners = pd.Corner(iH=corners2.iL, iL=corners1.iH,
                                #                               oH=corners2.oL, oL=corners1.oH)
                                # else:
                                #     wedge.corners = pd.Corner(iH=corners1.iL, iL=corners2.iH,
                                #                               oH=corners1.oL, oL=corners2.oH)

                                wedge.corrected_center = pd.CenterShift()
                                wedge.corrected_center_ins = pd.CenterShift()
                                if wedge.corners.iL.y >= 0.:
                                    inner, outer = arcCenter(C=coil.bore_center, iH=wedge.corners.iH, iL=wedge.corners.iL,
                                                             oH=wedge.corners.oH, oL=wedge.corners.oL)
                                    inner_ins, outer_ins = arcCenter(C=coil.bore_center, iH=wedge.corners_ins.iH, iL=wedge.corners_ins.iL,
                                                                     oH=wedge.corners_ins.oH, oL=wedge.corners_ins.oL)
                                else:
                                    inner, outer = arcCenter(C=coil.bore_center, iH=wedge.corners.iL, iL=wedge.corners.iH,
                                                             oH=wedge.corners.oL, oL=wedge.corners.oH)
                                    inner_ins, outer_ins = arcCenter(C=coil.bore_center, iH=wedge.corners_ins.iL, iL=wedge.corners_ins.iH,
                                                                     oH=wedge.corners_ins.oL, oL=wedge.corners_ins.oH)
                                wedge.corrected_center.inner = pd.Coord(x=float(sigDig(inner[0])), y=float(sigDig(inner[1])))
                                wedge.corrected_center.outer = pd.Coord(x=float(sigDig(outer[0])), y=float(sigDig(outer[1])))
                                wedge.corrected_center_ins.inner = pd.Coord(x=float(sigDig(inner_ins[0])), y=float(sigDig(inner_ins[1])))
                                wedge.corrected_center_ins.outer = pd.Coord(x=float(sigDig(outer_ins[0])), y=float(sigDig(outer_ins[1])))
                                # ax.text(wedge.corrected_center.inner.x, wedge.corrected_center.inner.y, 'i' + str(wedge_no), style='italic', bbox={'facecolor': 'blue', 'pad': 2})
                                # ax.text(wedge.corrected_center.outer.x, wedge.corrected_center.outer.y, 'o' + str(wedge_no), style='italic', bbox={'facecolor': 'blue', 'pad': 2})
        # plt.show()

        return self.data if coil else self.data.wedges

    def getData(self, dir_iron: Path = None, dir_data: Path = None, dir_cadata: Path = None,
                dump_yamls: bool = False, path_to_yaml_model_data: str = None, verbose: bool = False):
        """
            **Returns all data**

            :param dir_iron: directory for .iron file
            :type dir_iron: Path
            :param dir_data: directory for .data file
            :type dir_data: Path
            :param dir_cadata: directory for .cadata file
            :type dir_cadata: Path
            :param dump_yamls: flag that determines whether the dictionary is dumped into yaml
            :type dump_yamls: bool
            :param verbose: flag that determines whether the output are printed
            :type verbose: bool

            :return: list
        """
        # Re-initialize dictionaries
        self.data: pd.RoxieData = pd.RoxieData()
        self.roxieData: pd.RoxieRawData = pd.RoxieRawData()
        self.rawData: pd.RoxieRawData = pd.RoxieRawData()
        self.path_to_yaml = path_to_yaml_model_data

        # Acquire iron yoke data from the .iron Roxie file
        if dir_iron:
            self.dir_iron = dir_iron
            self.getIronYokeDataFromIronFile(verbose=verbose)

            # iron=self.data.iron
            # plt.figure(figsize=(7.5, 7.5))
            # ax = plt.axes()
            #
            # max_x = 0
            # max_y = 0
            # for point_name, point in iron.key_points.items():
            #     max_x = max(point.x, max_x)
            #     max_y = max(point.y, max_y)
            #
            # for line_name, line in iron.hyper_lines.items():
            #     if line.type == 'line':
            #         ax.add_line(lines.Line2D([iron.key_points[line.kp1].x, iron.key_points[line.kp2].x],
            #                                  [iron.key_points[line.kp1].y, iron.key_points[line.kp2].y],
            #                                  color='black', linewidth=1))
            #
            #     elif line.type == 'arc':
            #         pt1 = iron.key_points[line.kp1]
            #         pt2 = iron.key_points[line.kp2]
            #         center = arcCenterFromThreePoints(pt1, iron.key_points[line.kp3], pt2)
            #         radius = (np.sqrt(np.square(pt1.x - center[0]) + np.square(pt1.y - center[1])) +
            #                   np.sqrt(np.square(pt2.x - center[0]) + np.square(pt2.y - center[1]))) / 2
            #         if pt1.x < pt2.x and pt1.x < center[0] and pt1.y < pt2.y and pt1.y < center[1]:
            #             th1 = - np.arctan2(pt1.y - center[1], pt1.x - center[0]) * 180 / np.pi
            #         else:
            #             th1 = np.arctan2(pt1.y - center[1], pt1.x - center[0]) * 180 / np.pi
            #         th2 = np.arctan2(pt2.y - center[1], pt2.x - center[0]) * 180 / np.pi
            #         ax.add_patch(patches.Arc((center[0], center[1]), width=2 * radius, height=2 * radius, angle=0,
            #                                  theta1=min(th1, th2), theta2=max(th1, th2), color='blue', linewidth=1))
            #
            #     elif line.type == 'ellipticArc':
            #         pt1 = iron.key_points[line.kp1]
            #         pt2 = iron.key_points[line.kp2]
            #         a, b = line.arg1, line.arg2
            #         x1, y1 = pt1.x, pt1.y
            #         x2, y2 = pt2.x, pt2.y
            #         x3 = np.power(x1, 2.0)
            #         y3 = np.power(y1, 2.0)
            #         x4 = np.power(x2, 2.0)
            #         y4 = np.power(y2, 2.0)
            #         a2 = np.power(a, 2.0)
            #         b2 = np.power(b, 2.0)
            #         expression = (
            #                 -4.0 * a2 * b2 + a2 * y3 - 2.0 * a2 * y1 * y2 + a2 * y4 + b2 * x3 - 2.0 * b2 * x1 * x2 + b2 * x4)
            #         xc = x1 / 2.0 + x2 / 2.0 - a * np.power(-expression / (
            #                 a2 * y3 - 2.0 * a2 * y1 * y2 + a2 * y4 + b2 * x3 - 2.0 * b2 * x1 * x2 + b2 * x4),
            #                                                 0.5) * (y1 - y2) / (2.0 * b)
            #
            #         yc = y1 / 2.0 + y2 / 2.0 + b * np.power(
            #             -expression / (a2 * y3 - 2.0 * a2 * y1 * y2 + a2 * y4 + b2 * x3 - 2.0 * b2 * x1 * x2 + b2 * x4),
            #             0.5) * (x1 - x2) / (2.0 * a)
            #
            #         center = [xc, yc]
            #         th1 = np.degrees(np.arctan2(pt1.y - center[1], pt1.x - center[0]))
            #         th2 = np.degrees(np.arctan2(pt2.y - center[1], pt2.x - center[0]))
            #         arc=patches.Arc((center[0], center[1]), width=2 * line.arg1, height=2 * line.arg2, angle=0,
            #                                  theta1=min(th1, th2), theta2=max(th1, th2), color='purple', linewidth=1)
            #         ax.add_patch(arc)
            #
            #     elif line.type == 'circle':
            #         pt1 = iron.key_points[line.kp1]
            #         pt2 = iron.key_points[line.kp2]
            #         center = [(pt1.x + pt2.x) / 2, (pt1.y + pt2.y) / 2]
            #         radius = (np.sqrt(np.square(pt1.x - center[0]) + np.square(pt1.y - center[1])) +
            #                   np.sqrt(np.square(pt2.x - center[0]) + np.square(pt2.y - center[1]))) / 2
            #         ax.add_patch(patches.Circle((center[0], center[1]),
            #                                     radius=radius, fill=False, edgecolor='green', linewidth=1))

                # ax.set_xlim(0, 1.1 * max_x)
                # ax.set_ylim(0, max_y + 0.1 * max_x)
                # plt.set_cmap('jet')
                # plt.rcParams.update({'font.size': 12})
        #plt.show()

        if dir_data and dir_cadata:
            # Acquire conductor data from the .cadata Roxie file
            self.dir_cadata = dir_cadata
            self.getConductorDataFromCadataFile(verbose=verbose)

            # Acquire coil data from the .data Roxie file
            self.dir_data = dir_data
            self.getCoilDataFromDataFile(verbose=verbose)  # TODO: alternatively, allow to read coil data from DataBuilderMagnet keys

            # Save raw data from original Roxie files
            if dump_yamls:
                with open('raw_data.yaml', 'w') as yaml_file:
                    yaml.dump(self.rawData.dict(), yaml_file, default_flow_style=False)

            # Apply symmetry conditions and transformations to the original winding blocks
            self.roxieData = self.rawData
            self.applySymmetryConditions(verbose=verbose)
            self.applyTransformations(verbose=verbose)

            # Save comprehensive Roxie data after manipulation (inherits from the raw data)
            if dump_yamls:
                with open('roxie_data.yaml', 'w') as yaml_file:
                    yaml.dump(self.roxieData.dict(), yaml_file, default_flow_style=False)

            # Compute half turn positions (bare conductors, insulated conductors, strands)
            self.getCablePositions(verbose=verbose)

            # Compute wedge positions
            self.getWedgePositions(verbose=verbose)

            # Save data for API
            if dump_yamls:
                with open('data.yaml', 'w') as yaml_file:
                    yaml.dump(self.data.dict(), yaml_file, default_flow_style=False)

        return self.data

def plot_arcs(start, end, center, ax, color='b'):
    """
    Plot arc using a start coordinate, end coordinate, an axis x and a color
    """

    # Define the three points
    radius = np.sqrt((start[0] - center[0]) ** 2 + (start[1] - center[1]) ** 2)

    # Calculate the start and end angles of the arc
    start_angle = np.arctan2(start[1] - center[1], start[0] - center[0])
    end_angle = np.arctan2(end[1] - center[1], end[0] - center[0])
    central_angle = end_angle - start_angle

    # Create the arc object
    arc = Arc(center, 2 * radius, 2 * radius, angle=0, theta1=start_angle * 180 / np.pi,
              theta2=end_angle * 180 / np.pi, color=color)

    # If no Axes object was specified, use the current Axes

    # Add the arc to the plot and show the points for reference
    ax.add_patch(arc)