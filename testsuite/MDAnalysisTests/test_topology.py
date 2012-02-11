# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDAnalysis --- http://mdanalysis.googlecode.com
# Copyright (c) 2006-2011 Naveen Michaud-Agrawal,
#               Elizabeth J. Denning, Oliver Beckstein,
#               and contributors (see website for details)
# Released under the GNU Public Licence, v2 or any higher version
#
# Please cite your use of MDAnalysis in published work:
#
#     N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and
#     O. Beckstein. MDAnalysis: A Toolkit for the Analysis of
#     Molecular Dynamics Simulations. J. Comput. Chem. 32 (2011), 2319--2327,
#     doi:10.1002/jcc.21787
#

import MDAnalysis
from MDAnalysis.topology.core import guess_atom_type, guess_atom_element, get_atom_mass
from MDAnalysis.tests.datafiles import PRMpbc

from numpy.testing import *

def check_atom_type(atype, aname):
    assert_equal(guess_atom_type(aname), atype)

def check_atom_element(element, aname):
    assert_equal(guess_atom_element(aname), element)

class _TestGuessAtomType(object):
    atype = None
    testnames = []
    mass = None
    element = None
    def test_guess_atom_type(self):
        for aname in self.testnames:
            yield check_atom_type, self.atype, aname

    def test_guess_atom_mass(self):
        assert_equal(get_atom_mass(self.atype), self.mass)

    def test_guess_atom_element(self):
        for aname in self.testnames:
            yield check_atom_element, self.element, aname


class TestHydrogen(_TestGuessAtomType):
    atype = 'H'
    element = 'H'
    mass = 1.008
    testnames = ['H', 'HZ', '1HZ', '2HW', 'HE']

class TestCarbon(_TestGuessAtomType):
    atype = 'C'
    element = 'C'
    mass = 12.0110
    testnames = ['C', 'CA']

class TestSodium(_TestGuessAtomType):
    atype = 'NA'
    element = 'NA'
    mass = 22.989770
    testnames = ['NA', 'NA+', 'SOD', 'QN']

class TestPotassium(_TestGuessAtomType):
    atype = 'K'
    element = 'K'
    mass = 39.102
    testnames = ['K', 'K+', 'POT', 'QK']

class TestChloride(_TestGuessAtomType):
    atype = 'CL'
    element = 'CL'
    mass = 35.450
    testnames = ['CL', 'CL-', 'CLA', 'CLAL']

class TestNitrogen(_TestGuessAtomType):
    atype = 'N'
    element = 'N'
    mass = 14.007
    testnames = ['N', 'NZ', 'NE']

class TestPhosphorous(_TestGuessAtomType):
    atype = 'P'
    element = 'P'
    mass = 30.974000
    testnames = ['P', 'PL', 'PO']

class TestSulfur(_TestGuessAtomType):
    atype = 'S'
    element = 'S'
    mass = 32.06000
    testnames = ['S', 'SG']

class TestOxygen(_TestGuessAtomType):
    atype = 'O'
    element = 'O'
    mass = 15.99900
    testnames = ['O', 'OA', 'OXT', '1OG', 'OW']

class TestCalcium(_TestGuessAtomType):
    atype = 'CA'
    element = 'CA'
    mass = 40.080000
    testnames = ['CAL','CA2+', 'C0']

class TestMagnesium(_TestGuessAtomType):
    atype = 'MG'
    element = 'MG'
    mass = 24.305000
    testnames = ['MG', 'MG2+']


# add more...

# specific topology readers

# AMBER

class RefCappedAla(object):
    """Mixin class to provide comparison numbers.

    Capped Ala in water
    """
    PRM = PRMpbc
    ref_numatoms = 5071
    ref_proteinatoms = 22

class TestAmber(TestCase, RefCappedAla):
    def test_TOPParser(self):
        """Testing AMBER PRMTOP parser (Issue 76)"""
        # note: hard to test the issue because one needs a very specifi datafile
        #       so this test really checks that we did not break the parser for the
        #       existing test cases
        U = MDAnalysis.Universe(self.PRM)
        assert_equal(len(U.atoms), self.ref_numatoms, "load topology from PRM")
