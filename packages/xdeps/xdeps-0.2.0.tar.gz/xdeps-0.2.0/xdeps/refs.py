# copyright ############################### #
# This file is part of the Xdeps Package.   #
# Copyright (c) CERN, 2021.                 #
# ######################################### #


from dataclasses import dataclass, field
import operator, builtins, math

_binops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "@": operator.matmul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
    "&": operator.and_,
    "|": operator.or_,
    "^": operator.xor,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    ">": operator.gt,
    ">>": operator.rshift,
    "<<": operator.lshift,
}

_mutops = {
    "+": operator.iadd,
    "//": operator.ifloordiv,
    "<<": operator.ilshift,
    "@": operator.imatmul,
    "%": operator.imod,
    "*": operator.imul,
    "**": operator.ipow,
    ">>": operator.irshift,
    "-": operator.isub,
    "/": operator.itruediv,
    "^": operator.ixor,
}


_unops = {"-": operator.neg, "+": operator.pos, "~": operator.invert}

_builtins = {
    "divmod": builtins.divmod,
    "abs": builtins.abs,
    "complex": builtins.complex,
    "int": builtins.int,
    "float": builtins.float,
    "round": builtins.round,
    "trunc": math.trunc,
    "floor": math.floor,
    "ceil": math.ceil,
}


def _pr_binop():
    for sy, op in _binops.items():
        fn = op.__name__.replace("_", "")
        rr = fn.capitalize()
        fmt = f"""
       def __{fn}__(self, other):
           return {rr}Ref(self, other)  # type: ignore

       def __r{fn}__(self, other):
           return {rr}Ref(other, self)  # type: ignore"""
        print(fmt)


def _pr_builtins():
    for sy, op in _builtins.items():
        fn = op.__name__.replace("_", "")
        rr = fn.capitalize()
        fmt = f"""
       def __{fn}__(self, other): 
           return {rr}Ref(self, other)  # type: ignore"""
        print(fmt)

    ### careful with abs, round, floor, ceil


def _pr_mutops():
    for sy, op in _mutops.items():
        fn = op.__name__.replace("_", "")
        fmt = f"""
    def __{fn}__(self, other):
        newexpr=self._expr
        if newexpr:
            return newexpr{sy}other
        else:
            return self._get_value(){sy}other"""
        print(fmt)

def _isref(obj):
    return isinstance(obj, ARef)

