from collections import defaultdict
import itertools
from geosolver.text2.semantic_tree import SemanticTreeNode

__author__ = 'minjoon'


class SemanticForestNode(object):
    def __init__(self, tag_rule, unary_rules, binary_rules):
        self.tag_rule = tag_rule
        self.unary_rules = unary_rules
        self.binary_rules = binary_rules

    def is_leaf(self):
        return len(self.unary_rules) == 0 and len(self.binary_rules) == 0

    def __repr__(self):
        return "%r: %r %r" % (self.tag_rule, self.unary_rules, self.binary_rules)


class SemanticForest(object):
    def __init__(self, tag_rules, unary_rules, binary_rules):
        self.node_dict = {}
        for tag_rule in tag_rules:
            self.node_dict[tag_rule] = SemanticForestNode(tag_rule, [], [])
        for unary_rule in unary_rules:
            self.node_dict[unary_rule.parent_tag_rule].tag_rule = unary_rule.parent_tag_rule
            self.node_dict[unary_rule.parent_tag_rule].unary_rules.append(unary_rule)
        for binary_rule in binary_rules:
            self.node_dict[binary_rule.parent_tag_rule].tag_rule = binary_rule.parent_tag_rule
            self.node_dict[binary_rule.parent_tag_rule].binary_rules.append(binary_rule)

    def get_semantic_trees_by_node(self, root_node):
        """
        get all semantic trees with self as the root
        :return list:
        """
        return self._get_semantic_trees_by_node(root_node, set())

    def _get_semantic_trees_by_node(self, root_node, visited):
        tag_rule = root_node.tag_rule
        if tag_rule in visited:
            return []
        visited = visited.union([tag_rule])

        if root_node.is_leaf():
            if root_node.tag_rule.signature.valence == 0:
                return [SemanticTreeNode(root_node.tag_rule, [])]
            return []

        semantic_trees = []
        for unary_rule in root_node.unary_rules:
            child_node = self.node_dict[unary_rule.child_tag_rule]
            child_trees = self._get_semantic_trees_by_node(child_node, visited)
            for child_tree in child_trees:
                semantic_tree = SemanticTreeNode(tag_rule, [child_tree])
                semantic_trees.append(semantic_tree)

        for binary_rule in root_node.binary_rules:
            a_node = self.node_dict[binary_rule.child_a_tag_rule]
            b_node = self.node_dict[binary_rule.child_b_tag_rule]
            a_trees = self._get_semantic_trees_by_node(a_node, visited)
            b_trees = self._get_semantic_trees_by_node(b_node, visited)
            for a_tree, b_tree in itertools.product(a_trees, b_trees):
                a_tag_rules = a_tree.get_tag_rules()
                b_tag_rules = b_tree.get_tag_rules()
                if len(a_tag_rules.intersection(b_tag_rules)) == 0:
                    semantic_tree = SemanticTreeNode(tag_rule, [a_tree, b_tree])
                    semantic_trees.append(semantic_tree)

        return semantic_trees

    def get_semantic_trees_by_type(self, return_type):
        roots = [node for node in self.node_dict.values() if node.tag_rule.signature.return_type == return_type]
        semantic_trees = list(itertools.chain(*[self.get_semantic_trees_by_node(root) for root in roots]))
        return semantic_trees
