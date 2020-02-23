# distutils: language = c++

"""
Provides the wrapped main function of "KlondikeSolver.cpp".
"""

from enum import Enum

from cython.operator cimport dereference as deref
from libcpp.memory cimport unique_ptr
from libcpp.string cimport string

from .cppsolitaire cimport SolveResult as _SolveResult
from .cppsolitaire cimport Solitaire as _Solitaire
from .cppsolitaire cimport Move as _Move


__author__ = 'Tiziano Bettio'
__license__ = 'MIT'
__version__ = '0.0.5'
__copyright__ = """Copyright (c) 2020 Tiziano Bettio

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
SOFTWARE."""


class SolveResult(Enum):
    """
    Solve result enum.
    """
    CouldNotComplete = -2
    SolvedMayNotBeMinimal = -1
    Impossible = 0
    SolvedMinimal = 1


cdef class Solitaire:
    """
    Wrapper around the Solitaire C++ class from Klondike-Solver.
    """
    cdef unique_ptr[_Solitaire] thisptr

    def __cinit__(self):
        self.thisptr.reset(new _Solitaire())
        deref(self.thisptr).Initialize()

    def shuffle1(self, deal_number=-1):
        """
        Calls the `Shuffle1` method.

        Args:
            deal_number: ``int`` -> Optional random seed.

        Returns:
            ``int`` -> Random seed used to shuffle.
        """
        return self._shuffle1(deal_number)

    cdef int _shuffle1(self, deal_number=-1):
        return deref(self.thisptr).Shuffle1(deal_number)

    def shuffle2(self, deal_number):
        """
        Calls the `Shuffle2` method.

        Args:
            deal_number: ``int`` -> Random seed.
        """
        self._shuffle2(deal_number)

    cdef void _shuffle2(self, deal_number):
        deref(self.thisptr).Shuffle2(deal_number)

    def reset_game(self, draw_count=None):
        """
        Calls the `ResetGame` method.

        Args:
            draw_count: ``int`` -> Number of cards drawn for each draw move.
        """
        if draw_count is None:
            self._reset_game_default()
        else:
            self._reset_game(draw_count)

    cdef void _reset_game_default(self):
        deref(self.thisptr).ResetGame()

    cdef void _reset_game(self, int draw_count):
        deref(self.thisptr).ResetGame(draw_count)

    def solve_minimal_multithreaded(self, num_threads, max_closed_count=None):
        """
        Attempts to find a minimal solution, using multiple threads.

        Args:
            num_threads: ``int`` -> Number of threads to use.
            max_closed_count: ``Optional[int]`` -> Maximum number of game states
                to evaluate before terminating. Defaults to `5,000,000`.

        Returns:
            :class:`SolveResult` -> The result of the attempt.
        """
        return SolveResult(self._solve_minimal_multithreaded(
            num_threads, max_closed_count or 5_000_000))

    cdef int _solve_minimal_multithreaded(
            self, int num_threads, int max_closed_count):
        cdef int res
        with nogil:
            res = deref(self.thisptr).SolveMinimalMultithreaded(num_threads,
                max_closed_count)
        return res

    def solve_minimal(self, max_closed_count=None):
        """
        Attempts to find a minimal solution.

        Args:
            max_closed_count: ``Optional[int]`` -> Maximum number of game states
                to evaluate before terminating. Defaults to `5,000,000`.

        Returns:
            :class:`SolveResult` -> The result of the attempt.
        """
        return SolveResult(self._solve_minimal(max_closed_count or 5_000_000))

    cdef int _solve_minimal(self, int max_closed_count):
        cdef int res
        with nogil:
            res = deref(self.thisptr).SolveMinimal(max_closed_count)
        return res

    def solve_fast(self, two_shift=0, three_shift=0, max_closed_count=None):
        """
        Attempts to find a fast but possibly not minimal solution.

        Args:
            two_shift: ``Optional[int]`` ->
            three_shift: ``Optional[int]`` ->
            max_closed_count: ``Optional[int]`` -> Maximum number of game states
                to evaluate before terminating. Defaults to `5,000,000`.

        Returns:
            :class:`SolveResult` -> The result of the attempt.
        """
        return SolveResult(self._solve_fast(
            two_shift, three_shift, max_closed_count or 5_000_000))

    cdef int _solve_fast(
            self, int two_shift, int three_shift, int max_closed_count):
        cdef int res
        with nogil:
            res = deref(self.thisptr).SolveFast(max_closed_count, two_shift,
                three_shift)
        return res

    @property
    def moves_made_count(self):
        """``int`` -> Output of "MovesMadeCount()"."""
        return deref(self.thisptr).MovesMadeCount()

    @property
    def moves_made_normalized_count(self):
        """``int`` -> Output of "MovesMadeNormalizedCount()"."""
        return deref(self.thisptr).MovesMadeNormalizedCount()

    @property
    def foundation_count(self):
        """``int`` -> Output of "FoundationCount()"."""
        return deref(self.thisptr).FoundationCount()

    @property
    def draw_count(self):
        """
        ``int`` -> Number of cards drawn for each draw move.

        Setter:
            ``int``
        """
        return deref(self.thisptr).DrawCount()

    @draw_count.setter
    def draw_count(self, value):
        self._set_draw_count(value)

    cdef _set_draw_count(self, int draw_count):
        deref(self.thisptr).SetDrawCount(draw_count)

    def get_move_info(self, move_index):
        """
        Move info as KlondikeSolver provides it.

        Args:
            move_index: ``int`` -> valid move index.
        """
        return self._get_move_info(move_index)

    cdef _get_move_info(self, int move_index):
        cdef string s = deref(self.thisptr).GetMoveInfo(
            deref(self.thisptr)[move_index])
        return s.decode('utf-8')

    def load_solitaire(self, card_set):
        """
        Load a card set in the default format.

        Args:
            card_set: ``str`` -> The card set in the default format.
        """
        return self._load_solitaire(card_set.encode('utf-8'))

    cdef bint _load_solitaire(self, string card_set):
        return deref(self.thisptr).LoadSolitaire(card_set)

    def get_solitaire(self):
        """
        Get the current card set.

        Returns:
            ``str`` -> The card set in the default format.
        """
        return deref(self.thisptr).GetSolitaire().decode('utf-8')

    def load_pysol(self, card_set):
        """
        Load a card set in the PySol format.

        Args:
            card_set: ``str`` -> The card set in the PySol format.
        """
        return self._load_pysol(card_set.encode('utf-8'))

    cdef bint _load_pysol(self, string card_set):
        return deref(self.thisptr).LoadPysol(card_set)

    def get_pysol(self):
        """
        Get the current card set in PySol format.

        Returns:
            ``str`` -> The card set in the PySol format.
        """
        return deref(self.thisptr).GetPysol().decode('utf-8')

    def game_diagram(self):
        """
        Get the current game diagram in the default format.

        Returns:
            ``str`` -> The game diagram in the default format.
        """
        return deref(self.thisptr).GameDiagram().decode('utf-8')

    def game_diagram_pysol(self):
        """
        Get the current game diagram in PySol format.

        Returns:
            ``str`` -> The game diagram in the PySol format.
        """
        return deref(self.thisptr).GameDiagramPysol().decode('utf-8')

    def moves_made(self):
        """
        Get a space delimited list of the moves made to solve.

        Returns:
            ``str`` -> The moves delimited by single spaces.
        """
        return deref(self.thisptr).MovesMade().decode('utf-8')
