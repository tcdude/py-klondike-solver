# distutils: language = c++
"""
Provides Cython header for "Solitaire.h".
"""

from libcpp.string cimport string

__author__ = 'Tiziano Bettio'
__license__ = 'MIT'
__version__ = '0.0.6'
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


cdef extern from "Move.cpp":
    pass

cdef extern from "Move.h":
    cdef struct Move:
        pass

cdef extern from "Card.cpp":
    pass

cdef extern from "Card.h":
    pass

cdef extern from "HashMap.h":
    pass

cdef extern from "Pile.cpp":
    pass

cdef extern from "Pile.h":
    pass

cdef extern from "Random.cpp":
    pass

cdef extern from "Random.h":
    pass

cdef extern from "Solitaire.cpp":
    pass

cdef extern from "Solitaire.h":
    cdef enum SolveResult "SolveResult":
        CouldNotComplete = -2,
        SolvedMayNotBeMinimal = -1,
        Impossible = 0,
        SolvedMinimal = 1


    cdef cppclass Solitaire:
        void Initialize()
        int Shuffle1(int dealNumber)
        void Shuffle2(int dealNumber)
        void ResetGame()
        void ResetGame(int drawCount)
        SolveResult SolveMinimalMultithreaded(int numThreads, int maxClosedCount) nogil
        SolveResult SolveMinimal(int maxClosedCount) nogil
        SolveResult SolveFast(int maxClosedCount, int twoShift, int threeShift) nogil
        int MovesMadeCount()
        int MovesMadeNormalizedCount()
        int FoundationCount()
        int DrawCount()
        void SetDrawCount(int drawCount)
        string GetMoveInfo(Move move)
        bint LoadSolitaire(const string& cardSet)
        string GetSolitaire()
        bint LoadPysol(const string& cardSet)
        string GetPysol()
        string GameDiagram()
        string GameDiagramPysol()
        string MovesMade()
        Move operator[](int index)
