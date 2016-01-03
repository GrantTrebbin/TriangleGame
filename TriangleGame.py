#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Analyse a structured network to find all triangular regions.

A network is defined by supplying vertices of region in a clockwise or
anticlockwise manner.  All multi edge straight lines are also defined as
a further constraint on the network

"""

from collections import deque


class Edge(frozenset):
    """An edge defined by two vertices.

    The connection between 2 vertices in a graph/network define an edge.
    frozenset is subclassed and the way it is initialised is changed.
    This enables the following simple syntax to create an Edge

    Example:

    Edge(1, 2)
    Edge("alpha", "beta")

    """

    def __new__(cls, vertex_a, vertex_b):
        """Create Edge instance.

        Args:
            vertex_a: vertex id
            vertex_b: vertex id

        Returns: an instance of Edge

        """
        return super(Edge, cls).__new__(cls, {vertex_a, vertex_b})

    def __init__(self, vertex_a, vertex_b):
        """Initialize Edge.

        Args:
            vertex_a: vertex id
            vertex_b: vertex id

        """
        super(Edge, self).__init__()

    def __str__(self):
        """Human readable representation of an Edge object.

        Returns: string

        """
        return_str = ''.join([("*" + str(x) + "* ") for x in self])
        return ''.join(["|", return_str[:-1], "|"])


# class Edge:
#     """An edge defined by two vertices.
#
#     The connection between 2 vertices in a graph/network define an edge.
#
#     """
#
#     def __init__(self, vertex_a, vertex_b):
#         """Initialize an Edge.
#
#         Args:
#             vertex_a: An identifier of a vertex
#             vertex_b: An identifier of a Vertex
#
#         """
#         self.__vertices = frozenset([vertex_a, vertex_b])
#
#     def __str__(self):
#         """Human readable representation of an Edge.
#
#         Returns: string
#
#         """
#         return_str = ''.join([("*" + str(x) + "* ") for x in self.__vertices])
#         return ''.join(["|", return_str[:-1], "|"])
#
#     @property
#     def vertices(self):
#         """The vertices in an Edge.
#
#         Returns a frozenset containing the identifiers of vertices
#         in a Edge
#
#         Returns: frozenset
#
#         """
#         return self.__vertices
#
#     def __eq__(self, other):
#         """Equality comparison for Edge.
#
#         Compare two edges for equality by the vertices they contain.
#
#         For example:
#
#         |*9* *6*| is equal to |*6* *9*|
#
#         Args:
#             other: Edge
#
#         Returns: bool
#
#         """
#         return self.__vertices == other.__vertices
#
#     def __hash__(self):
#         """Hash function of an Edge.
#
#         Returns: int
#
#         """
#         return hash(self.__vertices)


def remove_folds(vertices):
    """Remove folds from a deque of vertices.

    When a deque of vertex ids is provided, edges that backtrack on
    themselves are removed.

    For Example:

    In a region defined by the vertices [2, 3, 4, 5, 6, 10, 6, 7]
    the vertices [6, 10, 6] represent a folded edge.  The edge goes from
    vertex 6 to vertex 10 and then back to vertex 6.  Replacing [6, 10, 6]
    with [6] will fix this.  The result will be [2, 3, 4, 5, 6, 7].  After
    finding a fold the vertices need to be checked again as the fold may
    be more than one edge long.

    Args:
        vertices: deque of vertex ids

    """
    vertex_count = len(vertices)

    # Rotate the vertex deque looking for equal vertex ids at position 0 and 2.
    # This indicates a fold.  The deque needs to be rotated the correct
    # number of times to check for folds at each location of the vertex list.
    for i in range(0, vertex_count):
        if vertices[0] == vertices[2]:

            # Pop the first two elements to remove the fold.
            vertices.popleft()
            vertices.popleft()

            # The vertices need to be checked for more folds
            remove_folds(vertices)
            return
        vertices.rotate(-1)


