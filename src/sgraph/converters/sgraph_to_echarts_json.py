import json
from sgraph import SGraph, SElement
from typing import TypedDict, Tuple, List


class Category(TypedDict):
    name: str
    base: str


class Node(TypedDict):
    id: int
    name: str
    value: int
    category: int


class Link(TypedDict):
    source: int
    target: int


def sgraph_to_echarts_json(sg: SGraph) -> Tuple[str, str, str]:
    categories: List[Category] = [{
        "name": sg.rootNode.children[0].name,
        "base": sg.rootNode.children[0].name
    }]
    nodes: List[Node] = []
    links: List[Link] = []
    hash_to_elem_index = {}

    def create_nodes_and_links(elem: SElement):
        nodes.append({
            "id": len(nodes),
            "name": elem.name,
            "value": 1,
            "category": 0
        })

        index = len(nodes) - 1
        hash_to_elem_index[hash(elem)] = index

        if elem.parent and hash(elem.parent) in hash_to_elem_index:
            source = hash_to_elem_index[hash(elem.parent)]
            links.append({
                "source": source,
                "target": index
            })

    for child in sg.rootNode.children:
        child.traverseElements(create_nodes_and_links)

    return json.dumps(categories), json.dumps(nodes), json.dumps(links)
