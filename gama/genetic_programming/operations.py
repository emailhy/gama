import random
from typing import List

from gama.genetic_programming.components import Primitive, Terminal, PrimitiveNode, DATA_TERMINAL, Individual


def random_terminals_for_primitive(primitive_set: dict, primitive: Primitive) -> List[Terminal]:
    """ Return a list with a Terminal matching each terminal type the Primitive requires. """
    return [random.choice(primitive_set[needed_terminal_type]) for needed_terminal_type in primitive.input]


def random_primitive_node(output_type: str, primitive_set: dict, exclude: Primitive = None) -> PrimitiveNode:
    """ Create a PrimitiveNode with a Primitive of specified output_type, with random terminals. """
    primitive = random.choice([p for p in primitive_set[output_type] if p != exclude])
    terminals = random_terminals_for_primitive(primitive_set, primitive)
    return PrimitiveNode(primitive, data_node=DATA_TERMINAL, terminals=terminals)


def create_random_expression(primitive_set: dict, min_length: int = 1, max_length: int = 3) -> PrimitiveNode:
    """ Create an PrimitiveNode with at least `min_length` and at most `max_length` chained PrimitiveNodes. """
    individual_length = random.randint(min_length, max_length)
    learner_node = random_primitive_node(output_type='prediction', primitive_set=primitive_set)
    last_primitive_node = learner_node
    for _ in range(individual_length - 1):
        primitive_node = random_primitive_node(output_type=DATA_TERMINAL, primitive_set=primitive_set)
        last_primitive_node._data_node = primitive_node
        last_primitive_node = primitive_node
    return learner_node


def create_seeded_expression(primitive_set: dict, main: Primitive, min_length: int = 1, max_length: int = 3) -> Individual:
    """ Create an individual with at least `min_length` Primitives and at most `max_length` Primitives that
        has `main` as learner node. """
    individual_length = random.randint(min_length, max_length)
    terminals = random_terminals_for_primitive(primitive_set, main)
    learner_node = PrimitiveNode(main, data_node=DATA_TERMINAL, terminals=terminals)
    last_primitive_node = learner_node

    for _ in range(individual_length - 1):
        primitive_node = random_primitive_node(output_type=DATA_TERMINAL, primitive_set=primitive_set)
        last_primitive_node._data_node = primitive_node
        last_primitive_node = primitive_node

    return learner_node


def create_expression_by_rule(primitive_set, rule):
    pipeline = rule.generate()
    learner = last = None
    for emission in reversed(pipeline):
        primitive = emission.primitive
        terminals = random_terminals_for_primitive(primitive_set, primitive)
        if emission.parameters is not None:
            for p,v in emission.parameters.items():
                tindex = primitive.input.index(p)
                if tindex >= 0:
                    terminals[tindex] = v
        pnode = PrimitiveNode(primitive, data_node=DATA_TERMINAL, terminals=terminals)
        if learner is None:
            learner = pnode
        if last is not None:
            last._data_node = pnode
        last = pnode
    return learner
