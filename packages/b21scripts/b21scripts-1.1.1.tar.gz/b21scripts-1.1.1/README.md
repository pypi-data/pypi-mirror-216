# b21scripts

Various scripts, libraries and modules to help with manipulating data and files associated with SAXS experiments and data analysis and particularly suited to the workflow at the B21 SAXS beamline, Diamond Light Source.
The Repository URL is: https://github.com/nathancowieson/b21scripts
The Repository can be found on PyPi: https://pypi.org/project/b21scripts/

Install via pip:
  >> pip install b21scripts

## readwrite
    
The readwrite libraries provied a convenient way to parse various files that might be associated with a SAXS experiment such as .dat files, .pdb files, fit files giving the fit of a model to experimental data and out files containing the output from the indirect Fourier transform as produced by the [ATSAS](https://www.embl-hamburg.de/biosaxs/software.html) program [Gnom](https://www.embl-hamburg.de/biosaxs/gnom.html).

---

### Modules

1. readwrite.dat.DAT
Functions for reading and writing files of type .dat containing three columns of SAXS data, scattering vector Q, intensity and error.

2. readwrite.pdb.PDB
Functions for reading and writing files of type .pdb. These are files describing a molecular structure of the type that might have been downloaded from the [Protein Data Bank](https://www.rcsb.org/). The library can parse such a file into a dictionary and then back out to a valid pdb file. There are functions to allow atomic coordinates to be rotated or translated etc.

## saxs

The saxs libraries contain functions related to calculation and manipulation of SAXS data.

### Modules

1. saxs.saxs_calc.SaxsCalc
A wrapper for running either [FoXS](https://integrativemodeling.org/) or [Crysol](https://www.embl-hamburg.de/biosaxs/crysol.html), parsing the output to capture the Chi^2 score for use in plotting or automatically comparing fits etc. To run either of these programs they must be available on the system path as 'foxs' or 'crysol'.