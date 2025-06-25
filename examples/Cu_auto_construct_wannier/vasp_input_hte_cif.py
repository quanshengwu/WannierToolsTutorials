# Creates VASP input from a given POSCAR
# Author: Ilias Samathrakis
# modified by Yuzhi Wang  
# Email: yuzhiwang@iphy.ac.cn

from pymatgen.core import Structure
from pymatgen.symmetry.bandstructure import HighSymmKpath
from pymatgen.io.vasp import Kpoints
import subprocess
import os
import sys
import numpy as np
import re
import math
from fractions import Fraction
import input_parameters


def read_POSCAR():
    POSCAR_exists = False
    atoms, multiplicity, lat_con = [], [], []
    number_line, multiplier = 0, 0

    if os.path.exists('POSCAR') == True:
        POSCAR_exists = True

    if POSCAR_exists == True:
        with open("POSCAR", "r") as rf:
            for i, line in enumerate(rf):
                line = line.split()
                if i == 5:
                    for j in line:
                        atoms.append(j)
                if i == 1:
                    multiplier = float(line[0])
                if i == 2:
                    line_info = []
                    for j in line:
                        line_info.append(multiplier*float(j))
                    lat_con.append(line_info)
                if i == 3:
                    line_info = []
                    for j in line:
                        line_info.append(multiplier*float(j))
                    lat_con.append(line_info)
                if i == 4:
                    line_info = []
                    for j in line:
                        line_info.append(multiplier*float(j))
                    lat_con.append(line_info)
                if i == 6:
                    if line[0].isdigit():
                        number_line = 5
                        for j in line:
                            multiplicity.append(int(j))
            if not atoms:
                print("Information cannot be extracted from POSCAR, use cif instead")
                exit(1)
    else:
        print("POSCAR does not exist")
        exit(1)

    return atoms, multiplicity, lat_con


def estim_bands(atoms, multiplicity, in_tags, cores):
    nbands_index = search_index(in_tags, 'NBANDS')

    if nbands_index != -1:
        minimum_bands = in_tags[nbands_index][1]
    else:
        number_of_atoms = 0
        for i in multiplicity:
            number_of_atoms = number_of_atoms + i
        minimum_bands = int(2 * 9 * number_of_atoms)

    num_bands = minimum_bands
    while True:
        if (num_bands/cores) % 1 == 0:
            break
        num_bands = num_bands + 1

    return num_bands


def read_INCAR():
    data = []
    lorbit_index = 0
    with open("INCAR", "r") as rf:
        for i, line in enumerate(rf):
            line = line.split()
            data.append(line)
    for i in range(len(data)):
        if data[i][0] == 'LORBIT':
            lorbit_index = i
            break
    return data, lorbit_index


