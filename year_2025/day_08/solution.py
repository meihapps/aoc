from collections.abc import Iterable
from functools import reduce
from math import dist
from pprint import pprint


Junction = tuple[int, int, int]
Cable = tuple[Junction, Junction]
Circuits = list[set[Junction]]
Accumulator = tuple[Circuits, Cable | None]


def format_input(sample: bool = False):
    with open(f"{'sample_' if sample else ''}input.txt") as file:
        return [
            (int(x), int(y), int(z))
            for x, y, z in [i.split(",") for i in file.read().strip().split("\n")]
        ]


def part_1() -> int:
    return reduce(
        lambda a, b: a * b,
        sorted(
            (len(i) for i in make_circuits(get_n_cables(format_input(), 1000))[0]),
            reverse=True,
        )[:3],
    )


def get_n_cables(junctions: list[Junction], n: int | None = None):
    connections = sorted(
        [
            (node1, node2)
            for index1, node1 in enumerate(junctions)
            for index2, node2 in enumerate(junctions)
            if index1 < index2
        ],
        key=straight_line_distance,
    )
    return connections if n is None else connections[:n]


def straight_line_distance(
    cable: Cable,
) -> float:
    return dist(*cable)


def part_2():
    _, last_cable = make_circuits(get_n_cables(format_input()))
    assert last_cable is not None
    return last_cable[0][0] * last_cable[1][0]


def find_matching_circuits(circuit_sets: Circuits, cable: Cable) -> list[int]:
    return [
        index
        for index, circuit in enumerate(circuit_sets)
        if cable[0] in circuit or cable[1] in circuit
    ]


def merge_circuits(
    circuit_sets: list[set[Junction]],
    matched_indices: list[int],
    edge: Cable,
) -> list[set[Junction]]:
    remaining = [
        circuit
        for idx, circuit in enumerate(circuit_sets)
        if idx not in matched_indices
    ]
    merged = set().union(  # pyright: ignore[reportUnknownVariableType]
        *(circuit_sets[idx] for idx in matched_indices), {edge[0], edge[1]}
    )
    return remaining + [merged]


def make_circuits_prime(state: Accumulator, edge: Cable) -> Accumulator:
    circuit_sets, last_crossing_edge = state
    node_a, node_b = edge

    match find_matching_circuits(circuit_sets, edge):
        case []:
            return circuit_sets + [{node_a, node_b}], (node_a, node_b)

        case [primary_index]:
            circuit = circuit_sets[primary_index]
            updated_circuit = circuit | {node_a, node_b}
            crossing_edge = (
                edge
                if (node_a in circuit) ^ (node_b in circuit)
                else last_crossing_edge
            )

            return (
                circuit_sets[:primary_index]
                + [updated_circuit]
                + circuit_sets[primary_index + 1 :],
                crossing_edge,
            )

        case [_, *_] as matched_indices:
            return merge_circuits(
                circuit_sets, matched_indices, edge
            ), last_crossing_edge

        case _:
            assert False


def make_circuits(connections: Iterable[Cable]) -> Accumulator:
    return reduce(make_circuits_prime, connections, ([], None))


pprint(part_1())
print(part_2())
