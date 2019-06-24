__author__ = "jlarsen-usgs"
"""
Shunting Yard algorithm to parse expressions into reverse
polish notation for mathematics for use with MODFLOW MULT
file.
"""
import numpy as np


class ExpressionParser(object):
    """
    ExpressionParser uses the shunting yard algorithm
    to parse a standard mathematical expression into a
    reverse polish expression. We then use the basic
    reverse polish solver relationship to calculate
    a result.

    Parameters:
        s: (string) expression string
    """

    precedence = {'(': 1,
                  '+': 2,
                  '-': 2,
                  '/': 3,
                  '*': 3,
                  '^': 4,
                  'ABS': 5,
                  'EXP': 5,
                  'LOG': 5,
                  'L10': 5,
                  'NEG': 5,
                  'SQRT': 5}

    def __init__(self, s, arrays={}):

        self.oringinal_sting = s
        self.result = None
        self.parsed_string = []
        self.reverse_polish_notation = []
        self.arrays = arrays

        self.__parse_string(s)
        self.__shunting_yard_algorithm()
        self.__evaluate_reverse_polish_expression()

    def __parse_string(self, s):
        """
        Parse the expression string into a list object

        Parameters:
            s: (string) expression string
        """
        parsed = []
        obj = ""
        for c in s:
            if c in ("(", ")"):
                if obj:
                    parsed.append(obj)
                    obj = ""
                parsed.append(c)

            elif c == " ":
                if obj:
                    parsed.append(obj)
                    obj = ""

            elif c in ('*', '/', '+', '-', '^'):
                if obj:
                    parsed.append(obj)
                    obj = ""
                parsed.append(c)

            else:
                obj += c

        if obj:
            parsed.append(obj)

        self.parsed_string = parsed

    def __shunting_yard_algorithm(self):
        """
        Perform the shunting yard algorithm format the
        parsed expression into reverse polish notation.
        """
        precedence = []
        operator_stack = []
        rpn = []

        for token in self.parsed_string:

            if token == '(':
                operator_stack.append(token)
                precedence.append(ExpressionParser.precedence[token])

            elif token in ("+", "-", "*", "/", "^",
                           "ABS", "EXP", "LOG", "L10",
                           "NEG", "SQRT"):
                pval = ExpressionParser.precedence[token]

                while True:
                    if precedence:
                        if pval <= precedence[-1]:
                            rpn.append(operator_stack.pop())
                            precedence.pop()
                        else:
                            break
                    else:
                        break

                operator_stack.append(token)
                precedence.append(ExpressionParser.precedence[token])

            elif token == ")":

                while True:
                    if operator_stack[-1] == "(":
                        operator_stack.pop()
                        precedence.pop()
                        break

                    else:
                        rpn.append(operator_stack.pop())
                        precedence.pop()

            else:
                try:
                    rpn.append(float(token))
                except ValueError:
                    # this is an array reference
                    if token.lower() in self.arrays:
                        rpn.append(token.lower())
                    else:
                        raise ValueError('variable name not referenced in arrays')

        for operator in reversed(operator_stack):
            rpn.append(operator)

        self.reverse_polish_notation = rpn

    def __evaluate_reverse_polish_expression(self):
        """
        Calculation based upon reverse polish notation
        """

        std_op = {"+": (lambda a, b: a + b),
                  "-": (lambda a, b: a - b),
                  "*": (lambda a, b: a * b),
                  "/": (lambda a, b: a / b),
                  "^": (lambda a, b: a ** b)}

        adv_op = {"ABS": (lambda a: np.abs(a)),
                  "EXP": (lambda a: np.exp(a)),
                  "LOG": (lambda a: np.log(a)),
                  "L10": (lambda a: np.log10(a)),
                  "SQRT": (lambda a: np.sqrt(a)),
                  "NEG": (lambda a: -1 * a)}

        tokens = self.reverse_polish_notation
        stack = []

        for token in tokens:
            if token in std_op:
                arg2 = stack.pop()
                arg1 = stack.pop()
                result = std_op[token](arg1, arg2)
                stack.append(result)

            elif token in adv_op:
                arg = stack.pop()
                result = adv_op[token](arg)
                stack.append(result)

            elif token in self.arrays:
                try:
                    stack.append(self.arrays[token].array)
                except AttributeError:
                    stack.append(self.arrays[token])

            else:
                stack.append(token)

        self.result = stack.pop()


class FunctionParser(object):
    """
    Simple parser for the Function(s) in the modflow MULT file
    Reminder: Functions do not follow order of operations, they
    only calculate from left to right.

    Parameters:
        s: (str) Function to be parsed
        arrays: (dict) Dictionary of variable arrays
    """
    def __init__(self, s, arrays={}):
        self.original_string = s
        self.parsed_string = ""
        self.arrays = arrays
        self.result = None
        s = self.__line_prep(s)
        if s:
            self.__parse_string(s)
            self.__evaluate_function()

    def __line_prep(self, s):
        """
        Prepare a line for further processing

        """
        o = ""
        for i in s:
            if i == "#":
                return o
            o += i

        return o

    def __parse_string(self, s):

        """
        Parse the expression string into a list object

        Parameters:
            s: (string) expression string
        """
        parsed = []
        obj = ""
        for c in s:
            if c in ("(", ")"):
                if obj:
                    parsed.append(obj)
                    obj = ""
                parsed.append(c)

            elif c == " ":
                if obj:
                    parsed.append(obj)
                    obj = ""

            elif c in ('*', '/', '+', '-', '^'):
                if obj:
                    parsed.append(obj)
                    obj = ""
                parsed.append(c)

            else:
                obj += c

        if obj:
            parsed.append(obj)

        self.parsed_string = parsed

    def __evaluate_function(self):
        """
        Method to evalute MODFLOW MULT FUNCTION, which does not
        follow order or operation!
        """
        std_op = {"+": (lambda a, b: a + b),
                  "-": (lambda a, b: a - b),
                  "*": (lambda a, b: a * b),
                  "/": (lambda a, b: a / b),
                  "^": (lambda a, b: a ** b)}

        t = self.parsed_string
        basename = t.pop(0).lower()
        multarray = self.arrays[basename]
        try:
            multarray = multarray.array.copy()
        except:
            multarray = multarray.copy()

        # Construct the multiplier array
        while True:
            if len(t) < 2:
                break
            op = t.pop(0)
            multname = t.pop(0).lower()
            try:
                atemp = self.arrays[multname].array
            except:
                atemp = self.arrays[multname]

            if op not in std_op:
                s = 'Invalid MULT operation {}'.format(op)
                raise Exception(s)

            else:
                multarray = std_op[op](multarray, atemp)

        self.result = multarray


if __name__ == '__main__':

    x = '4 ^ 6 + (m1 * 3) ^ (2 - 1)'
    arr = {'m1': np.ones((5, 5))}
    expression = ExpressionParser(x, arr)
    print(expression.result)

    x = 'x1 + x2 ^ x3'
    arr = {'x1': np.ones((5, 5)) * 1.5,
           'x2': np.ones((5, 5)) * 3.,
           'x3': np.ones((5, 5)) * 0.45}
    function = FunctionParser(x, arr)
    print(function.result)