def get_additional_tags(incar_tags, const_tag, number_bands, atoms, multiplicity, FELEM, u_calc, u_val, j_val, l_val, submitted, reason, magnetism, non_collinearity, soc_tag, cores):
    number_of_atoms = 0
    for i in multiplicity:
        number_of_atoms = number_of_atoms + i

    if number_of_atoms <= 10:
        submitted = True
    if number_of_atoms > 10:
        submitted = False
        reason.append("Too many atoms")

    # incar_tags.append(['npar'.upper(), int(math.sqrt(cores))])
    incar_tags.append(['nbands'.upper(), number_bands])

    if magnetism:
        mag_ind = search_index(incar_tags, "MAGMOM")
        if mag_ind == -1:
            if non_collinearity:
                mag_init = '0 0 0 '
                incar_tags.append(['lnoncollinear'.upper(), ".TRUE."])
            else:
                mag_init = '0 '

            incar_tags.append(['magmom'.upper(), mag_init * number_of_atoms])
        else:
            if const_tag:
                if non_collinearity:
                    incar_tags.append(['lnoncollinear'.upper(), ".TRUE."])
                # rw = get_rws()
                # incar_tags.append(['i_constrained_m'.upper(), 1])
                # incar_tags.append(['lambda'.upper(), 10])
                # incar_tags.append(['rwigs'.upper(), rw])
                # incar_tags.append(['m_constr'.upper(), incar_tags[mag_ind][1]])
        if soc_tag:
            incar_tags.append(['lsorbit'.upper(), ".TRUE."])

    if u_calc and FELEM:
        u_values = ""
        j_values = ""
        l_values = ""

        f_elements = ["La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho",
                      "Er", "Tm", "Yb", "Lu", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Cf"]

        incar_tags.append(['ldau'.upper(), ".TRUE."])
        incar_tags.append(['ldautype'.upper(), 1])
        incar_tags.append(['ldauprint'.upper(), 2])

        for i in atoms:
            if i in f_elements:
                u_values = u_values + str(u_val[i])
                j_values = j_values + str(j_val[i])
                l_values = l_values + str(l_val[i])
            else:
                u_values = u_values + ' 0 '
                j_values = j_values + ' 0 '
                l_values = l_values + ' -1 '

        incar_tags.append(["ldauu".upper(), u_values])
        incar_tags.append(["ldauj".upper(), j_values])
        incar_tags.append(["ldaul".upper(), l_values])

    return submitted, incar_tags


def get_INCARwfs_tags(tags, lorbit_index):
    new_tags = []
    if lorbit_index != -1:
        tags[lorbit_index][1] = 11
    for i in range(len(tags)):
        new_tags.append([tags[i][0], tags[i][1]])
    new_tags.append(["LWANNIER90".upper(), ".TRUE.".upper()])
    new_tags.append(["ISYM".upper(), "-1".upper()])
    new_tags.append(["ICHARG".upper(), "11"])
    npar_index = search_index(new_tags, 'NPAR')
    del new_tags[npar_index]
    return new_tags


def get_INCARband_tags(tags, lorbit_index):
    new_tags = []
    if lorbit_index != -1:
        tags[lorbit_index][1] = 11
    for i in range(len(tags)):
        new_tags.append([tags[i][0], tags[i][1]])
    new_tags.append(["ICHARG".upper(), "11"])
    return new_tags


def get_INCARrelax_tags(tags, lorbit_index):
    new_tags = []
    if lorbit_index != -1:
        tags[lorbit_index][1] = 11
    for i in range(len(tags)):
        new_tags.append([tags[i][0], tags[i][1]])
    # new_tags.append(["ICHARG".upper(), "11"])
    new_tags.append(["EDIFFG".upper(), "-0.005"])
    new_tags.append(["ISIF".upper(), "3"])
    new_tags.append(["NSW".upper(), "200"])
    new_tags.append(["IBRION".upper(), "2"])
    new_tags = [t for t in new_tags if t[0] != "LSORBIT"]
    new_tags = [t for t in new_tags if t[0] != "LNONCOLLINEAR"]
    return new_tags


def get_file(data, name):
    with open(name, 'w') as wf:
        for i in range(len(data)):
            wf.write("{} = {}\n".format(data[i][0], data[i][1]))


def get_POTCAR(pseudo, atoms, submitted, reason, potcar_dir):
    if os.path.exists('POTCAR'):
        print("POTCAR already exists in the current directory, skip generation.")
        submitted = True
        return submitted
    
    full_dir = []
    elements_dir = []
    submitted = True

    for i in atoms:
        elements_dir.append(pseudo[i])
    if 'NA' in elements_dir:
        submitted = False
        reason.append("pseudopotential does not exist")
        return submitted
    for i in elements_dir:
        full_dir.append(potcar_dir + i + '/POTCAR')

    my_files, my_dirs = [], []
    my_files, my_dirs = search_files_and_dirs()

    # if 'POTCAR' in my_files:
    #     os.system("rm POTCAR")

    with open('potgen.sh', 'w') as wf:
        for i in range(len(full_dir)):
            wf.write("{} {} {} {}\n".format(
                'cat', full_dir[i], '>>', 'POTCAR'))

    os.system('sh potgen.sh')
    os.system('rm potgen.sh')
    return submitted


def get_rws():
    h = []
    with open('POTCAR', 'r') as rf:
        for i, line in enumerate(rf):
            line = line.split()
            if line and line[0] == 'RWIGS':
                for j in range(len(line)):
                    line[j] = line[j].replace(";", "")
                h.append(line[5])
    rws = " ".join(h)
    return rws


def get_KPOINTS():
    structure = Structure.from_file("POSCAR")
    kpoints = Kpoints.automatic_density(structure, kppa=4000)
    kpoints.write_file("KPOINTS")


def get_KPOINTS_band():
    structure = Structure.from_file("POSCAR")
    kpath = HighSymmKpath(structure)
    kpoints = Kpoints.automatic_linemode(20, kpath)
    kpoints.write_file("KPOINTS.band")


def get_restrictions(atoms):
    FELEM = False

    f_elements = ["La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho",
                  "Er", "Tm", "Yb", "Lu", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Cf"]


    for i in atoms:
        if i in f_elements:
            FELEM = True

    return FELEM


def get_run(CALC, atoms, multiplicity, names_wfs, names_band, names_relax, vasp_dir, wann_dir, cores, time, memory, increase_memory, pr_id, python_dir, vasp_output, wannier_output):
    multi_str = []
    name = ""
    GB = 1024
    for i in range(len(multiplicity)):
        multi_str.append(str(multiplicity[i]))
    for i in range(len(atoms)):
        name = name + atoms[i] + multi_str[i]
    total_atoms = 0
    for i in range(len(multiplicity)):
        total_atoms = total_atoms + multiplicity[i]

    memory = memory*GB

    if memory == 0:
        if total_atoms > 0 and total_atoms <= 10:
            memory = 4*GB
        elif total_atoms > 10 and total_atoms <= 20:
            memory = 6*GB
        elif total_atoms > 20 and total_atoms <= 30:
            memory = 8*GB
        elif total_atoms > 30 and total_atoms <= 40:
            memory = 10*GB
        elif total_atoms > 40 and total_atoms <= 50:
            memory = 12*GB
        else:
            memory = 16*GB

    if increase_memory:
        memory = memory + 2048

    time = int(time)
    if time > 168:
        time = 168
    if time == 0:
        time = 24

    with open("sub-vasp.sh", "w") as wf:
        wf.write("#!/bin/bash\n")
        wf.write("#SBATCH -J {}\n".format(name))
        wf.write("#SBATCH -p intel\n")
        wf.write("#SBATCH -e %j.err\n")
        wf.write("#SBATCH --exclusive\n")
        # wf.write("#SBATCH --account={}\n".format(pr_id))
        wf.write("#SBATCH --time={}:00:00\n".format(time))
        wf.write("#SBATCH --nodes=1\n")
        wf.write("#SBATCH --ntasks-per-node={}\n".format(cores))
        wf.write("\n")
        wf.write("module load intel/intelcompiler/2020.4\n")
        # wf.write("module load intel/oneapi/2023.2.0\n")
        wf.write("export PATH=~/data/wt2025/bin/:$PATH\n")
        # wf.write("export MODULEPATH=/online1/paratera_wx_group/pwx_share/modules:$MODULEPATH\n")
        # wf.write("module load conda/conda-zy\n")
        # wf.write("source ~/data/conda/etc/profile.d/conda.sh\n")
        wf.write("source /online1/paratera_wx_group/pwx_share/soft/conda/etc/profile.d/conda.sh\n")
        wf.write("\n")
        wf.write("\n")
        wf.write("conda activate mp_api\n")

        wf.write("\n")
        wf.write("date\n")
        wf.write("\n")


        if CALC[3]:
            wf.write("# Relaxation step\n")
            wf.write("mkdir relax\n")
            wf.write("cp POSCAR POTCAR relax/\n")
            wf.write("mv {} relax/INCAR\n".format(names_relax[0]))
            wf.write("cp {} relax/KPOINTS\n".format(names_relax[1]))
            wf.write("\n")
            wf.write("# Relaxation run\n")
            wf.write("cd relax\n")
            wf.write("mpirun {} > {}\n".format(vasp_dir, vasp_output))
            wf.write("rm WAVECAR CHG CHGCAR PCDAT XDATCAR\n")
            wf.write("cd ../\n")
            wf.write("cp relax/CONTCAR POSCAR\n")
            wf.write("\n")

        if CALC[0]:
            wf.write("# SCF step\n")
            wf.write("# SCF run\n")
            wf.write("mpirun {} > {}\n".format(vasp_dir, vasp_output))
            wf.write("rm WAVECAR CHG CONTCAR EIGENVAL OSZICAR PCDAT XDATCAR\n")
            wf.write("\n")
            # extract band gap
            wf.write("# Extract band gap\n")
            wf.write("gap=$(python3 - << 'EOF'\n")
            wf.write("from pymatgen.io.vasp import Vasprun\n")
            wf.write("vr = Vasprun('vasprun.xml', parse_projected_eigen=False)\n")
            wf.write(
                "print(vr.get_band_structure().get_band_gap()['energy'])\n")
            wf.write("EOF\n")
            wf.write(")\n\n")
            wf.write("echo \"band gap = $gap eV\"\n")
            wf.write("\n")

        if CALC[2]:
            wf.write("# Band step\n")
            wf.write("mkdir band\n")
            wf.write("cp CHGCAR POSCAR POTCAR band/\n")
            wf.write("mv {} band/INCAR\n".format(names_band[0]))
            wf.write("mv {} band/KPOINTS\n".format(names_band[1]))
            wf.write("\n")
            wf.write("# Band run\n")
            wf.write("cd band\n")
            wf.write("mpirun {} > {}\n".format(vasp_dir, vasp_output))
            wf.write("rm WAVECAR CHG CHGCAR CONTCAR PCDAT XDATCAR\n")
            wf.write("cd ../\n")
            wf.write("\n")

        if CALC[1]:
            wf.write("# Wannier step\n")
            wf.write("mkdir wan\n")
            wf.write("cp CHGCAR POSCAR POTCAR wan/\n")
            wf.write("mv {} wan/INCAR\n".format(names_wfs[0]))
            wf.write("mv {} wan/KPOINTS\n".format(names_wfs[1]))
            wf.write("cp autoconstruction.py wan/\n")
            wf.write("\n")
            wf.write("# Wannier run\n")
            wf.write("cd wan/\n")
            wf.write("{} autoconstruction.py\n".format(python_dir))
            wf.write("mpirun {} > {}\n".format(vasp_dir, vasp_output))
            wf.write("{} wannier90 > {}\n".format(
                wann_dir, wannier_output))
            wf.write(   
                "rm WAVECAR CHG EIGENVAL CONTCAR PCDAT XDATCAR\n")
            wf.write("cd ../\n")
            wf.write("\n")

        if CALC[1] and CALC[2]:
            wf.write("# Compare DFT band and Wannier90 band\n")
            wf.write("python compare_band.py\n")

        wf.write("\n")
        wf.write("date\n")
        wf.write("\n")


def search_files_and_dirs():
    my_files, my_dirs = [], []
    for x in os.listdir("."):
        if os.path.isfile(x):
            my_files.append(x)
        elif os.path.isdir(x):
            my_dirs.append(x)
    return my_files, my_dirs


def check_vasp_output_file(my_files, filename, increase_memory):
    if filename in my_files:
        with open(filename, 'r') as rf:
            for i, line in enumerate(rf):
                if increase_memory == False and "out-of-memory" in line:
                    increase_memory = True
                line = line.split()
        if line and line[0] == "writing" and line[1] == "wavefunctions":
            restart = False
        else:
            restart = True
    else:
        restart = True

    return restart, increase_memory


def search_index(data, search_for):
    index = -1
    for i in range(len(data)):
        if data[i][0] == search_for:
            index = i
            break
    return index


def modify_wann90_win(data, tag_exists, cycles, number):
    with open('wannier90.win', 'w') as wf:
        for i in range(len(data)):
            if data[i] and data[i][0] == 'num_iter' and tag_exists == False:
                wf.write("restart = wannierise\n")
            if data[i] and data[i][0] == 'num_iter':
                data[i][2] = cycles-number+1
            for j in range(len(data[i])):
                wf.write("{} ".format(data[i][j]))
            wf.write("\n")


def modify_POSCAR():
    data = []

    with open('POSCAR', "r") as rf:
        for i, line in enumerate(rf):
            line = line.split()
            data.append(line)

    if data[5][0].isdigit():
        with open("POSCAR", "w") as wf:
            for i in range(len(data)):
                for j in range(len(data[i])):
                    wf.write("{} ".format(data[i][j]))
                wf.write("\n")
                if i == 4:
                    for j in range(len(data[0])):
                        wf.write("{} ".format(data[0][j]))
                    wf.write("\n")


def update_tags(incar_tags, magnetism, non_collinearity, soc_tag):

    if magnetism == False:
        non_collinearity = False
        # incar_tags["ispin"] = 1

    if magnetism == True:
        # incar_tags["saxis"] = "0 0 1"
        # incar_tags["amix_mag"] = "0.0001"
        # incar_tags["bmix_mag"] = "0.00001"
        incar_tags["lorbmom"] = ".TRUE."
        # incar_tags["ispin"] = 2

    return incar_tags, non_collinearity, soc_tag


def main():
    # Define files and tags

    names_scf = ['INCAR', 'POTCAR', 'KPOINTS']
    names_wfs = ['INCAR.wfs', 'KPOINTS']
    names_band = ['INCAR.band', 'KPOINTS.band']
    names_relax = ['INCAR.relax', 'KPOINTS']
    submitted = False  # Initial tag for submission (DO NOT MODIFY)
    increase_memory = False  # Initial tag for memory (DO NOT MODIFY)
    in_tags, reason = [], []

    # Read input file

    CALC = input_parameters.calc_type()
    pseudo = input_parameters.pseudopotentials()
    incar_tags, magnetism, non_collinearity, soc_tag, const_tag, u_calc = input_parameters.hte_tags()
    vasp_dir, wann_dir, ps_dir, python_dir, vasp_output, wannier_output = input_parameters.directories()
    cores, time, memory, pr_id = input_parameters.running_parameters()
    u_val, j_val, l_val = input_parameters.ldau_values()
    incar_tags, non_collinearity, soc_tag = update_tags(
        incar_tags, magnetism, non_collinearity, soc_tag)

    for key, value in incar_tags.items():
        temp = [key.upper(), value]
        in_tags.append(temp)

    modify_POSCAR()
    atoms, multiplicity, lat_con = read_POSCAR()
    number_bands = estim_bands(atoms, multiplicity, in_tags, cores)

    FELEM = get_restrictions(atoms)

    submitted = get_POTCAR(pseudo, atoms, submitted, reason, ps_dir)

    # get_KPOINTS(ktyp, lat_con, ksp, names_scf[2])
    get_KPOINTS()
    submitted, all_incar_tags = get_additional_tags(in_tags, const_tag, number_bands, atoms, multiplicity, 
                                                    FELEM, u_calc, u_val, j_val, l_val, submitted, reason, magnetism, non_collinearity, soc_tag, cores)

    lorbit_index = search_index(all_incar_tags, 'lorbit'.upper())

    incar_wfs_tags = get_INCARwfs_tags(all_incar_tags, lorbit_index)
    incar_band_tags = get_INCARband_tags(all_incar_tags, lorbit_index)
    incar_relax_tags = get_INCARrelax_tags(all_incar_tags, lorbit_index)

    if CALC[0]:
        get_file(all_incar_tags, names_scf[0])
    if CALC[1]:
        get_file(incar_wfs_tags, names_wfs[0])
    if CALC[2]:
        get_file(incar_band_tags, names_band[0])
        get_KPOINTS_band()
    if CALC[3]:
        get_file(incar_relax_tags, names_relax[0])

    get_run(CALC, atoms, multiplicity, names_wfs, names_band, names_relax, vasp_dir, wann_dir,
            cores, time, memory, increase_memory, pr_id, python_dir, vasp_output, wannier_output)

    with open('info.dat', 'w') as wf:
        wf.write("Submitted: {} ".format(submitted))
        for i in range(len(reason)):
            wf.write("{} ".format(reason[i]))
    os.system("rm -r __py*")


main()