class ARef:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise ValueError("Cannot instantiate ARef")

    @staticmethod
    def _mk_value(value):
        if isinstance(value, ARef):
            return value._get_value()
        else:
            return value

    @property
    def _value(self):
        return self._get_value()

    # order of precedence
    def __call__(self, *args, **kwargs):
        return CallRef(self, args, kwargs)

    def __getitem__(self, item):
        return ItemRef(self, item, self._manager)

    def __getattr__(self, attr):
        if attr.startswith("__array_"):  # numpy crashes without
            # print(self,attr)
            raise AttributeError
        if attr == '_manager':
            raise RuntimeError("This should not happen...")
        return AttrRef(self, attr, self._manager)

    # Untested:

    # def __getstate__(self):
    #     raise ValueError("Cannot pickle ARef")

    # def __setstate__(self, state):
    #     raise ValueError("Cannot pickle ARef")

    # numerical unary  operator
    def __neg__(self):
        return NegRef(self)  # type: ignore

    def __pos__(self):
        return PosRef(self)  # type: ignore

    def __invert__(self):
        return InvertRef(self)  # type: ignore

    # numerical binary operators

    def __add__(self, other):
        return AddRef(self, other)  # type: ignore

    def __radd__(self, other):
        return AddRef(other, self)  # type: ignore

    def __sub__(self, other):
        return SubRef(self, other)  # type: ignore

    def __rsub__(self, other):
        return SubRef(other, self)  # type: ignore

    def __mul__(self, other):
        return MulRef(self, other)  # type: ignore

    def __rmul__(self, other):
        return MulRef(other, self)  # type: ignore

    def __matmul__(self, other):
        return MatmulRef(self, other)  # type: ignore

    def __rmatmul__(self, other):
        return MatmulRef(other, self)  # type: ignore

    def __truediv__(self, other):
        return TruedivRef(self, other)  # type: ignore

    def __rtruediv__(self, other):
        return TruedivRef(other, self)  # type: ignore

    def __floordiv__(self, other):
        return FloordivRef(self, other)  # type: ignore

    def __rfloordiv__(self, other):
        return FloordivRef(other, self)  # type: ignore

    def __mod__(self, other):
        return ModRef(self, other)  # type: ignore

    def __rmod__(self, other):
        return ModRef(other, self)  # type: ignore

    def __pow__(self, other):
        return PowRef(self, other)  # type: ignore

    def __rpow__(self, other):
        return PowRef(other, self)  # type: ignore

    def __and__(self, other):
        return AndRef(self, other)  # type: ignore

    def __rand__(self, other):
        return AndRef(other, self)  # type: ignore

    def __or__(self, other):
        return OrRef(self, other)  # type: ignore

    def __ror__(self, other):
        return OrRef(other, self)  # type: ignore

    def __xor__(self, other):
        return XorRef(self, other)  # type: ignore

    def __rxor__(self, other):
        return XorRef(other, self)  # type: ignore

    def __lt__(self, other):
        return LtRef(self, other)  # type: ignore

    def __rlt__(self, other):
        return LtRef(other, self)  # type: ignore

    def __le__(self, other):
        return LeRef(self, other)  # type: ignore

    def __rle__(self, other):
        return LeRef(other, self)  # type: ignore

    def __eq__(self, other):
        return EqRef(self, other)  # type: ignore

    def __req__(self, other):
        return EqRef(other, self)  # type: ignore

    def __ne__(self, other):
        return NeRef(self, other)  # type: ignore

    def __rne__(self, other):
        return NeRef(other, self)  # type: ignore

    def __ge__(self, other):
        return GeRef(self, other)  # type: ignore

    def __rge__(self, other):
        return GeRef(other, self)  # type: ignore

    def __gt__(self, other):
        return GtRef(self, other)  # type: ignore

    def __rgt__(self, other):
        return GtRef(other, self)  # type: ignore

    def __rshift__(self, other):
        return RshiftRef(self, other)  # type: ignore

    def __rrshift__(self, other):
        return RshiftRef(other, self)  # type: ignore

    def __lshift__(self, other):
        return LshiftRef(self, other)  # type: ignore

    def __rlshift__(self, other):
        return LshiftRef(other, self)  # type: ignore

    def __divmod__(self, other):
        return BDivmodRef(self, other)  # type: ignore

    def __pow__(self, other):
        return PowRef(self, other)  # type: ignore

    def __round__(self, other=0):
        return BRoundRef(self, other)  # type: ignore

    def __trunc__(self, other):
        return BTruncRef(self, other)  # type: ignore

    def __floor__(self, other):
        return BFloorRef(self, other)  # type: ignore

    def __ceil__(self, other):
        return BCeilRef(self, other)  # type: ignore

    def __abs__(self):
        return BAbsRef(self)  # type: ignore

    def __complex__(self):
        return BComplexRef(self)  # type: ignore

    def __int__(self):
        return BIntRef(self)  # type: ignore

    def __float__(self):
        return BFloatRef(self)  # type: ignore


