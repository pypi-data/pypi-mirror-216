import graphviz

class ZddNode:
    def __init__(self, top, left, right):
        self.top = top
        self.left = left
        self.right = right

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.top == other.top and self.left == other.left and self.right == other.right
        else:
            return False

class ZddManager:
    UNIQUE_NODES:dict[tuple[int,ZddNode,ZddNode], ZddNode] = {}
    TOP = ZddNode(1, None, None)
    BOTTOM = ZddNode(-1, None, None)


def to_zdd(set_of_sets:set[frozenset[int]]) -> ZddNode:
    """Creates an ordered zdd tree that represents the set of sets

    Args:
        set_of_sets (set[frozenset[int]]): A set of frozensets of ints that the function will make a zdd of

    Returns:
        Zdd: The ordered zdd tree that represents the set of sets
    """
    if(len(set_of_sets) == 0): return empty()
    if(len(set_of_sets) == 1 and frozenset() in set_of_sets): return base()
    universe = set().union(*set_of_sets)
    biggest_element = max(universe)

    contains_biggest_element = set()
    for s in set_of_sets:
        if biggest_element in s:
            new = set(s)
            new.remove(biggest_element)
            contains_biggest_element.add(frozenset(new))
    contains_not_biggest_element = set([s for s in set_of_sets if biggest_element not in s])

    return get_node(
        biggest_element,
        to_zdd(contains_not_biggest_element),
        to_zdd(contains_biggest_element)
    )


def to_set_of_sets(P:ZddNode) -> set[frozenset[int]]:
    """Creates a set of frozensets that P represents

    Args:
        P (Zdd): Zdd node that represents a set of sets

    Returns:
        set[frozenset[int]]: The set of frozensets that P represents
    """
    def preorder_traversal(node:ZddNode, parent:ZddNode, add:bool, current_set:set[int], set_of_sets:set[frozenset[int]]) -> None:
        if(add):
            current_set.add(parent.top)
        if(node == empty()):
            return
        if(node == base()):
            set_of_sets.add(frozenset(current_set))
            return
        preorder_traversal(node.left, node, False, current_set, set_of_sets)
        preorder_traversal(node.right, node, True, current_set, set_of_sets)
        current_set.remove(node.top)
    
    if (P == empty()): return set()
    if (P == base()): return {frozenset({})}
    set_of_sets = set()
    current_set = set()
    preorder_traversal(P.left, P, False, current_set, set_of_sets)
    preorder_traversal(P.right, P, True, current_set, set_of_sets)
    return set_of_sets


def create_image(P:ZddNode, file_name:str="ZDD") -> None:
    """Creates an .PNG image that visualizes the tree P

    Args:
        P (Zdd): Root node 
        file_name (str, optional): Name of the file the image will be stored
    """
    visited = set()
    dot = graphviz.Digraph()
    dot.node(str(id(P)), shape="circle", label=str(P.top))

    dot.node(str(id(empty())), shape="square", label='ø')
    dot.node(str(id(base())), shape="square", label='\{ø\}')

    def add_nodes_edges(node:ZddNode):
        if node.left and (id(node) not in visited):
            dot.node(str(id(node)), shape="circle", label=str(node.top))
            dot.edge(str(id(node)), str(id(node.left)), style="dashed")
            add_nodes_edges(node.left)
        if node.right and (id(node) not in visited):
            dot.node(str(id(node)), shape="circle", label=str(node.top))
            dot.edge(str(id(node)), str(id(node.right)))
            add_nodes_edges(node.right)
        visited.add(id(node))
    add_nodes_edges(P)
    dot.render(file_name, view=True, format='png')


def empty() -> ZddNode:
    """Returns the zdd node that represents the empty family ∅

    Returns:
        Zdd: ∅
    """
    return ZddManager.BOTTOM


def base() -> ZddNode:
    """Returns the zdd node that represents the unit family {∅}

    Returns:
        Zdd: {∅}
    """
    return ZddManager.TOP


def get_node(top:int, left:ZddNode, right:ZddNode) -> ZddNode:
    """Returns the node Zdd(top, left, right) if it already exists or 
        creates that node and returns it if it does not exist

    Args:
        top (int): Value of the node
        left (Zdd): Left child
        right (Zdd): Right child

    Returns:
        Zdd: Zdd(top, left, right)
    """
    if right == empty():
        return left
    if (top, id(left), id(right)) in ZddManager.UNIQUE_NODES:
        return ZddManager.UNIQUE_NODES[(top, id(left), id(right))]
    else:
        new_node = ZddNode(top, left, right)
        ZddManager.UNIQUE_NODES[(top, id(left), id(right))] = new_node
        return ZddManager.UNIQUE_NODES[(top, id(left), id(right))]


