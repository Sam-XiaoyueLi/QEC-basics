"""Check the repetition-code examples using exact probabilities.

Run with --with-stim for circuit/DEM and matching checks.
No BP or BeliefMatching result is computed here.
"""

from argparse import ArgumentParser
from fractions import Fraction as Q
from itertools import product
from math import isclose, log, prod


DEM = """error(0.1) D0 L0
error(0.1) D1 D2
error(0.1) D3
error(0.02) D0 D1 ^ D2 D3
"""


def syndrome(pattern):
    return tuple(a ^ b for a, b in zip(pattern, pattern[1:]))


def probability(bits, rates):
    return prod(p if bit else 1 - p for bit, p in zip(bits, rates))


def exact_checks():
    assert syndrome((0, 1, 0)) == (1, 1)
    observed = (1, 1, 1, 1)
    rates = (Q(1, 10), Q(1, 10), Q(1, 10), Q(1, 50))
    true_distribution = {}
    one_check_total = Q(0)
    one_check_with_f = Q(0)
    all_check_with_f = Q(0)
    total = Q(0)
    for events in product((0, 1), repeat=4):
        a, b, c, f = events
        x = (a, f, b, f, c)
        p = probability(events, rates)
        total += p
        s = syndrome(x)
        if s[0]:
            one_check_total += p
            if f:
                one_check_with_f += p
        if s == observed:
            true_distribution[x] = p
            if f:
                all_check_with_f += p
    assert total == 1
    assert true_distribution == {
        (0, 1, 0, 1, 0): Q('0.01458'),
        (1, 0, 1, 0, 1): Q('0.00098'),
    }
    one_check_posterior = one_check_with_f / one_check_total
    posterior = all_check_with_f / sum(true_distribution.values())
    assert one_check_posterior == Q(9, 58)
    assert posterior == Q(729, 778)
    assert true_distribution[(0, 1, 0, 1, 0)] / true_distribution[(1, 0, 1, 0, 1)] == Q(729, 49)

    independent_rates = (Q(1, 10), Q(1, 50), Q(1, 10), Q(1, 50), Q(1, 10))
    approximate_distribution = {}
    total = Q(0)
    for x in product((0, 1), repeat=5):
        p = probability(x, independent_rates)
        total += p
        if syndrome(x) == observed:
            approximate_distribution[x] = p
    assert total == 1
    assert approximate_distribution == {
        (0, 1, 0, 1, 0): Q('0.0002916'),
        (1, 0, 1, 0, 1): Q('0.0009604'),
    }
    actual = max(true_distribution, key=true_distribution.get)
    inferred = max(approximate_distribution, key=approximate_distribution.get)
    assert actual == (0, 1, 0, 1, 0)
    assert inferred == (1, 0, 1, 0, 1)
    residual = tuple(a ^ b for a, b in zip(actual, inferred))
    assert residual == (1, 1, 1, 1, 1)
    assert syndrome(residual) == (0, 0, 0, 0)
    assert actual[0] != inferred[0]  # Logical Z1 readout flips differ.

    for x, p in approximate_distribution.items():
        cost = sum(log(float((1 - r) / r)) for bit, r in zip(x, independent_rates) if bit)
        baseline = probability((0, 0, 0, 0, 0), independent_rates)
        assert isclose(cost, -log(float(p / baseline)))
    print('Exact enumeration: 16 shared-event combinations and 32 independent patterns passed.')
    print(f'P(F | first detector) = {one_check_posterior} = {float(one_check_posterior):.10f}')
    print(f'P(F | syndrome 1111) = {posterior} = {float(posterior):.10f}')
    print(f'Matching costs: 01010 = {2 * log(49):.7f}; 10101 = {3 * log(9):.7f}')
    print('Model preferences: shared event -> 01010; independent approximation -> 10101.')


def stim_checks():
    import stim
    import pymatching
    import numpy as np

    # A known logical-zero state supplies the fault-free reference.
    # Perfect MPP checks make this the static toy, not a noisy extraction circuit.
    circuit = stim.Circuit('''R 0 1 2 3 4
X_ERROR(0.1) 0 2 4
CORRELATED_ERROR(0.02) X1 X3
MPP Z0*Z1 Z1*Z2 Z2*Z3 Z3*Z4 Z0
DETECTOR rec[-5]
DETECTOR rec[-4]
DETECTOR rec[-3]
DETECTOR rec[-2]
OBSERVABLE_INCLUDE(0) rec[-1]
''')
    dem = stim.DetectorErrorModel(DEM)

    def effects(model):
        result = {}
        for instruction in model.flattened():
            if instruction.type != 'error':
                continue
            detectors, logicals = set(), set()
            for target in instruction.targets_copy():
                if target.is_relative_detector_id():
                    detectors.symmetric_difference_update((target.val,))
                elif target.is_logical_observable_id():
                    logicals.symmetric_difference_update((target.val,))
            key = (tuple(sorted(detectors)), tuple(sorted(logicals)))
            assert key not in result
            result[key] = instruction.args_copy()[0]
        return result

    generated = effects(circuit.detector_error_model())
    supplied = effects(dem)
    assert generated.keys() == supplied.keys()
    assert all(isclose(p, supplied[key]) for key, p in generated.items())
    assert dem.num_detectors == 4 and dem.num_observables == 1

    # Check the graph, not just the final logical bit: it must be 10101.
    matching = pymatching.Matching.from_detector_error_model(dem)
    # The supplied DEM still has one shared event. Its two graph components
    # each receive p=.02 and weight ln(49) for independent-edge scoring.
    for u, v in ((0, 1), (2, 3)):
        edge = matching.get_edge_data(u, v)
        assert isclose(edge['error_probability'], 0.02)
        assert isclose(edge['weight'], log(49))
    s = np.ones(4, dtype=np.uint8)
    prediction, weight = matching.decode(s, return_weight=True)
    selected = {tuple(sorted(map(int, row))) for row in matching.decode_to_edges_array(s)}
    assert selected == {(-1, 0), (1, 2), (-1, 3)}
    assert prediction.tolist() == [1]
    # Matching quantizes/rescales weights internally; allow numerical rounding.
    assert isclose(weight, 3 * log(9), rel_tol=1e-6)
    print(f'Stim {stim.__version__}: generated DEM and supplied shared-event DEM agree.')
    print(f'PyMatching {pymatching.__version__}: ordinary matching selects 10101 and predicts L0=1.')

    correlated = pymatching.Matching.from_detector_error_model(dem, enable_correlations=True)
    corr_prediction = correlated.decode(s, enable_correlations=True)
    corr_edges = correlated.decode_to_edges_array(s, enable_correlations=True)
    corr_selected = {tuple(sorted(map(int, row))) for row in corr_edges}
    # Report the actual heuristic result rather than assuming it equals exact ML.
    if corr_selected == {(-1, 0), (1, 2), (-1, 3)}:
        pattern = '10101'
    elif corr_selected == {(0, 1), (2, 3)}:
        pattern = '01010'
    else:
        raise AssertionError(f'Unexpected syndrome-1111 edge set: {corr_selected}')
    assert corr_prediction.tolist() == [int(pattern[0])]
    print(f'PyMatching {pymatching.__version__}: two-pass correlated matching selects {pattern} and predicts L0={int(pattern[0])}.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--with-stim', action='store_true', help='also verify Stim and report ordinary/correlated matching')
    args = parser.parse_args()
    exact_checks()
    if args.with_stim:
        stim_checks()