class MutableRef(ARef):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise ValueError("Cannot instantiate MutableRef")

    def __setitem__(self, key, value):
        ref = ItemRef(self, key, self._manager)
        self._manager.set_value(ref, value)

    def __setattr__(self, attr, value):
        if attr[0] == "_" and attr in ["_expr", "_exec"]:
            raise ValueError(f"`{attr}` is a special keyword and cannot be assigned.")
        ref = AttrRef(self, attr, self._manager)
        self._manager.set_value(ref, value)

    def _eval(self, expr, gbl=None):
        if gbl is None:
            gbl = {}
        return eval(expr, gbl, self)

    def _exec(self, expr, gbl=None):
        if gbl is None:
            gbl = {}
        exec(expr, gbl, self)

    @property
    def _tasks(self):
        return self._manager.tartasks[self]

    def _find_dependant_targets(self):
        return self._manager.find_deps([self])

    @property
    def _expr(self):
        if self in self._manager.tasks:
            task = self._manager.tasks[self]
            if hasattr(task, "expr"):
                return task.expr

    def _info(self, limit=10):
        print(f"#  {self}._get_value()")
        try:
            value = self._get_value()
            print(f"   {self} = {value}")
        except:
            print(f"#  {self} has no value")
        print()

        if self in self._manager.tasks:
            task = self._manager.tasks[self]
            print(f"#  {self}._expr")
            print(f"   {task}")
            print()
            if hasattr(task, "info"):
                task.info()
        else:
            print(f"#  {self}._expr is None")
            print()

        refs = self._manager.find_deps([self])[1:]
        if len(refs) == 0:
            print(f"#  {self} does not influence any target")
            print()
        else:
            print(f"#  {self}._find_dependant_targets()")
            for tt in refs[:limit]:
                if tt._expr is not None:
                    print(f"   {tt}")
            if len(refs) > limit:
                print(f"   ... set _info(limit={len(refs)}) to get all lines")
            print()

    def __iadd__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr + other
        else:
            return self._get_value() + other

    def __ifloordiv__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr // other
        else:
            return self._get_value() // other

    def __ilshift__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr << other
        else:
            return self._get_value() << other

    def __imatmul__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr @ other
        else:
            return self._get_value() @ other

    def __imod__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr % other
        else:
            return self._get_value() % other

    def __imul__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr * other
        else:
            return self._get_value() * other

    def __ipow__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr**other
        else:
            return self._get_value() ** other

    def __irshift__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr >> other
        else:
            return self._get_value() >> other

    def __isub__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr - other
        else:
            return self._get_value() - other

    def __itruediv__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr / other
        else:
            return self._get_value() / other

    def __ixor__(self, other):
        newexpr = self._expr
        if newexpr:
            return newexpr ^ other
        else:
            return self._get_value() ^ other


class AttrRef(MutableRef):
    __slots__ = ("_owner", "_key", "_manager")

    def __init__(self, _owner, _key, _manager=None):
        object.__setattr__(self, "_owner", _owner)
        object.__setattr__(self, "_key", _key)
        object.__setattr__(self, "_manager", _manager)

    # Untested:

    # def __getstate__(self):
    #     return self._owner, self._key, self._manager

    # def __setstate__(self, state):
    #     object.__setattr__(self, "_owner", state[0])
    #     object.__setattr__(self, "_key", state[1])
    #     object.__setattr__(self, "_manager", state[2])

    def __hash__(self):
        if isinstance(self._owner, ARef):
            own = self._owner
        else:
            own = id(self._owner)
        return hash((own, self._key))

    def _get_value(self):
        owner = ARef._mk_value(self._owner)
        attr = ARef._mk_value(self._key)
        return getattr(owner, attr)

    def _set_value(self, value):
        owner = ARef._mk_value(self._owner)
        attr = ARef._mk_value(self._key)
        setattr(owner, attr, value)

    def _get_dependencies(self, out=None):
        if out is None:
            out = set()
        if isinstance(self._owner, ARef):
            self._owner._get_dependencies(out)
        if isinstance(self._key, ARef):
            self._key._get_dependencies(out)
        out.add(self)
        return out

    def __repr__(self):
        return f"{self._owner}.{self._key}"


class Ref(MutableRef):
    __slots__ = ("_owner", "_manager", "_label")

    def __init__(self, _owner, _manager=None, _label="_"):
        object.__setattr__(self, "_owner", _owner)
        object.__setattr__(self, "_manager", _manager)
        object.__setattr__(self, "_label", _label)

    # Untested:

    # def __getstate__(self):
    #     return self._owner, self._manager, self._label

    # def __setstate__(self, state):
    #     object.__setattr__(self, "_owner", state[0])
    #     object.__setattr__(self, "_manager", state[1])
    #     object.__setattr__(self, "_label", state[2])

    def __hash__(self):
        return hash(self._label)

    def __repr__(self):
        return self._label

    def _get_value(self):
        return ARef._mk_value(self._owner)


