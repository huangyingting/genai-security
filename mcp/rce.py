# Proof of concept for MCP RCE
# uv run fastmcp run rce.py --transport sse --port 8000

from fastmcp import FastMCP
import math
import ast
import operator

mcp = FastMCP("MCP RCE server 🚀")

# Even with the restricted environment attempt ({"__builtins__": None}),
# it's still susceptible to remote code execution (RCE) attacks.


@mcp.tool()
def calculate(expression: str) -> float:
  """
  Evaluates a mathematical expression using functions from the math module.
  """
  try:
    # Add the math module functions to the local namespace
    allowed_names = {k: v for k, v in math.__dict__.items()
                     if not k.startswith("__")}
    result = eval(expression, {"__builtins__": None}, allowed_names)
    return result
  except Exception as e:
    return math.nan


# @mcp.tool()
# def safe_calculate(expression: str) -> float:
#   """
#   Safely evaluates a mathematical expression using functions from the math module.
#   """
#   # Define allowed operators
#   operators = {
#       ast.Add: operator.add,
#       ast.Sub: operator.sub,
#       ast.Mult: operator.mul,
#       ast.Div: operator.truediv,
#       ast.Pow: operator.pow,
#       ast.USub: operator.neg
#   }

#   # Define allowed functions from math
#   math_functions = {}
#   for name in dir(math):
#     if not name.startswith('__'):
#       math_functions[name] = getattr(math, name)

#   def eval_node(node):
#     # Number constant
#     if isinstance(node, ast.Constant):
#       return node.value

#     # Variable/function name
#     elif isinstance(node, ast.Name):
#       if node.id in math_functions:
#         return math_functions[node.id]
#       raise ValueError(f"Unknown variable: {node.id}")

#     # Binary operations (like x+y)
#     elif isinstance(node, ast.BinOp):
#       if type(node.op) not in operators:
#         raise ValueError(f"Unsupported operation")
#       return operators[type(node.op)](eval_node(node.left), eval_node(node.right))

#     # Unary operations (like -x)
#     elif isinstance(node, ast.UnaryOp):
#       if type(node.op) not in operators:
#         raise ValueError(f"Unsupported unary operation")
#       return operators[type(node.op)](eval_node(node.operand))

#     # Function calls (like sin(x))
#     elif isinstance(node, ast.Call):
#       if not isinstance(node.func, ast.Name):
#         raise ValueError("Complex function calls not supported")

#       func_name = node.func.id
#       if func_name not in math_functions:
#         raise ValueError(f"Unknown function: {func_name}")

#       args = [eval_node(arg) for arg in node.args]
#       return math_functions[func_name](*args)

#     else:
#       raise ValueError(f"Unsupported expression type: {type(node).__name__}")

#   try:
#     # Parse the expression into an AST
#     tree = ast.parse(expression, mode='eval')
#     # Evaluate the AST safely
#     return eval_node(tree.body)
#   except Exception as e:
#     return str(e)

if __name__ == "__main__":
  mcp.run()
