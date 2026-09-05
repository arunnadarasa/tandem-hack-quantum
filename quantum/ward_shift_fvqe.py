#!/usr/bin/env python3
"""F-VQE-style filtering optimizer for the 4q ward shift-split (Amaro et al. 2022,
Quantum Sci. Technol. 7 015021 — job scheduling with filtering VQE on Quantinuum).

Honest scope: training loop runs on an exact numpy statevector (noiseless,
classical optimization — standard VQE practice); the FINAL trained circuit is
submitted to Nexus H1-1LE for a certified sampled receipt, directly comparable
to the unoptimized QAOA p=1 baseline (opt-mass 0.1875).

Method: hardware-efficient ansatz (Ry layers + CX ring), maximize <f^2(H)> with
exponential filtering f(E) = exp(-tau*E/2) (H = -cut, so optimum states get the
largest filter weight). Parameter-shift gradients, plain gradient ascent.
"""
import json, time, math
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
EDGES = [(0, 1, 3), (1, 2, 1), (2, 3, 4), (3, 0, 2)]
N, LAYERS, TAU, ETA, ITERS, SEED = 4, 2, 0.6, 0.4, 120, 11

def cut(bits):
    return sum(w for i, j, w in EDGES if bits[i] != bits[j])

# diagonal energies H = -cut  (minimize H == maximize cut)
ENERGIES = np.array([-cut([(m >> i) & 1 for i in range(N)]) for m in range(2 ** N)])
FILTER2 = np.exp(-TAU * (ENERGIES - ENERGIES.min()))  # f^2(H), shifted for stability
OPT_STATES = {m for m in range(16) if -ENERGIES[m] == 10}  # {0b0101,0b1010} order-checked below

def apply_ry(state, q, theta):
    c, s = math.cos(theta / 2), math.sin(theta / 2)
    st = state.reshape([2] * N)
    sl0 = [slice(None)] * N; sl0[N - 1 - q] = 0
    sl1 = [slice(None)] * N; sl1[N - 1 - q] = 1
    a, b = st[tuple(sl0)].copy(), st[tuple(sl1)].copy()
    st[tuple(sl0)] = c * a - s * b
    st[tuple(sl1)] = s * a + c * b
    return st.reshape(-1)

def apply_cx(state, ctrl, tgt):
    st = state.reshape([2] * N)
    sl10 = [slice(None)] * N; sl10[N - 1 - ctrl] = 1; sl10[N - 1 - tgt] = 0
    sl11 = [slice(None)] * N; sl11[N - 1 - ctrl] = 1; sl11[N - 1 - tgt] = 1
    a, b = st[tuple(sl10)].copy(), st[tuple(sl11)].copy()
    st[tuple(sl10)], st[tuple(sl11)] = b, a
    return st.reshape(-1)

def run_ansatz(params):
    state = np.zeros(2 ** N); state[0] = 1.0
    k = 0
    for _ in range(LAYERS):
        for q in range(N):
            state = apply_ry(state, q, params[k]); k += 1
        for q in range(N):
            state = apply_cx(state, q, (q + 1) % N)
    for q in range(N):  # final rotation layer
        state = apply_ry(state, q, params[k]); k += 1
    return state

N_PARAMS = N * (LAYERS + 1)

def objective(params):
    probs = run_ansatz(params) ** 2
    return float(probs @ FILTER2)

def opt_mass(params):
    probs = run_ansatz(params) ** 2
    return float(sum(probs[m] for m in OPT_STATES))

def main():
    # sanity: bitstring order — index m read little-endian, q0 = LSB
    assert sorted(OPT_STATES) == [0b0101, 0b1010], sorted(OPT_STATES)
    rng = np.random.default_rng(SEED)
    params = rng.uniform(0, 2 * math.pi, N_PARAMS)
    hist = []
    for it in range(ITERS):
        grad = np.zeros(N_PARAMS)
        for j in range(N_PARAMS):  # parameter shift
            p = params.copy(); p[j] += math.pi / 2; f_plus = objective(p)
            p[j] -= math.pi;    f_minus = objective(p)
            grad[j] = 0.5 * (f_plus - f_minus)
        params += ETA * grad
        if it % 20 == 0 or it == ITERS - 1:
            om = opt_mass(params)
            hist.append({"iter": it, "objective": round(objective(params), 4),
                         "opt_mass": round(om, 4)})
            print(f"iter {it:3d} obj={objective(params):.4f} opt_mass={om:.4f}")
    probs = run_ansatz(params) ** 2
    top = sorted(((format(m, '04b')[::-1], round(float(p), 4)) for m, p in enumerate(probs)),
                 key=lambda x: -x[1])[:6]
    out = {"method": "F-VQE-style exponential filtering (Amaro 2022 inspired)",
           "ansatz": f"Ry x{LAYERS + 1} layers + CX ring, {N_PARAMS} params",
           "tau": TAU, "eta": ETA, "iters": ITERS, "seed": SEED,
           "training": "exact statevector (noiseless, classical loop — honest scope)",
           "final_opt_mass_noiseless": round(opt_mass(params), 4),
           "qaoa_baseline_h1_1le": 0.1875, "uniform": 0.125,
           "top_states_bitorder_q0_first": top, "history": hist,
           "params": [round(float(x), 6) for x in params]}
    (HERE / "ward_shift_fvqe_training.json").write_text(json.dumps(out, indent=2))
    print("final noiseless opt_mass:", out["final_opt_mass_noiseless"])
    print("top states:", top)

if __name__ == "__main__":
    main()