class Region:
    """A Region with an id and value defined by a list of vertices.

    A region identified by a unique id is defined by a list of vertices.
    The region also has a value. This value is analogous to an area of a
    region.

    """

    def __init__(self, region_id, region_value, region_vertices):
        """Initialize a Region.

        Initialize a Region with an id set, a value, and an list of vertices
        defining the region.  The list of vertices must be defined in a
        consistent clockwise or anti-clockwise manner between regions.


        Example:

        The region below would be defined as Region({3}, 20, [1, 2, 4, 5, 6, 3])

        region_id = 3, region_value = 20

        1----2
        |    |
        |    4------5
        |           |
        3-----------6


        Args:
            region_id: set
            region_value: number
            region_vertices: list

        Returns:

        """
        self.__id = frozenset(region_id)
        self.__value = region_value
        self.__vertices = deque(region_vertices)
        self.__vertex_count = len(self.__vertices)
        self.__edges = []
        self.generate_edge_list()

    def __str__(self):
        """Human readable representation of a Region.

        A region is surrounded by parenthesis.  It contains an id in the form
        of a set surrounded by braces, a value surrounded by equal signs,
        and a list of vertices, each one surrounded by asterisks

        Example:

        Printing Region({3}, 20, [1, 2, 4, 5, 6, 3]) would display
        ({3} =20= *1* *2* *4* *5* *6* *3*)

        Returns: string

        """
        vertex_string = ''.join([(" *" + str(x) + "*")
                                 for x in self.__vertices])

        return "(" + str(set(self.__id)) + " =" + str(self.__value) + "=" +\
            vertex_string + ")"

    def add_edge(self, e):
        """Add an Edge to a Region.

        Args:
            e: Edge

        """
        self.__edges.append(e)

    def generate_edge_list(self):
        """Add edges to a Region based on the list of vertices.

        Take the list of vertices defining a region and add each edge that's
        defined by neighbouring vertices to the Region.

        """
        # if the region is null and has no vertices it can't have any edges
        if self.vertex_count == 0:
            return

        # add the edge connecting the first and last vertices of the region
        vertex_a = self.vertices[self.vertex_count-1]
        vertex_b = self.vertices[0]
        self.add_edge(Edge(vertex_a, vertex_b))

        # add all the other edges of the region to the list
        for vertex in range(1, self.vertex_count):
            vertex_a = self.vertices[vertex-1]
            vertex_b = self.vertices[vertex]
            self.add_edge(Edge(vertex_a, vertex_b))

    def rotate_vertices(self, edge):
        """Rotate a vertex list of a region until a specific edge is at the end.

        For Example:

        If a region contains a vertex list equal to [1, 2, 4, 5, 6, 3]
        and Edge(5, 4) is passed as the argument the vertex list will become
        [6, 3, 1, 2, 4, 5]

        Args:
            edge: Edge

        """
        # Rotate the vertex list until the connecting vertices are at the start
        while Edge(self.vertices[0], self.vertices[1]) != edge:
            self.vertices.rotate(-1)

        # Rotate the vertex list 2 more times so that the connecting vertices
        # are at the end
        self.vertices.rotate(-2)

    def __add__(self, other):
        """The addition operation for Region objects.

        The id of a the new Region will be the ids of Region objects that
        comprise it in a combined set.  The new value will be the addition of
        the values of the Region objects that it's made of.  The vertex list
        will be a merging of the boundaries of the Region objects it's made of.
        Vertex lists need to be in a consistent clockwise or anti-clockwise
        order.  The starting vertex doesn't matter.

        If regions can't be added because they aren't touching, an empty region
        is returned.  This also implies that Region addition is not commutative.
        Imagine three consecutive regions A,B,C.  (A + B) + C will return a
        valid result while (A + C) + B will return an empty region as A and C
        are not connected.

        There is no guarantee that adding two regions with two separate shared
        edges will yield the same result on different hardware.

        For Example:

        1---------------2
        |               |
        |        9      |
        |      / |      |
        3-----7--8------4
        |               |
        5---------------6

        Adding the Region with a vertex list [1, 2, 4, 8, 9, 7, 3] to the
        Region with a vertex list [3, 7, 8, 4, 6, 5] could give two different
        results depending on if the shared edge of 3-7 or 8-4 is used to join
        the regions.  This would give results of

        [9, 7, 3, 1, 2, 4, 6, 5, 3, 7, 8] if joined on edge 8-4
        [9, 7, 8, 4, 6, 5, 3, 1, 2, 4, 8] if joined on edge 3-7

        They are the same Region, but because internal cut outs aren't defined,
        a "slice" at either 8-4 or 37 needs to be made to reach the internal
        section

        Using the example above,  merging of vertex list is done as follows.

        1. Rotate the lists so the edge 8-4 is at the end
        2. Remove the end vertex from each list.
        3. Join them

           [1, 2, 4, 8, 9, 7, 3] and [3, 7, 8, 4, 6, 5] along the edge 3-7
        1. [9, 7, 3, 1, 2, 4, 8]     [6, 5, 3, 7, 8, 4]
        2. [9, 7, 3, 1, 2, 4]        [6, 5, 3, 7, 8]
        3. [9, 7, 3, 1, 2, 4, 6, 5, 3, 7, 8]

        Args:
            other: Region

        Returns: Region

        """
        region_a = self
        region_b = other

        region_a_edges = set(region_a.edges)
        region_b_edges = set(region_b.edges)

        shared_edges = list(region_a_edges.intersection(region_b_edges))
        number_of_shared_edges = len(shared_edges)

        # If the regions don't share and edge, they
        # can't be added. Return a null region.
        if number_of_shared_edges == 0:
            return Region(set(), None, [])

        if region_a.id.intersection(region_b.id):
            return Region(set(), None, [])

        # Get an Edge that connects region_a to region_b
        shared_edge = shared_edges[0]

        # Rotate the vertex list until the vertices of the shared edge
        # are at the end of each Region vertex list
        region_a.rotate_vertices(shared_edge)
        region_b.rotate_vertices(shared_edge)

        # Create a new list from each Region's vertex list and remove
        # the last element
        vertex_list_a = deque()
        vertex_list_a.extend(region_a.vertices)
        vertex_list_a.pop()

        vertex_list_b = deque()
        vertex_list_b.extend(region_b.vertices)
        vertex_list_b.pop()

        # Join the 2 new lists
        new_vertex_list = deque()
        new_vertex_list.extend(vertex_list_a)
        new_vertex_list.extend(vertex_list_b)

        # After the join, the edges defining a Region can double back on
        # themselves.  These need to be removed.
        remove_folds(new_vertex_list)

        # Name of new Region
        new_name = region_a.id.union(region_b.id)

        # Value of new Region
        new_value = region_a.value + region_b.value

        return Region(set(new_name), new_value, new_vertex_list)

    def __eq__(self, other):
        """Define Region equality.

        Regions are equal if their region ids are the same.  This means they
        are composed of the same base regions.

        Args:
            other: Region

        Returns: bool

        """
        return self.__id == other.__id

    def __hash__(self):
        """Define the hash of a Region.

        The ids of regions are used for hashes

        Returns: int

        """
        return hash(self.__id)

    @property
    def edges(self):
        """Return a list of edges a Region is composed of.

        Returns: list

        """
        return self.__edges

    @property
    def id(self):
        """Return the ID of a Region.

        Returns: Region id

        """
        return self.__id

    @property
    def value(self):
        """Return the value of a Region.

        Returns: number

        """
        return self.__value

    @property
    def vertices(self):
        """Return the ordered vertices of a Region.

        Returns: deque

        """
        return self.__vertices

    @property
    def vertex_count(self):
        """Return the number of vertices that define a Region.

        Returns: integer

        """
        return self.__vertex_count


