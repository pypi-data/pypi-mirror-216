# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""Module for custom Graph."""
import logging
from typing import (
    Any,
    Dict,
)

from numpydoc.docscrape import NumpyDocString

from qctrlcommons.node.composite.namespace import NAMESPACE_ATTR
from qctrlcommons.node.composite.registry import (
    COMPOSITE_NAMESPACE_REGISTRY,
    COMPOSITE_NODE_REGISTRY,
)
from qctrlcommons.node.registry import NODE_REGISTRY

LOGGER = logging.getLogger(__name__)


class Graph:
    """
    A class for representing and building a Boulder Opal data flow graph.

    The graph object is the main entry point to the Boulder Opal graph ecosystem.
    You can call methods to add nodes to the graph, and use the `operations` attribute to get a
    dictionary representation of the graph.
    """

    def __init__(self):
        self.operations = {}
        self._add_composite_nodes()

    def __getattr__(self, attr):
        # We override getattr to stop pylint from complaining about missing attributes for methods
        # that are added dynamically.
        raise AttributeError(f"'Graph' object has no attribute '{attr}'.")

    def _add_composite_nodes(self):
        # We initialize the node namespaces to the graph in this way since they need access
        # to the initialized class object.
        for _composite_namespace in COMPOSITE_NAMESPACE_REGISTRY:
            _namespace = getattr(_composite_namespace, NAMESPACE_ATTR)
            setattr(self, _namespace, _composite_namespace(self))
            LOGGER.debug("adding attr %s to namespace: %s", _namespace, self)

    @classmethod
    def _from_operations(cls, operations: Dict[str, Any]):
        """
        Create a new graph from an existing set of operations.

        Parameters
        ----------
        operations : dict[str, Any]
            The initial dictionary of operations for the graph.
        """
        graph = cls()
        graph.operations = operations
        return graph


def _extend_method(obj, method, method_name):
    """
    Extends the specified object by adding methods as attributes.

    Parameters
    ----------
    obj : Any
        The object to which the node should be added.
    method : Any
        Method to be added to the object.
    method_name : str
        Name of the method to be added.
    """
    if hasattr(obj, method_name):
        raise AttributeError(f"existing attr {method_name} on namespace: {obj}")
    LOGGER.debug("adding attr %s to namespace: %s", method_name, obj)
    setattr(obj, method_name, method)


def _clean_doc(doc: str) -> str:
    """
    Remove the graph parameter from the doc.
    """
    doc_obj = NumpyDocString(doc)

    doc_obj["Parameters"] = [
        item for item in doc_obj["Parameters"] if item.name != "graph"
    ]

    return str(doc_obj)


# Set nodes to Graph.
for node_cls in NODE_REGISTRY.as_list():
    node = node_cls.create_graph_method()
    _extend_method(Graph, node, node.__name__)

# Set composite nodes to Graph.
for composite_node in COMPOSITE_NODE_REGISTRY:
    composite_node.__doc__ = _clean_doc(composite_node.__doc__)
    _extend_method(Graph, composite_node, composite_node.__name__)
