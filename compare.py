import re
import argparse
import ast

class Compare:
    @staticmethod
    def levenshtein(prey, suss):
        dp = [[0 for j in range(len(suss) + 1)] for i in range(len(prey) + 1)]

        for i in range(len(prey) + 1):
            dp[i][0] = i

        for j in range(len(suss) + 1):
            dp[0][j] = j

        for i in range(1, len(prey) + 1):
            for j in range(1, len(suss) + 1):
                if prey[i - 1] == suss[j - 1]:
                    cost = 0
                else:
                    cost = 1

                dp[i][j] = min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost,
                )
        return 1 - dp[len(prey)][len(suss)]/(max(len(prey), len(suss)))


class NormalizeTree:
    """Normalize ast. Сonverting tree nodes to tokens"""

    def __init__(self):
        self.regular = {'M': ("Module"),
              'D': ("FunctionDef", "AsyncFunctionDef", "ClassDef"),
              'R': ("Return"),
              'Q': ("Delete"),
              'A': ("Assign", "AugAssign", "AnnAssign"),
              'F': ("For", "AsyncFor", "While"),
              'I': ("If", "With", "AsyncWith"),
              'Z': ("Match"),
              'T': ("Raise", "Try", "TryStar", "Assert"),
              'G': ("Global", "Nonlocal", "Expr", "Pass"),
              'B': ("Import", "ImportFrom"),
              'J': ("BoolOp", "NamedExpr", "BinOp", "UnaryOp", "Lambda", "IfExp"),
              'S': ("Dict", "Set", "ListComp", "SetComp", "DictComp", "GeneratorExp"),
              'Y': ("Await", "Yield", "YieldFrom"),
              'C': ("Compare", "Call", "FormattedValue", "JoinedStr", "Constant"),
              'L': ("Attribute", "Subscript", "Starred", "Name", "List"),
              'V': ("Load", "Store", "Del"),
              'O': ("Add", "Sub", "Mult", "MatMult", "Div", "Mod", "Pow", "LShift",
                    "RShift", "BitOr", "BitXor", "BitAnd", "FloorDiv", "And", "Or"),
              'N': ("Invert", "Not", "UAdd", "USub"),
              'E': ("Eq", "NotEq", "Lt", "LtE", "Gt", "GtE", "Is", "IsNot", "In", "NotIn"),
              'H': ("comprehension"),
              'X': ("excepthandler"),
              'U': ("arguments"),
              'W': ("arg"),
              'K': ("keyword"),
              'P': ("MatchValue", "MatchSingleton", "MatchSequence", "MatchMapping", "MatchClass", "MatchStar", "MatchAs", "MatchOr")
               }

    def normalize(self, tree):
        for repl, pattern in self.regular.items():
            if type(pattern) == str:
                tree = re.sub(pattern, repl, tree)
            else:
                for patter in pattern:
                    patter = re.compile(patter)
                    tree = re.sub(patter, repl, tree)

        tree = re.sub(r'[^MFRDAZIVXGBJLYCTEOUQNHSWKP]', '', tree)
        return tree


class TreeCode:
    @staticmethod
    def get_tree(filename):
        with open(filename, 'r', encoding="utf-8") as code:
            tree = ast.parse(code.read())
        dump = ast.dump(tree)
        return dump


def main(args):
    res = ""
    normalizer = NormalizeTree()
    with open(args.input, 'r') as f:
        for line in f:
            file1, file2 = line.split()
            tree1 = TreeCode.get_tree(file1)
            tree2 = TreeCode.get_tree(file2)
            norm_tree1 = normalizer.normalize(tree1)
            norm_tree2 = normalizer.normalize(tree2)
            plag_chek = Compare.levenshtein(norm_tree1, norm_tree2)
            res += str(plag_chek) + "\n"


    with open(args.output, 'w') as out:
        out.write(res)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="antiplagiat", description="Check python file on antiplagiat")
    parser.add_argument("input", help="input filename")
    parser.add_argument("output", help="output filename")

    main(parser.parse_args())
