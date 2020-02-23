"""
Unit tests for the solver module.
"""

from pyksolve import solver

__author__ = 'Tiziano Bettio'
__license__ = 'MIT'
__version__ = '0.0.5'
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


def test_shuffle1():
    """
    Test the functionality of the shuffle1 method.
    """
    s = solver.Solitaire()
    s.reset_game()
    assert s.shuffle1(7187413) == 7187413
    s.reset_game()
    assert s.shuffle1(-1) != -1


def test_draw_count():
    """
    Test the draw_count property.
    """
    s = solver.Solitaire()
    s.draw_count = 3
    assert s.draw_count == 3


def test_solve_fast():
    """
    Test the solve_minimal method.
    """
    s = solver.Solitaire()
    s.shuffle1(1023536416)
    s.reset_game()
    assert s.solve_fast(0, 0, 5_000_000) in (
        solver.SolveResult.SolvedMinimal,
        solver.SolveResult.SolvedMayNotBeMinimal)
    assert s.moves_made_count == 74


def test_solve_minimal():
    """
    Test the solve_minimal method.
    """
    s = solver.Solitaire()
    s.shuffle1(1023536416)
    s.reset_game()
    assert s.solve_minimal(5_000_000) \
        == solver.SolveResult.SolvedMinimal
    assert s.moves_made_count == 73


def test_solve_minimal_multithreaded():
    """
    Test the solve_minimal_multithreaded method.
    """
    s = solver.Solitaire()
    s.shuffle1(1023536416)
    s.reset_game()
    assert s.solve_minimal_multithreaded(8) \
        == solver.SolveResult.SolvedMinimal
    assert s.moves_made_count == 73


def test_foundation_count():
    """
    Test the foundation_count property.
    """
    s = solver.Solitaire()
    s.shuffle1(1023536416)
    s.reset_game()
    assert s.foundation_count == 0
    assert s.solve_minimal_multithreaded(8) \
        == solver.SolveResult.SolvedMinimal
    assert s.foundation_count == 52
    s.reset_game()
    assert s.foundation_count == 0
