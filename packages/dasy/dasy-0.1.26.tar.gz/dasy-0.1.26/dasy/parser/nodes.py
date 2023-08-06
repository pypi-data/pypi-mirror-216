from vyper.ast import nodes as vy_nodes
from vyper.ast.nodes import (
    Break,
    Pass,
    Continue,
    Log,
    Raise,
    Return,
    AugAssign,
    Assert,
    Index,
)
from hy import models
from dasy import parser
from .utils import process_body, build_node, set_parent_children


def parse_for(expr):
    # (for [x xs] (.append self/nums x))
    # (for [target iter] *body)
    target, iter_ = expr[1]
    target_node = parser.parse_node(target)
    iter_node = parser.parse_node(iter_)
    body_nodes = [parser.parse_node(b) for b in expr[2:]]
    body = process_body(body_nodes)
    for_node = build_node(vy_nodes.For, body=body, iter=iter_node, target=target_node)
    set_parent_children(for_node, body + [target_node, iter_node])
    return for_node


def parse_if(expr):
    # used for base case in cond expansion
    if expr[1] == models.Keyword("else"):
        if expr[3] == models.Symbol("None"):
            return parser.parse_node(expr[2])

    # we need to determine if this is an if expression or if statement
    # if expressionsn always have 4 elements, if statements may have 3
    # if expressions always have a single element in the body and else
    # if statements have 1 or more elements in the body and else
    #
    # so our criteria can be something like:
    # - if len(expr) == 4 and len(expr[2]) == 1 and len(expr[3]) == 1 and
    # both body and else are instances of vy_nodes.ExprNode

    body_nodes = [parser.parse_node(expr[2])]
    body = process_body(body_nodes)
    else_nodes = [parser.parse_node(expr[3])] if len(expr) == 4 else []
    else_ = process_body(else_nodes)
    test = parser.parse_node(expr[1])

    if (
        len(body) == 1
        and len(else_) == 1
        and isinstance(body[0], vy_nodes.ExprNode)
        and isinstance(else_[0], vy_nodes.ExprNode)
    ):
        body = body[0]
        else_ = else_[0]
        if_node = build_node(vy_nodes.IfExp, test=test, body=body, orelse=else_)
        set_parent_children(if_node, [body, else_, test])
    else:
        if_node = build_node(vy_nodes.If, test=test, body=body, orelse=else_)
        set_parent_children(if_node, body + else_ + [test])
    return if_node


def parse_assign(expr):
    # needs some slight massaging due to the way targets/target is treated
    # the Assign class has a target slot, but it uses the first value in the
    # targets arg to fill it instead of using the target kwarg
    args = [parser.parse_node(arg) for arg in expr[1:]]
    return build_node(vy_nodes.Assign, *args, targets=[args[0]])


def parse_expr(expr, nodes):
    return [parser.parse_node(node) for node in expr[1 : nodes + 1]]


def build_and_parent(node_type, body_nodes, else_nodes, test):
    node = build_node(node_type, test=test, body=body_nodes, orelse=else_nodes)
    set_parent_children(node, body_nodes + else_nodes + [test])
    return node


handlers = {
    node_type.__name__.lower(): lambda expr, node_type=node_type: build_node(
        node_type, *parse_expr(expr, 2)
    )
    for node_type in [
        Break,
        Pass,
        Continue,
        Log,
        Raise,
        Return,
        AugAssign,
        Assert,
        Index,
    ]
}