class ItemRef(MutableRef):
    __slots__ = ("_owner", "_key", "_manager")

    def __init__(self, _owner, __key, _manager=None):
        object.__setattr__(self, "_owner", _owner)
        object.__setattr__(self, "_key", __key)
        object.__setattr__(self, "_manager", _manager)

    # Untested:

    # def __getstate__(self):
    #     return self._owner, self._key, self._manager

    # def __setstate__(self, state):
    #     object.__setattr__(self, "_owner", state[0])
    #     object.__setattr__(self, "_key", state[1])
    #     object.__setattr__(self, "_manager", state[2])

    def __hash__(self):
        if isinstance(self._owner, ARef):
            own = self._owner
        else:
            own = id(self._owner)
        return hash((own, self._key))

    def _get_value(self):
        owner = ARef._mk_value(self._owner)
        item = ARef._mk_value(self._key)
        return owner[item]

    def _set_value(self, value):
        owner = ARef._mk_value(self._owner)
        item = ARef._mk_value(self._key)
        owner[item] = value

    def _get_dependencies(self, out=None):
        if out is None:
            out = set()
        if isinstance(self._owner, ARef):
            self._owner._get_dependencies(out)
        if isinstance(self._key, ARef):
            self._key._get_dependencies(out)
        out.add(self)
        return out

    def __repr__(self):
        return f"{self._owner}[{repr(self._key)}]"


class ItemDefaultRef(MutableRef):
    __slots__ = ("_owner", "_key", "_manager", "_default")

    def __init__(self, _owner, _key, _manager=None, _default=0):
        object.__setattr__(self, "_owner", _owner)
        object.__setattr__(self, "_key", _key)
        object.__setattr__(self, "_manager", _manager)
        object.__setattr__(self, "_default", _default)

    # Untested:

    # def __getstate__(self):
    #     return self._owner, self._key, self._manager, self._default

    # def __setstate__(self, state):
    #     object.__setattr__(self, "_owner", state[0])
    #     object.__setattr__(self, "_key", state[1])
    #     object.__setattr__(self, "_manager", state[2])
    #     object.__setattr__(self, "_default", state[3])

    def __hash__(self):
        if isinstance(self._owner, ARef):
            own = self._owner
        else:
            own = id(self._owner)
        return hash((own, self._key))

    def _get_value(self):
        owner = ARef._mk_value(self._owner)
        item = ARef._mk_value(self._key)
        return owner[item]

    def _set_value(self, value):
        owner = ARef._mk_value(self._owner)
        item = ARef._mk_value(self._key)
        owner[item] = value

    def _get_dependencies(self, out=None):
        if out is None:
            out = set()
        if isinstance(self._owner, ARef):
            self._owner._get_dependencies(out)
        if isinstance(self._key, ARef):
            self._key._get_dependencies(out)
        out.add(self)
        return out

    def __repr__(self):
        return f"{self._owner}[{repr(self._key)}]"


class ObjectAttrRef(Ref):

    # Untested:

    # def __getstate__(self):
    #     return self._manager

    # def __setstate__(self, state):
    #     object.__setattr__(self, "_manager", state)

    def __getattr__(self, attr):
        return ItemDefaultRef(self, attr, self._manager)

    def __setattr__(self, attr, value):
        ref = ItemDefaultRef(self, attr, self._manager)
        self._manager.set_value(ref, value)


@dataclass(frozen=True)
class BinOpRef(ARef):
    _a: object
    _b: object

    # Untested:

    # def __getstate__(self):
    #     return self._a, self._b

    # def __setstate__(self, state):
    #     object.__setattr__(self, "_a", state[0])
    #     object.__setattr__(self, "_b", state[1])

    def _get_value(self):
        a = ARef._mk_value(self._a)
        b = ARef._mk_value(self._b)
        return self._op(a, b)

    def _get_dependencies(self, out=None):
        a = self._a
        b = self._b
        if out is None:
            out = set()
        if isinstance(a, ARef):
            a._get_dependencies(out)
        if isinstance(b, ARef):
            b._get_dependencies(out)
        return out

    def __repr__(self):
        return f"({self._a}{self._st}{self._b})"