def subset1(P:ZddNode, var:int) -> ZddNode:
    """Returns the set of subsets of P containing the element var

    Args:
        P (Zdd): Set of sets of ints in the form of an zdd node
        var (int): Element that may or may not be in the sets of P

    Returns:
        Zdd: The subset of P containing the element var
    """
    if (P == empty()): return empty()
    if (P == base()):  return empty()
    if (P.top < var):  return empty(); 
    if (P.top == var): return get_node(var, empty(), P.right)
    if (P.top > var):  return get_node(P.top, subset1(P.left, var), subset1(P.right, var));  
       

def subset0(P:ZddNode, var:int) -> ZddNode:
    """Returns the set of subsets of P not containing the element var

    Args:
        P (Zdd): Set of sets of ints in the form of an zdd node
        var (int): Element that may or may not be in the sets of P

    Returns:
        Zdd: The subset of P not containing the element var
    """
    if (P == empty()): return empty()
    if (P == base()):  return base()
    if (P.top < var):  return P
    if (P.top == var): return P.left
    if (P.top > var):  return get_node(P.top, subset0(P.left, var), subset0(P.right, var))


def change(P:ZddNode, var:int) -> ZddNode:
    """Returns the set of subsets derived
        from P by adding element var to those subsets that
        did not contain it and removing element var from
        those subsets that contain it. 

    Args:
        P (Zdd): Set of sets of ints in the form of an zdd node
        var (int): Element that may or may not be in the sets of P

    Returns:
        Zdd: The set of subsets derived
            from P by adding element var to those subsets that
            did not contain it and removing element var from
            those subsets that contain it. 
    """
    if (P == empty()): return empty()
    if (P == base()):  return get_node(var, empty(), base())
    if (P.top < var):  return get_node(var, empty(), P)
    if (P.top == var): return get_node(var, P.right, P.left)
    if (P.top > var):  return get_node(P.top, change(P.left, var), change(P.right, var))


def union(P:ZddNode, Q:ZddNode) -> ZddNode:
    """Union between two Zdd nodes that each represent a set of sets

    Args:
        P (Zdd): First zdd nodes that represents a set of sets
        Q (Zdd): Second zdd nodes that represents a set of sets

    Returns:
        Zdd: P U Q
    """
    if (P == empty()):   return Q
    if (Q == empty()):   return P
    if (P == Q):         return P
    if (P == base()):    return get_node(Q.top, union(P, Q.left), Q.right)
    if (Q == base()):    return get_node(P.top, union(P.left, Q), P.right)
    if (P.top > Q.top):  return get_node(P.top, union(P.left, Q), P.right)
    if (P.top < Q.top):  return get_node(Q.top, union(P, Q.left), Q.right)
    if (P.top == Q.top): return get_node (P.top, union(P.left, Q.left), union(P.right, Q.right))


def intersection(P:ZddNode, Q:ZddNode) -> ZddNode:
    """Intersection between two Zdd nodes that each represent a set of sets

    Args:
        P (Zdd): First zdd nodes that represents a set of sets
        Q (Zdd): Second zdd nodes that represents a set of sets

    Returns:
        Zdd: P ⋂ Q
    """
    if (P == empty()):   return empty()
    if (Q == empty()):   return empty()
    if (P == Q):         return P
    if (P == base()):    return intersection(P, Q.left)
    if (Q == base()):    return intersection(P.left, Q)
    if (P.top > Q.top):  return intersection(P.left, Q)
    if (P.top < Q.top):  return intersection (P, Q.left)
    if (P.top == Q.top): return get_node(P.top, intersection(P.left, Q.left), intersection(P.right, Q.right))


def difference(P:ZddNode, Q:ZddNode) -> ZddNode:
    """Difference between the first zdd node and the second zdd node 
    Args:
        P (Zdd): First zdd nodes that represents a set of sets
        Q (Zdd): Second zdd nodes that represents a set of sets

    Returns:
        Zdd: P - Q
    """
    if (P == empty()):   return empty(); 
    if (Q == empty()):   return P
    if (P == Q):         return empty()
    if (P == base()):    return difference(P, Q.left)
    if (Q == base()):    return get_node(P.top, difference(P.left, Q), P.right)
    if (P.top > Q.top):  return get_node(P.top, difference(P.left, Q), P.right)
    if (P.top < Q.top):  return difference(P, Q.left)
    if (P.top == Q.top): return get_node(P.top, difference(P.left, Q.left), difference(P.right, Q.right))


def count(P:ZddNode) -> int:
    """Counts the number of sets in the set P

    Args:
        P (Zdd): Set of sets

    Returns:
        int: Number of sets in the set P
    """
    if (P == empty()): return 0
    if (P == base()): return 1
    return count(P.left) + count(P.right)