class StraightLineSegment:
    """Vertices that in a geometric sense form straight lines."""

    def __init__(self, line_vertices):
        """Create a StraightLineSegment by supplying a set of vertices.

        Args:
            line_vertices: set

        """
        self.__vertices = line_vertices

    def __str__(self):
        """Return a human readable version of a StraightLineSegment.

        Returns: string

        """
        return_str = ''.join([("*" + str(x) + "* ") for x in self.__vertices])
        return ''.join(['-', return_str[:-1], '-'])

    @property
    def vertices(self):
        """Return a set of vertices comprising a StraightLineSegment.

        Returns: set

        """
        return self.__vertices


class StructuredNetwork:
    """A planar network with some geometric constraints.

    A planar network with the geometric constraint that some of the edges are
    collinear.  The planar network is defined by defining the all the regions
    it contains in the form of a list of vertices.  All collinear edges are
    also supplied.

    After initialization, all the possible compound regions are found.
    Of these, the ones that are triangular are identified.  The value property
    of all of these are added together.

    """

    def __init__(self, network_regions, network_straight_lines):
        """Initialize a StructuredNetwork with Regions & StraightLinesSegments.

        The network to be defined is supplied by dividing it into the smallest
        regions possible.  Each region is defined as a clockwise or counter
        clockwise (it doesn't matter, just be consistent) list of vertices.
        Some geometric structure of the network needs to be supplied as well.
        This is done by supplying straight edges that contain 3 or more
        vertices.

        Args:
            network_regions: A set of Region objects
            network_straight_lines: A set of StraightLineSegment objects

        """
        self.__regions = network_regions
        self.__region_count = len(self.__regions)

        self.__straight_lines = network_straight_lines
        self.__straight_line_count = len(self.__straight_lines)

        # construct a dictionary of edges by iterating through each region
        # while also adding connected regions to each edge
        self.__edge_dict = dict()
        for region in self.__regions:
            for edge in region.edges:
                if edge in self.__edge_dict:
                    self.__edge_dict[edge].add(region)
                else:
                    self.__edge_dict[edge] = {region}

        self.__edge_count = len(self.__edge_dict)

        # Create a list of sets. In increasing order the list will contain a set
        # of compound regions with an increasing number of base regions.
        # The first list entry will contain a set of the base regions.
        # The second one will contain a set of all possible compound regions
        # made up of two base regions. This pattern will continue until a
        # compound region containing all base regions is created

        compound_region_list = [self.__regions]
        while len(compound_region_list[-1]) != 0:
            self.expand_regions(compound_region_list)

        self.__compound_regions = set.union(*compound_region_list)
        self.__compound_regions_count = len(self.__compound_regions)

        # Check each compound region to see if it is triangular.
        self.__triangular_regions = set()
        for region in self.__compound_regions:
            vertex_list = deque()
            vertex_list.extend(region.vertices)
            is_triangle = self.are_vertices_triangular(vertex_list)
            if is_triangle:
                self.__triangular_regions.add(region)

        # Add the values of all triangular Region objects
        triangle_values = [region.value for region in self.__triangular_regions]
        self.__sum_of_triangles = sum(triangle_values)
        self.__triangular_region_count = len(self.__triangular_regions)

    def are_vertices_triangular(self, vertices):
        """Recursively check a deque of vertices to see if they form a triangle.

        3 elements of the vertex list are checked at a time to see if they
        form a straight line. If so the middle vertex is removed.  This is
        repeated until all redundant vertices are removed.  If the region can be
        defined by 3 vertices it is triangular.

        Args:
            vertices: deque

        Returns: bool

        """
        # test each consecutive group of 3 vertices
        for i in range(0, len(vertices)):
            triad = {vertices[0], vertices[1], vertices[2]}

            # is that triad defined in any of the StraightLineSegments?
            straight_segments = [triad.issubset(x.vertices)
                                 for x in self.__straight_lines]

            # if it is remove the redundant vertex and check the new vertex list
            if any(straight_segments):
                vertices.rotate(-1)
                vertices.popleft()
                self.are_vertices_triangular(vertices)
                break
            vertices.rotate(-1)

        # If a region can be described by 3 vertices it is a triangle.
        return len(vertices) == 3

    def expand_regions(self, regions_by_order):
        """Expand compound Regions.

        When passed a list of sets of Regions, each Region in the last set of
        the list will be expanded.  This means that separately, and one at a
        time, each edge of a compound Region will have any connected regions
        added to it.  All of the new regions are added to a set which is
        appended to the original list.  Adding a base region to a compound
        region that already contains it will create a null region.
        All of these are removed.

        Args:
            regions_by_order: list of sets of regions

        Returns:

        """
        region_set = set()

        # iterate over each region in the last set
        for region_a in regions_by_order[-1]:
            # iterate over each edge in the region
            for edge in region_a.edges:
                # iterate over each region that is connected to that edge
                for region_b in self.__edge_dict[edge]:
                    # add the compound region to the new connected region
                    # add this to the new set
                    region_set.add(region_a + region_b)

        # remove null regions
        region_set.remove(Region(set(), None, []))

        # add the set to the list
        regions_by_order.append(region_set)

    def __str__(self):
        """A human readable string containing all information about the network.

        Returns a string containing all the base regions, edges,
        multi edge straight lines, all compound regions, all triangular regions,
        and the sum of the values in all triangular regions.

        Returns: string

        """
        # a string containing all the region in the network
        region_string = ''.join([(str(x) + "\n") for x in self.__regions])

        # a string containing all the straight lines in the network
        straight_line_string = ''.join([(str(x) + "\n")
                                        for x in self.__straight_lines])

        # a string describing all the edges and their connections in a network
        edge_string =\
            ''.join([(str(edge) + " -> " +
                    ''.join(str(set(region.id))
                            for region in connected_region) + '\n')
                     for edge, connected_region in self.__edge_dict.items()])

        compound_region_string = ''.join([(str(x) + "\n")
                                          for x in self.__compound_regions])

        triangle_region_string = ''.join([(str(x) + "\n")
                                          for x in self.__triangular_regions])

        # a string describing the network
        return_string = ''.join(["Base regions ({id} =value= *vertices*)\n",
                                 "count = ", str(self.__region_count), "\n\n",
                                 region_string,
                                 "\n\nMulti edge straight lines -*vertices*-\n",
                                 "count = ", str(self.__straight_line_count),
                                 "\n\n", straight_line_string,
                                 "\n\nedge list |*vertices*| ->",
                                 " {connected region id}\ncount = ",
                                 str(self.__edge_count), "\n\n",
                                 edge_string, "\n\nCompound regions ",
                                 "({id} =value= *vertices*)\ncount = ",
                                 str(self.__compound_regions_count), "\n\n",
                                 compound_region_string, "\n\nTriangular",
                                 " Regions ({id} =value= *vertices*)\ncount = ",
                                 str(self.__triangular_region_count), "\n\n",
                                 triangle_region_string, "\n\nSum of all the ",
                                 "numbers in each triangular region = ",
                                 str(self.__sum_of_triangles)])

        return return_string

