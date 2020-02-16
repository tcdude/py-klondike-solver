Introduction
============

About pyksolve
##############

:mod:`pyksolve` is a wrapper around
`Klondike-Solver <https://github.com/ShootMe/Klondike-Solver>`_ using Cython.


Using pyksolve
##############

Small usage sample
******************

.. code-block:: python

    from pyksolve import solitaire

    s = solitaire.Solitaire()
    s.reset_game()
    s.shuffle1(42)

    print(s.game_diagram())

    result = s.solve_minimal_multithreaded(4)
    if result == solitaire.SolveResult.SolvedMinimal:
        print('Found a solution:\n')
        print(s.moves_made())
    else:
        print(f'No minimal solution found. SolveResult = "{repr(result)}"')


1.  This code creates a :class:`pyksolve.solitaire.Solitaire` instance ``s``
    which is then shuffled with 42 as optionally specified random seed.
2.  It prints out the game diagram after the shuffle, before trying to solve
    with a minimal solution using 4 hardware threads.
3.  Finally it verifies whether a minimal solution was found and either prints
    the corresponding moves made or just what result code was received.

**Spoiler** *To get 42 to work, a "larger computer" is needed, as the*
*SolveResult is:* :attr:`pyksolve.solitaire.SolveResult.CouldNotComplete` *...*
