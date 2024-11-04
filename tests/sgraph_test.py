import copy
import os

from sgraph.loader import ModelLoader

MODELFILE = 'modelfile.xml'

# Helper for creating the model
def get_model(file_name):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file_name)
    modelLoader = ModelLoader()
    model = modelLoader.load_model(filename)
    return model

def test_deepcopy():
    graph1 = get_model(MODELFILE)
    graph2 = copy.deepcopy(graph1)
    assert graph1.rootNode.getNodeCount() == graph2.rootNode.getNodeCount()
    elem_names_1 = list([x.name for x in graph1.rootNode.children[0].children])
    elem_names_2 = list([x.name for x in graph2.rootNode.children[0].children])
    assert elem_names_1 == elem_names_2
    assert graph1.rootNode.getEACount() == graph2.rootNode.getEACount()
    assert graph1.produce_deps_tuples() == graph2.produce_deps_tuples()
    assert graph1.calculate_model_stats() == graph2.calculate_model_stats()


def test_calculate_model_stats():
    graph = get_model(MODELFILE)
    dependenciesCount, nodesCount, depTypeCounts, depToElemRatio = graph.calculate_model_stats()
    assert dependenciesCount == 6
    assert depToElemRatio == 21
    assert depTypeCounts == {'inc': 6}
    assert nodesCount == 29
