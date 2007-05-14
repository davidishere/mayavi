"""Elementary tests for wrapper_gen.py.

This test suite is not comprehensive because it is very hard to test
wrapper_gen directly.

"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2004, Prabhu Ramachandran,  Enthought, Inc.
# License: BSD Style.

import unittest
import vtk

from enthought.tvtk import wrapper_gen

_cache = wrapper_gen.WrapperGenerator()


class TestWrapperGenerator(unittest.TestCase):
    def setUp(self):
        self.wg = _cache
        
    def test_find_type(self):
        wg = self.wg
        sigs = ['int', 'vtkOpenGLVolumeMapper',
                ('int', 'int', 'float', 'list'),
                ('int', 'vtkActor', 'vtkXMLReader'),
                ['vtkImageActor', 'vtkExporter'],
                ['int', 'vtkDataArray', 'vtkCellArray',
                 'vtkIdTypeArray']
                ]
        expect = ['basic', 'vtk', 'basic', 'vtk', 'vtk', 'array']
        for i, sig in enumerate(sigs):
            self.assertEqual(expect[i], wg._find_type(sig))

    def test_sig_types(self):
        wg = self.wg
        meths = [vtk.vtkProperty.GetColor,
                 vtk.vtkProperty.GetRepresentation,
                 vtk.vtkStructuredPointsReader.GetOutput,
                 vtk.vtkPolyData.SetPoints,
                 vtk.vtkPolyData.SetPolys,
                 vtk.vtkQuad.CellBoundary,
                 vtk.vtkContourFilter.SetLocator
                 ]
        expect = [('basic', 'basic'),
                  ('basic', None),
                  ('vtk', 'basic'),
                  ('basic', 'array'),
                  ('basic', 'array'),
                  ('basic', 'array'),
                  ('basic', 'vtk'),                  
                  ]
        for i, meth in enumerate(meths):
            sig = wg.parser.get_method_signature(meth)
            self.assertEqual(expect[i], wg._find_sig_type(sig))
        sig = [(['int'], ['int']),
               (['vtkStructuredPoints'], ['vtkFooClass'])]
        self.assertEqual(('vtk', 'vtk'), wg._find_sig_type(sig))

def test_suite():
    """Collects all the tests to be run."""
    suites = []
    suites.append(unittest.makeSuite(TestWrapperGenerator, 'test_'))
    total_suite = unittest.TestSuite(suites)
    return total_suite

def test(verbose=2):
    """Useful when you need to run the tests interactively."""
    all_tests = test_suite()
    runner = unittest.TextTestRunner(verbosity=verbose)
    result = runner.run(all_tests)
    return result, runner

if __name__ == "__main__":
    unittest.main()
