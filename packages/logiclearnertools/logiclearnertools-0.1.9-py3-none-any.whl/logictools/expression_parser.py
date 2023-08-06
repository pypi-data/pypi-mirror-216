import os

from logictools.AI.astar_search import astar_search
from logictools.logic_rule_transforms import *
from copy import deepcopy
from lark import Lark, Tree, Token
from lark.visitors import Visitor, Transformer, v_args
from lark.exceptions import UnexpectedInput
from logictools.validation_exception import *
from logictools.AI.astar_heuristics import GeneHeuristic


class ExpressionParser:

    def __init__(self):
        self.grammar_file = "AI/grammar.lark"
        self.parser = Lark.open(
            self.grammar_file,
            rel_to=__file__,
            parser="lalr",
            propagate_positions=True)
        self.parent = Parent()

    def parse(self, eqn):
        return self.parser.parse(eqn)


class Parent(Visitor):
    def visit(self, tree):
        for subtree in tree.children:
            if isinstance(subtree, Tree):
                assert not hasattr(subtree, "parent")
                subtree.parent = tree


class TreeToString(Transformer):
    def __init__(self):
        super().__init__()
        self.string_forms = {
            "IMPL": "->", "DBLIMPL": "<->", "NOT": "~", "AND": "^",
            "OR": "v", "LPAR": "(", "RPAR": ")", "TRUE": "T", "FALSE": "F"
        }

    def start(self, eqn):
        return eqn[0]

    def eqn(self, dbl_exprs):
        return self.string_forms["DBLIMPL"].join(dbl_exprs)

    def dbl_expr(self, exprs):
        return self.string_forms["IMPL"].join(exprs)

    def expr(self, terms):
        return self.string_forms["OR"].join(terms)

    def term(self, literals):
        return self.string_forms["AND"].join(literals)

    def literal(self, variable):
        if len(variable) == 2:
            return self.string_forms["NOT"] + variable[1]
        return variable

    def variable(self, data):
        if isinstance(data[0], str):
            return data[0]
        elif is_token(data[0], 'ID'):
            return data[0].value
        return self.string_forms[data[0].type]

    def paren_expr(self, expr):
        return self.string_forms["LPAR"] + expr[0] + self.string_forms["RPAR"]


class Frontier(Transformer):
    def __init__(self, in_str, allowed_ops=allowed_operations):
        super().__init__()
        self.in_str = in_str
        self.frontier = set()
        self.checked_tokens = set()
        self.tts = TreeToString()
        self.allowed_ops = allowed_ops

    # necessary since Lark doesn't have meta for tokens. Ugh.
    def _get_token_variants(self, token: Token):
        sp, ep = token.start_pos, token.end_pos
        transforms = set()
        for op in self.allowed_ops[token.type]:
            new_node = op(token)
            if not isinstance(new_node, list):
                new_node = [new_node]
            for n in new_node:
                new_str = n.value if isinstance(
                    n, Token) else self.tts.transform(n)
                transforms.add((new_str, get_operation_name(op)))
        variants = {(self.in_str[:sp] + t[0] +
                     self.in_str[ep:], t[1]) for t in transforms}
        return variants

    def _get_transformations(self, node: Tree) -> set:
        transforms = set()
        for op in self.allowed_ops[node.data]:
            # necessary because some transformations are in-place. Change this.
            new_node = deepcopy(node)
            new_node = op(new_node)
            if not isinstance(new_node, list):
                new_node = [new_node]
            for n in new_node:
                new_str = n.value if isinstance(
                    n, Token) else self.tts.transform(n)
                transforms.add((new_str, get_operation_name(op)))
        return transforms

    def _get_variants(self, tree_type, meta, children):
        variants = set()
        for tok in filter(lambda t: isinstance(t, Token) and (
                t.start_pos, t.end_pos) not in self.checked_tokens, children):
            variants.update(self._get_token_variants(tok))  # ugly pt.2
            self.checked_tokens.add((tok.start_pos, tok.end_pos))
        if not meta.empty:
            sp, ep = meta.start_pos, meta.end_pos
            transforms = self._get_transformations(Tree(tree_type, children))
            variants.update(
                {(self.in_str[:sp] + t[0] + self.in_str[ep:], t[1]) for t in transforms})
        self.frontier.update(variants)

    def _process_rule(self, tree_type, meta, children):
        self._get_variants(tree_type, meta, children)
        return Tree(tree_type, children)

    @v_args(meta=True)
    def start(self, meta, children):
        return self._process_rule('start', meta, children)

    @v_args(meta=True)
    def eqn(self, meta, children):
        return self._process_rule('eqn', meta, children)

    @v_args(meta=True)
    def dbl_expr(self, meta, children):
        return self._process_rule('dbl_expr', meta, children)

    @v_args(meta=True)
    def expr(self, meta, children):
        return self._process_rule('expr', meta, children)

    @v_args(meta=True)
    def term(self, meta, children):
        return self._process_rule('term', meta, children)

    @v_args(meta=True)
    def literal(self, meta, children):
        return self._process_rule('literal', meta, children)

    @v_args(meta=True)
    def variable(self, meta, children):
        return self._process_rule('variable', meta, children)

    @v_args(meta=True)
    def paren_expr(self, meta, children):
        return self._process_rule('paren_expr', meta, children)


class SimplifyParentheses(Transformer):
    def __init__(self):
        super().__init__()

    def _stringify(self, tree):
        return TreeToString().transform(tree)

    def start(self, children):
        if is_tree(children[0], "paren_expr"):
            children = children[0].children
        return self._stringify(Tree("start", children))

    def paren_expr(self, children):
        tr = Tree("paren_expr", children)
        while is_tree(tr.children[0], 'paren_expr'):
            tr = tr.children[0]
        if not isinstance(tr.children[0], Tree) or is_tree(
                tr.children[0], 'literal') or len(tr.children[0].children) == 1:
            tr = tr.children[0]
        return tr


