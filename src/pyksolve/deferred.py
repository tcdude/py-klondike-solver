"""
Provides the DeferredSolver class that generates a number of solvable games for
faster access to a solvable seed on demand.
"""

import queue
import random
import threading
import time
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from . import solver

__author__ = 'Tiziano Bettio'
__license__ = 'MIT'
__version__ = '0.0.10'
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

MAX_SEED = 2 ** 31 - 1


def _worker(exit_e: threading.Event, e_conf: threading.Event,
            job_q: queue.Queue, res_q: queue.Queue, max_closed: int) -> None:
    """Worker thread -> consumes jobs that are executed in a Solver thread."""
    sol = solver.Solitaire()

    while not exit_e.is_set():
        try:
            seed, draw_count = job_q.get(timeout=0.001)
        except queue.Empty:
            continue
        sol.draw_count = draw_count
        sol.shuffle1(seed)
        sol.reset_game()
        if abs(sol.solve_fast(max_closed).value) == 1:
            res_q.put((seed, sol.draw_count, sol.moves_made()))
        job_q.task_done()
    e_conf.set()


def _filler(exit_e: threading.Event, e_conf:threading.Event, job_q: queue.Queue,
            res_q: queue.Queue, target: int,
            draw_counts: Tuple[int, ...]) -> None:
    """
    Filler thread -> keeps the result Queue filled with approximately the right
    amount of solutions per draw count.
    """
    job_no = 0
    mod = len(draw_counts)
    while not exit_e.is_set():
        if res_q.qsize() < target * mod and job_q.empty():
            job_q.put((random.randint(0, MAX_SEED), draw_counts[job_no % mod]))
            job_no += 1
        time.sleep(0.001)
    e_conf.set()


class DeferredSolver:
    """
    Provides a cache of solved games, that is kept at a user defined number of
    games for each specified draw count. To properly clean up, call
    :meth:`DeferredSolver.stop` when the `DeferredSolver` is no longer needed.

    Args:
        draw_counts: ``Tuple[int, ...]`` -> for which draw count a cache is
            generated. Defaults to `(1, 3)`.
        cache_num: ``int`` -> number of solvable games to cache at any time.
            Defaults to `5`.
        threads: ``int`` -> number of workers to run solvers. Defaults to `3`.
        max_closed: ``int`` -> max_closed argument to be passed to the
            used :meth:`pyksolve.solver.Solitaire.solve_fast` method. Defaults
            to `1,000,000`.

    .. warning::
        If you don't call :meth:`DeferredSolver.stop`, your program might hang
        until terminated forcefully. After :meth:`DeferredSolver.stop` was
        called, the class is defunct!
    """
    def __init__(self, draw_counts: Tuple[int, ...] = (1, 3),
                 cache_num:int = 5, threads:int = 3,
                 max_closed: int = 1_000_000,
                 seed: Optional[int] = None) -> None:
        if not isinstance(draw_counts, tuple):
            raise TypeError('Expected type tuple for argument draw_counts.')
        for draw_count in draw_counts:
            if not 0 < draw_count < 8:
                raise ValueError('Expected draw_counts to lie between 1 and 7.')
        if not isinstance(cache_num, int):
            raise TypeError('Expected type int for argument cache_num.')
        if cache_num < 1:
            raise ValueError('Expected positive value for argument cache_num.')
        if not isinstance(threads, int):
            raise TypeError('Expected type int for argument threads.')
        if threads < 1:
            raise ValueError('Expected positive value for argument threads.')
        if not isinstance(max_closed, int):
            raise TypeError('Expected type int for argument max_closed.')
        if max_closed < 1:
            raise ValueError('Expected positive value for argument max_closed.')
        if seed is not None and not isinstance(seed, int):
            raise TypeError('Expected type int for argument seed.')
        self._job_queue = queue.Queue()
        self._result_queue = queue.Queue()
        self._exit_thread = threading.Event()
        self._exit_conf = (
            [threading.Event() for _ in range(threads)],
            threading.Event()
        )
        self._draw_counts = draw_counts
        self._cache_num = cache_num
        for i in range(threads):
            worker = threading.Thread(target=_worker, args=(self._exit_thread,
                                      self._exit_conf[0][i], self._job_queue,
                                      self._result_queue, max_closed))
            worker.start()
        filler = threading.Thread(target=_filler, args=(self._exit_thread,
                                  self._exit_conf[1], self._job_queue,
                                  self._result_queue, cache_num, draw_counts))
        filler.start()
        self._solved: Dict[int, List[Tuple[int, str]]] = {}
        self._sol = solver.Solitaire()

    def get_solved(self, draw_count: int) -> Tuple[int, str, str]:
        """
        Get a solved game from cache with the specified draw count.

        Args:
            draw_count: ``int`` -> valid draw count value as specified on init.

        Returns:
            Tuple of (seed, game_diagram before solved, moves_made).
        """
        if draw_count not in self._draw_counts:
            raise ValueError(f'Wrong draw_count = {draw_count}')
        if draw_count not in self._solved:
            self._solved[draw_count] = []
        while not len(self._solved[draw_count]):
            seed, g_draw_count, moves_made = self._result_queue.get()
            if g_draw_count not in self._solved:
                self._solved[g_draw_count] = []
            self._sol.shuffle1(seed)
            self._sol.reset_game()
            self._solved[g_draw_count].append((seed, self._sol.game_diagram(),
                                               moves_made))
            self._result_queue.task_done()
        return self._solved[draw_count].pop(0)

    def stop(self):
        """
        Signals all threads to stop.
        """
        self._exit_thread.set()
        while True:
            time.sleep(0.001)
            if not self._exit_conf[1].is_set():
                continue
            clean = True
            for i in self._exit_conf[0]:
                if not i.is_set():
                    clean = False
                    break
            if clean:
                break
