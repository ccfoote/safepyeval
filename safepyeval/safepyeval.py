import ast


_not_specified = object()


class _SafePyEvalContext:
    def __init__(self, variables: dict):
        self._variables = {**variables}
        self._return_value = _not_specified


def evaluate(code, globals={"userId": "magland"}):
    context = _SafePyEvalContext(globals)
    tree = ast.parse(code)
    _eval_node(tree, context)
    if context._return_value is _not_specified:
        raise Exception("No return value specified")
    return context._return_value


def _eval_node(node, context: _SafePyEvalContext):
    if isinstance(node, ast.Module):
        return _eval_node(node.body, context)
    elif isinstance(node, list):
        for n in node:
            if context._return_value is not _not_specified:
                return
            _eval_node(n, context)
    elif isinstance(node, ast.Assign):
        if len(node.targets) != 1:
            raise Exception("Unexpected number of targets in assignment")
        if not isinstance(node.targets[0], ast.Name):
            raise Exception("Unexpected target type in assignment")
        name = node.targets[0].id
        value = _eval_node(node.value, context)
        context._variables[name] = value
    elif isinstance(node, ast.If):
        if _eval_node(node.test, context):
            _eval_node(node.body, context)
        else:
            _eval_node(node.orelse, context)
    elif isinstance(node, ast.Compare):
        if len(node.ops) != 1:
            raise Exception("Unexpected number of ops in compare")
        if isinstance(node.ops[0], ast.In) or isinstance(node.ops[0], ast.NotIn):
            left = _eval_node(node.left, context)
            if len(node.comparators) != 1:
                raise Exception("Unexpected number of comparators in compare")
            right = _eval_node(node.comparators[0], context)
            if isinstance(node.ops[0], ast.In):
                return left in right
            elif isinstance(node.ops[0], ast.NotIn):
                return left not in right
        elif isinstance(node.ops[0], (ast.LtE, ast.Lt, ast.GtE, ast.Gt, ast.Eq, ast.NotEq)):
            left = _eval_node(node.left, context)
            if len(node.comparators) != 1:
                raise Exception("Unexpected number of comparators in compare")
            right = _eval_node(node.comparators[0], context)
            if isinstance(node.ops[0], ast.LtE):
                return left <= right
            elif isinstance(node.ops[0], ast.Lt):
                return left < right
            elif isinstance(node.ops[0], ast.GtE):
                return left >= right
            elif isinstance(node.ops[0], ast.Gt):
                return left > right
            elif isinstance(node.ops[0], ast.Eq):
                return left == right
            elif isinstance(node.ops[0], ast.NotEq):
                return left != right
            else:
                raise Exception("Unexpected op in compare")
        else:
            raise Exception(f"Unexpected op in compare: {node.ops[0]}")
    elif isinstance(node, ast.BoolOp):
        if len(node.values) != 2:
            raise Exception("Unexpected number of values in boolop")
        v1 = _eval_node(node.values[0], context)
        v2 = _eval_node(node.values[1], context)
        if isinstance(node.op, ast.Or):
            return v1 or v2
        elif isinstance(node.op, ast.And):
            return v1 and v2
        else:
            raise Exception("Unexpected op in boolop")
    elif isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.Not):
            return not _eval_node(node.operand, context)
        else:
            raise Exception(f"Unexpected op in unaryop: {node.op}")
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left, context)
        right = _eval_node(node.right, context)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right
        else:
            raise Exception(f"Unexpected op in binop: {node.op}")
    elif isinstance(node, ast.Return):
        context._return_value = _eval_node(node.value, context)
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Name):
        if node.id in context._variables:
            return context._variables[node.id]
        else:
            raise Exception("Unexpected name: {}".format(node.id))
    elif isinstance(node, ast.List):
        return [_eval_node(n, context) for n in node.elts]
    elif isinstance(node, ast.Dict):
        ret = {}
        for i in range(len(node.keys)):
            key = _eval_node(node.keys[i], context)
            value = _eval_node(node.values[i], context)
            ret[key] = value
        return ret
    elif isinstance(node, ast.Subscript):
        slice = _eval_node(node.slice, context)
        value = _eval_node(node.value, context)
        return value[slice]
    else:
        raise Exception("Unexpected node type: {}".format(type(node)))