@dataclass(frozen=True)
class UnOpRef(ARef):
    _a: object

    # Untested:

    # def __getstate__(self):
    #     return self._a

    # def __setstate__(self, state):
    #     object.__setattr__(self, "_a", state)

    def _get_value(self):
        a = ARef._mk_value(self._a)
        return self._op(a)

    def _get_dependencies(self, out=None):
        a = self._a
        if out is None:
            out = set()
        if isinstance(a, ARef):
            a._get_dependencies(out)
        return out

    def __repr__(self):
        return f"({self._st}{self._a})"


@dataclass(frozen=True)
class BuiltinRef(ARef):
    _a: object

    # Untested:

    # def __getstate__(self):
    #     return self._a

    # def __setstate__(self, state):
    #     object.__setattr__(self, "_a", state)

    def _get_value(self):
        a = ARef._mk_value(self._a)
        return self._op(a)

    def _get_dependencies(self, out=None):
        a = self._a
        if out is None:
            out = set()
        if isinstance(a, ARef):
            a._get_dependencies(out)
        return out

    def __repr__(self):
        return f"{self._st}({self._a})"


@dataclass(frozen=True)
class CallRef(ARef):
    _func: object
    _args: tuple
    _kwargs: tuple

    # Untested:

    # def __getstate__(self):
    #     return self._func, self._args, self._kwargs

    # def __setstate__(self, state):
    #     object.__setattr__(self, "_func", state[0])
    #     object.__setattr__(self, "_args", state[1])
    #     object.__setattr__(self, "_kwargs", state[2])

    def _get_value(self):
        func = ARef._mk_value(self._func)
        args = [ARef._mk_value(a) for a in self._args]
        kwargs = {n: ARef._mk_value(v) for n, v in self._kwargs}
        return func(*args, **kwargs)

    def _get_dependencies(self, out=None):
        if out is None:
            out = set()
        if isinstance(self._func, ARef):
            self._func._get_dependencies(out)
        for arg in self._args:
            if isinstance(arg, ARef):
                arg._get_dependencies(out)
        for name, arg in self._kwargs:
            if isinstance(arg, ARef):
                arg._get_dependencies(out)
        return out

    def __repr__(self):
        args = []
        for aa in self._args:
            args.append(repr(aa))
        for k, v in self._kwargs:
            args.append(f"{k}={v}")
        args = ",".join(args)
        if isinstance(self._func, ARef):
            fname = repr(self._func)
        else:
            fname = self._func.__name__
        return f"{fname}({args})"


class RefList:
    """
    A list implementation that does not use __eq__ for comparisons. It is used
    for storing tasks, which need to be compared by their hash, as the usual
    == operator yields an expression, which is always True.
    """
    def __init__(self, *args, **kwargs):
        self.list = list(*args, **kwargs)

    def __repr__(self):
        return f"RefList({self.list})"

    def __contains__(self, item):
        try:
            self.index(item)
            return True
        except ValueError:
            return False

    def __getitem__(self, item):
        return self.list[item]

    def __delitem__(self, index):
        self.list.pop(index)

    def __iter__(self):
        return iter(self.list)

    def index(self, item):
        for ii, x in enumerate(self.list):
            if hash(item) == hash(x):
                return ii
        raise ValueError(f'{item} is not in list')

    def extend(self, other):
        if isinstance(other, RefList):
            other = other.list
        self.list.extend(other)

    def append(self, item):
        self.list.append(item)

    def remove(self, item):
        del self[self.index(item)]


gbl = globals()
for st, op in _binops.items():
    fn = op.__name__.replace("_", "")
    cn = f"{fn.capitalize()}Ref"
    mn = f"__{fn}__"
    gbl[cn] = type(cn, (BinOpRef,), {"_op": op, "_st": st})

for st, op in _unops.items():
    fn = op.__name__.replace("_", "")
    cn = f"{fn.capitalize()}Ref"
    if cn in gbl:
        raise ValueError
    mn = f"__{fn}__"
    gbl[cn] = type(cn, (UnOpRef,), {"_op": op, "_st": st})

for st, op in _builtins.items():
    fn = op.__name__.replace("_", "")
    cn = f"B{fn.capitalize()}Ref"
    if cn in gbl:
        raise ValueError
    mn = f"__{fn}__"
    gbl[cn] = type(cn, (BuiltinRef,), {"_op": op, "_st": st})
