"""
TODO documentation

python -m timeit -vv -s "from dulp_numpy import perf" "perf()"


"""
from numpy import array, asanyarray
from numpy import float32, float64
from numpy import int32, int64
from numpy import uint32, uint64


def dulp(x, y):
    x = asanyarray(x)
    y = asanyarray(y)

    if x.dtype is not y.dtype:
        raise TypeError("%s is not %s" % (x.dtype, y.dtype))

    if x.dtype.type is float64:
        r = _dulp(x, y)
    elif x.dtype.type is float32:
        r = _dulpf(x, y)
    else:
        raise TypeError("%s not in (float64, float32)" % x.dtype)

    return r


def val(x):
    x = asanyarray(x)

    if x.dtype.type is float64:
        r = _val(x)
    elif x.dtype.type is float32:
        r = _valf(x)
    else:
        raise TypeError("%s not in (float64, float32)" % x.dtype)

    return r


def dif(vx, vy):
    vx = asanyarray(vx)
    vy = asanyarray(vy)

    if vx.dtype is not vy.dtype:
        raise TypeError("%s is not %s" % (vx.dtype, vy.dtype))

    if vx.dtype.type is uint64:
        r = _dif(vx, vy)
    elif vx.dtype.type is uint32:
        r = _diff(vx, vy)
    else:
        raise TypeError("%s not in (uint64, uint32)" % vx.dtype)

    return r


def _dulp(x, y):
    vx = _val(x)
    vy = _val(y)
    return _dif(vx, vy)


def _dulpf(x, y):
    vx = _valf(x)
    vy = _valf(y)
    return _diff(vx, vy)


def _val(x):
    shift = int64(63)
    sign = int64(1) << shift
    u = x.view(int64)
    r = u >> shift
    r |= int64(1) << shift
    r ^= u
    return r.view(uint64)


def _valf(x):
    shift = int32(31)
    u = x.view(int32)
    r = u >> shift
    r |= int32(1) << shift
    r ^= u
    return r.view(uint32)


def _dif(vx, vy):
    shift = uint64(32)
    mask = (uint64(1) << shift) - uint64(1)
    scale = float64(mask + 1)
    hi = (vy >> shift).view(int64)
    hi -= (vx >> shift).view(int64)
    lo = (vy & mask).view(int64)
    lo -= (vx & mask).view(int64)
    return scale*hi + lo


def _diff(vx, vy):
    r = vy.astype(int64) - vx.astype(int64)
    return r.astype(float64)
