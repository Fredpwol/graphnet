"""
Graphnet
=====
A lightweight library for working and visualizing graphs and network
it also comes with some usefull graph algorithm.
"""

from __future__ import absolute_import
import os

VECTOR = "vector"
SCALAR = "scalar"

from .components import Node, Edge
from .graph import Graph, GraphPriorityQueue

__author__ = "Fredrick Pwol"
__version__ = "0.1.2"
__all__ = ["Graph", "GraphPriorityQueue"]
