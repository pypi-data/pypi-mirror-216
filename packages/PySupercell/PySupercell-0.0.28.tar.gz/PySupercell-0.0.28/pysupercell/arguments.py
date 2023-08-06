#!/usr/bin/env python


#===========================================================================#
#                                                                           #
#  File:       arguments.py                                                 #
#  Dependence: none                                                         #
#  Usage:      process with arguments                                       #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       May 15, 2020                                                 #
#                                                                           #
#===========================================================================#


import argparse
import os
import sys
pyver=sys.version_info[:2]

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):    return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):  return False
    else: raise argparse.ArgumentTypeError('Unsupported value encountered.')


def add_control_arguments(parser):
    parser.add_argument('--source',type=str,default='VASP',help='source file type: VASP/QE/Abinit')
    parser.add_argument('--restart',type=str2bool,const=False,default=False,nargs='?',help='restart mode or not')
    parser.add_argument('--outdir',type=str,default='./tmp',help='directory to store temporary files')
    parser.add_argument('--task',type=str,default=None,help='task to process')
    parser.add_argument('--irr_to_BZ',type=str2bool,nargs='?',const=False,help='map kpts in irreducible BZ to 1st BZ')
    parser.add_argument('--redefine_ibrav',type=str2bool,nargs='?',const=False,help='To define the ibrav manually or not') 


def add_io_arguments(parser):
    parser.add_argument('--poscar', type=str, default='POSCAR', help='POSCAR file')
    parser.add_argument('--poscar1',type=str,default='POSCAR1',help='the first POSCAR file')
    parser.add_argument('--poscar2',type=str,default='POSCAR2',help='the second POSCAR file')
    parser.add_argument('--foutcar',type=str,default='OUTCAR',help='the VASP OUTCAR file')
    parser.add_argument('--filpw',type=str,default='scf.in',help='QE pw.x input file with structures')
    parser.add_argument('--filcif',type=str,default='ph.out',help='cif file')
    parser.add_argument('--verbosity',type=int,default=1,help='level of verbosity')


def add_structure_arguments(parser):
    parser.add_argument('--sc1',type=eval,default=(1,0,0), help='sc1')
    parser.add_argument('--sc2',type=eval,default=(0,1,0), help='sc2')
    parser.add_argument('--sc3',type=eval,default=(0,0,1), help='sc3')
    parser.add_argument('--cell_orientation',type=int,default=0, help='orientation of redefined cell')
 
    parser.add_argument('--hkl',type=str,default='111',help='the Miller index to build slab model')
    parser.add_argument('--thickness',type=int,default=2,help='the thickness of the slab')
    parser.add_argument('--vacuum',type=float,default=20,help='the vacuum distance of slab model in Angstrom')
    parser.add_argument('--chiral_num',type=eval,default=(3,3),help='number to define the chiral vector of nanotube')
    parser.add_argument('--negative_R',type=str2bool,default=False,help='Negative R folds the sheet in opposite direction')
    parser.add_argument('--atom_index',type=eval,default=None,help='indices for two ions to calculate the distance')
    parser.add_argument('--atom_shift',type=float,default=0,help='shift atoms for building slab in layered structures')

    parser.add_argument('--nn',type=int,default=10,help='number of cells to repeat')
    parser.add_argument('--amp',type=float,default=0.5,help='amplitude of the bending curve')
    parser.add_argument('--idir_per',type=int,default=0,help='latt vector index, for repeation')
    parser.add_argument('--idir_bend',type=int,default=2,help='latt vector index, for bending')
    parser.add_argument('--central_z',type=float,default=0.5,help='height for the central layer of the film (for bending) in frac coord')

    parser.add_argument('--screw_center',type=eval,default=[0.5,0.5,0.5],help='center of a screw dislocation in fractional coord.')
    parser.add_argument('--screw_normal',type=eval,default=[0.,1.,0.],help='normal vector of the glide plane for a screw dislocation.')
    parser.add_argument('--screw_idir',type=int,default=2,help='direction of screw dislocation: 0/1/2 for x/y/z')
    parser.add_argument('--burgers_vector',type=eval,default=[0,0,1],help='Burgers vector in fractional coord.')
    parser.add_argument('--display_structure',type=str2bool,default=False,help='display the structure with screw dislocation')

    parser.add_argument('--strain',type=eval,default=0,help='magnitude of strain')
    parser.add_argument('--strain_dirs',type=eval,default=None,help='directions for strain, along crystal axes')
    parser.add_argument('--angle',type=float,default=0,help='angle to rotate the crystal axes')
    parser.add_argument('--symmprec',type=float,default=1E-4,help='accuracy to find crystal symmetry in Angstrom')
    parser.add_argument('--case',type=str,default='case',help='case name for wien2k input')
    parser.add_argument('--kgrid',type=float,default=0.02,help='density of kgrid, in unit of 2pi/Angs')
    parser.add_argument('--idir_shift',type=int,default=2,help='latt vector index, for shifting')
    parser.add_argument('--shift',type=float,default=1,help='atom shift distance along certain direction')
    parser.add_argument('--to_home',type=str2bool,default=True,help='shift atom coordinates to home cell or not')
    parser.add_argument('--inv_center',type=eval,default=(0,0,0),help='Inversion center to transform the structure')
    parser.add_argument('--nimages',type=int,default=5,help='Number of images to interpolate two structures')
    parser.add_argument('--sort_atoms',type=str2bool,default=True,help='Sort atoms in POSCAR2 accordingly to POSCAR1')
 


def add_plotting_arguments(parser):
    parser.add_argument('--scatter_size',type=int,default=10,help='Size of markers in plots')
    parser.add_argument('--cmap',type=str,default='turbo',help='colormap for visulization')


if __name__=='__main__':
    print ('\nthis is a collection of arguments')
