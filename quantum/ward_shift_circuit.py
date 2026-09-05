#!/usr/bin/env python3
"""WardFlow shift-split QAOA toy — standalone circuit builder for slides/demos.

4 qubits (one per job), Max-Cut ring, QAOA p=1. Angles in HALFTURNS
(pytket convention). Classical optimum: cut=10, states 0101 / 1010.
Run with the Hermes venv python (qnexus + pytket live there).
"""
from pytket import Circuit
from pytket.circuit import OpType

EDGES = [(0, 1, 3), (1, 2, 1), (2, 3, 4), (3, 0, 2)]
GAMMA, BETA = 0.5, 0.4

def build_circuit() -> Circuit:
    c = Circuit(4, 4)
    for q in range(4):
        c.H(q)
    for i, j, w in EDGES:
        c.add_gate(OpType.ZZPhase, GAMMA * w, [i, j])
    for q in range(4):
        c.add_gate(OpType.Rx, BETA, [q])
    for q in range(4):
        c.Measure(q, q)
    return c

if __name__ == "__main__":
    print(build_circuit().get_commands())