regions = {Region({1},  8, [2,  3,  9]),
           Region({2},  3, [9,  3,  4]),
           Region({3},  5, [1,  2,  8]),
           Region({4},  2, [2,  9, 10, 8]),
           Region({5},  4, [9,  4, 10]),
           Region({6},  8, [1,  8,  7]),
           Region({7}, 10, [8, 10,  6, 7]),
           Region({8},  1, [6, 10,  4]),
           Region({9},  9, [6,  4,  5])}

straight_lines = [StraightLineSegment({1, 2, 3}),
                  StraightLineSegment({1, 8, 10, 4}),
                  StraightLineSegment({1, 7, 6, 5}),
                  StraightLineSegment({2, 8, 7}),
                  StraightLineSegment({3, 9, 10, 6}),
                  StraightLineSegment({2, 9, 4}),
                  StraightLineSegment({3, 4, 5})]

triangle_game_test = StructuredNetwork(regions, straight_lines)
print(triangle_game_test)


# <editor-fold desc="test_code">
# reg1 = Region({1},  17, [1,  2,  6, 7, 4, 5])
# reg1.add_edge(Edge(2, 6))
# reg1.add_edge(Edge(6, 7))
# reg1.add_edge(Edge(7, 4))
# reg1.add_edge(Edge(4, 5))
# reg1.add_edge(Edge(5, 1))
# reg1.add_edge(Edge(1, 2))
#
#
# reg2 = Region({2},  40, [2,  3,  4, 7, 6])
# reg2.add_edge(Edge(2, 3))
# reg2.add_edge(Edge(3, 4))
# reg2.add_edge(Edge(4, 7))
# reg2.add_edge(Edge(7, 6))
# reg2.add_edge(Edge(6, 2))
#
#
# print("----------")
# print(reg1)
# print(reg2)
# region_test1 = reg1 + reg2
# print(region_test1)
# print("----------")
#
# reg3 = regions[0]
# reg4 = regions[1]
# reg5 = regions[3]
#
# print(reg3)
# print(reg4)
# region_test2 = reg3 + reg4
# print(region_test2)
# print("----------")
# region_test3 = (((((region_test2 + regions[3]) + regions[2]) + regions[5]) + regions[6]) + regions[7])
# print(region_test3)
# print("**********")
# region_test4 = (region_test3 + regions[4])+regions[8]
# print(region_test4)
#
# print((reg3 + reg4) + reg5)
#
# print(Region({2},  40, [2,  3,  4, 7, 6]) == Region({2},  42, [2,  3,  4, 7, 6]))
# </editor-fold>
