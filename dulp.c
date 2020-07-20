/* dulp measures order distances between floating point numbers 
 
Assumes a context with stdint.h included
TODO explanation
*/

uint64_t
dulpval(double x)
{
    union {double f; uint64_t i;} u = {x};
    return -(u.i >> 63) ^ (u.i | 1llu << 63);
}


double
dulp(double x, double y)
{
    uint64_t vx = dulpval(x);
    uint64_t vy = dulpval(y);
    int lo = (vy & 1) - (vx & 1);
    int64_t hi = (vy >> 1) - (vx >> 1);
    return (float)lo + hi + hi;
}


uint32_t
dulpvalf(float x)
{
    union {float f; uint32_t i;} u = {x};
    return -(u.i >> 31) ^ (u.i | 1lu << 31);
}


float
dulpf(float x, float y)
{
    uint32_t vx = dulpvalf(x);
    uint32_t vy = dulpvalf(y);
    int lo = (vy & 1) - (vx & 1);
    int32_t hi = (vy >> 1) - (vx >> 1);
    return (float)lo + hi + hi;
}
