"""
Unit tests for the deferred module.
"""

from pyksolve import deferred

__author__ = 'Tiziano Bettio'
__license__ = 'MIT'
__version__ = '0.0.6'
__copyright__ = """
Copyright (c) 2020 Tiziano Bettio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def test_deferred_solver():
    """
    Test the functionality of the deferred_solver.
    """
    d = deferred.DeferredSolver(draw_counts=(1, 2, 3), cache_num=1, threads=3)
    seed, diagram, moves = d.get_solved(1)
    assert seed > 0
    assert diagram != ''
    assert moves != ''
    seed, diagram, moves = d.get_solved(2)
    assert seed > 0
    assert diagram != ''
    assert moves != ''
    seed, diagram, moves = d.get_solved(3)
    assert seed > 0
    assert diagram != ''
    assert moves != ''