def get_frontier(in_str: str, simplify_paren=True,
                 include_paren=False, allowed_ops=allowed_operations) -> list:
    ep, tts = ExpressionParser(), TreeToString()
    tree = ep.parse(in_str)
    linted_str = tts.transform(tree)
    fr = Frontier(linted_str, allowed_ops=allowed_ops)
    fr.transform(tree)
    frontier = fr.frontier
    if simplify_paren:
        sp = SimplifyParentheses()
        no_par_frontier = set(
            map(lambda f: (sp.transform(ep.parse(f[0])), f[1]), frontier))
        no_par_frontier = set(
            filter(
                lambda x: x[0] != sp.transform(
                    ep.parse(linted_str)),
                no_par_frontier))
        frontier = frontier | no_par_frontier if include_paren else no_par_frontier
    # tts transform so that tokens standardized
    return list(set(filter(lambda x: x[0] != linted_str, frontier)))


def validate(current_frontier: list, new_expr: str,
             new_rule: str, extra_paren_allowed=True) -> str:
    ep, tts = ExpressionParser(), TreeToString()
    try:
        new_tree = ep.parse(new_expr)
    except UnexpectedInput as e:
        raise InvalidExpressionException(InvalidStates.INPUT_SYNTAX_ERROR)
    new_rule = new_rule.casefold()
    # make str comparisons case-insensitive
    current_frontier = [(i[0], i[1].casefold()) for i in current_frontier]
    new_linted = SimplifyParentheses().transform(
        new_tree) if extra_paren_allowed else tts.transform(new_tree)
    if new_linted not in [i[0] for i in current_frontier]:
        raise InvalidExpressionException(InvalidStates.INVALID_NEW_EXPR)
    elif new_rule not in [i[1] for i in current_frontier]:
        raise InvalidExpressionException(InvalidStates.INVALID_NEW_RULE)
    elif (new_linted, new_rule) not in current_frontier:
        raise InvalidExpressionException(InvalidStates.INCORRECT_RULE_EXPR)
    return new_linted


def check_success(new_linted: str, target: str) -> bool:
    return new_linted.casefold() == target.casefold()


def validate_and_get_frontier(
        old_expr: str, new_expr: str, new_rule: str, target: str) -> dict:
    ep, tts = ExpressionParser(), TreeToString()
    response = {
        "isValid": True
    }
    old_tree = ep.parse(old_expr)
    new_linted = old_linted = tts.transform(old_tree)
    current_frontier = get_frontier(old_linted)
    try:
        new_linted = validate(current_frontier, new_expr, new_rule)
        response['isSolution'] = check_success(new_linted, target)
    except InvalidExpressionException as e:
        response = e.get_error_dict()
    response['nextFrontier'] = get_frontier(new_linted)
    return response


def get_hint(expr, target, heuristic, max_timeout=1):
    def frontier_func(x):
        fr = get_frontier(
            x[0],
            include_paren=False,
            allowed_ops=search_operations)
        return fr

    def goal_func(x, target):
        return x[0] == target[0]

    isfound, result = astar_search(
        expr, target, heuristic, frontier_func, goal_func, max_timeout=max_timeout)
    return {
        "nextStep": result[1] if len(result) > 1 else result[0],
        "solutionFound": isfound,
        "path": result
    }


def validate_and_get_hint(old_expr: str, new_expr: str,
                          new_rule: str, target: str, max_timeout: int) -> dict:
    """
    Validates an input expression and rule given the previous expression, and returns a hint for the next step
    :param old_expr: previous valid expression
    :param new_expr: user's proposed expression
    :param new_rule: user's proposed rule
    :param target: target proposition of the question
    :param max_timeout: amount of time to search for
    :return: dict containing {
        isValid: bool, whether the input expression is valid,
        isSolution: bool, whether the solution has been reached,
        errorCode: Enum, if not isValid, the exception code for the error,
        errorMsg: str, if not isValid, the exception description for the error,
        hint: dict, {
            nextStep: tuple<str, str>, the (expr, rule) hint for the next step,
            solutionFound: bool, whether the hint search actually solved the question,
            path: list<tuple>, the steps for the closest node to target found by the search (=target if solutionFound)
        }
    }
    """
    ep, tts = ExpressionParser(), TreeToString()

    response = {
        "isValid": True
    }

    old_tree = ep.parse(old_expr)
    new_linted = old_linted = tts.transform(old_tree)
    current_frontier = get_frontier(old_linted)
    try:
        new_linted = validate(current_frontier, new_expr, new_rule)
        response['isSolution'] = check_success(new_linted, target)
    except InvalidExpressionException as e:
        response = e.get_error_dict()

    target = ExpressionParser().parse(target)
    target = TreeToString().transform(target) if isinstance(
        target, Tree) else target.value

    heuristic = GeneHeuristic()
    dirname = os.path.dirname(__file__)
    heuristic.load(os.path.join(dirname, "AI/astar_heuristic_weights.txt"))
    response['hint'] = get_hint(
        new_linted,
        target,
        heuristic.gene_meta_dist,
        max_timeout=max_timeout)
    return response


if __name__ == "__main__":
    old, new, rule, goal = "~(p^q)v~q", "(~pv~q)v~q", "de morgan's law", "~pv~q"
    print(validate_and_get_hint(old, new, rule, goal, max_timeout=1))

    print("\n", get_frontier("~(~p)<->p"), "\n")
