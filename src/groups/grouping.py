from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set


@dataclass
class Node:
    children: set = field(default_factory=set)
    words: set = field(default_factory=set)
    parent: Optional[str] = None
    name: Optional[str] = None


def make_groups(words_list: Iterable[str], delimiter: str) -> Dict[str, Set[str]]:
    structured_data = prepare_structure(words_list=words_list, delimiter=delimiter)
    groups = process_structure(input_structure=structured_data, delimiter=delimiter, words_list=words_list)
    return groups


def prepare_structure(words_list: Iterable[str], delimiter: str) -> Dict[str, Node]:
    result: Dict[str, Node] = defaultdict(Node)
    words_set = set(words_list)
    for word in words_set:
        current_words = []
        split_word = word.split(delimiter)
        for element in split_word:
            current_words.append(element)
            previous_key = delimiter.join(current_words[:-1])
            key = delimiter.join(current_words)
            if previous_key:
                result[previous_key].children.add(key)
            current_node = result[key]
            current_node.words.add(word)
            current_node.parent = previous_key if previous_key else None
            current_node.name = key

    return result


def process_structure(
    input_structure: Dict[str, Node], words_list: Iterable[str], delimiter: str
) -> Dict[str, Set[str]]:
    roots = {word.split(delimiter)[0] for word in words_list}
    groups: Dict[str, Set[str]] = dict()
    for root in roots:
        groups = {**groups, **process_node(input_structure, input_structure[root])}

    return groups


def process_node(input_structure: Dict[str, Node], node: Node) -> Dict[str, Set[str]]:
    groups: Dict[str, Set[str]] = dict()
    children = [value for key, value in input_structure.items() if key in node.children]
    leaves = [child for child in children if len(child.words) == 1]
    nodes_for_further_processing = [child for child in children if len(child.words) > 1]

    if node.name in node.words:
        return {node.name: node.words}
    if len(leaves) == 1 and len(node.words) == 1:
        return {list(node.words)[0]: node.words}
    if len(leaves) == 1 and nodes_for_further_processing:
        groups = {
            node.name: {word for word in node.words if node.name == word}
            | {word for node in children for word in node.words}
        }
        return groups
    if len(leaves) == 1 and not nodes_for_further_processing:
        leave = leaves.pop()
        groups = {leave.name: {word for word in leave.words}}
        return groups
    if leaves:
        groups = {node.name: {word for leave in leaves for word in leave.words}}

    for node_for_further_processing in nodes_for_further_processing:
        groups = {**groups, **process_node(input_structure, node_for_further_processing)}

    return groups
