def parse_prefix(expr):
    tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
    def parse(tokens):
        token = tokens.pop(0)
        if token == '(':
            lst = []
            while tokens[0] != ')':
                lst.append(parse(tokens))
            tokens.pop(0)  # remove ')'
            return lst
        elif token == ')':
            raise ValueError("Unexpected )")
        else:
            try:
                return int(token)
            except:
                try:
                    return float(token)
                except:
                    return token
    return parse(tokens)

def to_prefix(expr):
    if isinstance(expr, list):
        return '(' + ' '.join(to_prefix(e) for e in expr) + ')'
    else:
        return str(expr)

def simplify(expr):
    if isinstance(expr, list):
        op = expr[0]
        args = [simplify(e) for e in expr[1:]]

        # Basit toplama çıkarma çarpma bölme güçlendirme sabit işlemleri
        # Burada sadece temel sadeleştirmeler yapılacak
        if op == '+':
            # (+ 0 x) veya (+ x 0) -> x
            if 0 in args:
                args = [a for a in args if a != 0]
                if not args:
                    return 0
                if len(args) == 1:
                    return args[0]
            # eğer tüm args sabitse topla
            if all(isinstance(a, (int,float)) for a in args):
                return sum(args)
            return [op] + args
        elif op == '-':
            if len(args) == 1:
                # unary minus
                if isinstance(args[0], (int,float)):
                    return -args[0]
                return [op] + args
            if all(isinstance(a, (int,float)) for a in args):
                return args[0] - args[1]
            if args[1] == 0:
                return args[0]
            return [op] + args
        elif op == '*':
            # (* 0 x) veya (* x 0) -> 0
            if 0 in args:
                return 0
            # (* 1 x) veya (* x 1) -> x
            args = [a for a in args if a != 1]
            if not args:
                return 1
            if len(args) == 1:
                return args[0]
            if all(isinstance(a, (int,float)) for a in args):
                res = 1
                for a in args:
                    res *= a
                return res
            return [op] + args
        elif op == '/':
            # (/ x 1) -> x
            if args[1] == 1:
                return args[0]
            if args[0] == 0:
                return 0
            if all(isinstance(a, (int,float)) for a in args):
                return args[0] / args[1]
            return [op] + args
        elif op == '^':
            # (^ x 0) -> 1
            if args[1] == 0:
                return 1
            # (^ x 1) -> x
            if args[1] == 1:
                return args[0]
            if all(isinstance(a, (int,float)) for a in args):
                return args[0] ** args[1]
            return [op] + args
        else:
            # fonksiyonlar için arg sadeleştir
            return [op] + args
    else:
        return expr

def derivative(expr):
    if isinstance(expr, (int,float)):
        return 0
    if isinstance(expr, str):
        if expr == 'x':
            return 1
        else:
            return 0
    op = expr[0]
    if op == '+':
        return ['+', derivative(expr[1]), derivative(expr[2])]
    if op == '-':
        if len(expr) == 2:
            return ['-', derivative(expr[1])]
        else:
            return ['-', derivative(expr[1]), derivative(expr[2])]
    if op == '*':
        u, v = expr[1], expr[2]
        return ['+', ['*', derivative(u), v], ['*', u, derivative(v)]]
    if op == '/':
        u, v = expr[1], expr[2]
        numerator = ['-', ['*', derivative(u), v], ['*', u, derivative(v)]]
        denominator = ['^', v, 2]
        return ['/', numerator, denominator]
    if op == '^':
        base, exp = expr[1], expr[2]
        if isinstance(exp, (int,float)):
            return ['*', exp, ['*', ['^', base, exp-1], derivative(base)]]
        else:
            # Genel güç kuralı (exp değişken ise)
            return ['*', expr, ['+', ['*', derivative(exp), ['ln', base]], ['*', exp, ['/', derivative(base), base]]]]
    if op == 'sin':
        u = expr[1]
        return ['*', derivative(u), ['cos', u]]
    if op == 'cos':
        u = expr[1]
        return ['*', ['-', 0, derivative(u)], ['sin', u]]
    if op == 'tan':
        u = expr[1]
        # tan'(u) = (1 / cos(u)^2) * u'
        return ['*', derivative(u), ['^', ['cos', u], -2]]
    if op == 'exp':
        u = expr[1]
        return ['*', derivative(u), ['exp', u]]
    if op == 'ln':
        u = expr[1]
        return ['/', derivative(u), u]
    raise ValueError("Unknown operator " + op)

def diff(expr):
    parsed = parse_prefix(expr)
    deriv = derivative(parsed)
    simp = simplify(deriv)
    return to_prefix(simp)
  
print(diff("(* 1 x)"))        # output: 1
print(diff("(^ x 3)"))        # output: (* 3 (^ x 2))
print(diff("(cos x)"))        # output: (* -1 (sin x))
print(diff("(tan x)"))        # output: (* (/ 1 (^ (cos x) 2)) 1) veya (* (^ (cos x) -2) 1) gibi olabilir
