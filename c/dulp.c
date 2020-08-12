/*
 * Floating point differences --- dulp
 *
 * dulp`_ measures directed differences between floating point numbers
 * by counting the discrete spaces between them.
 *
 * This distance was proposed by an anonymous reviewer to
 * "On the definition of ulp(x)" (JM Muller 2005).
 *
 *
 * #include <stdint.h>
 * #include "dulp.c"
 *
 * dulp(1., 1. + pow(2, -52)); // 1.
 * dulp((1. + sqrt(5))/2, 1.6180339887); // -224707.
 * dulpf(-0., 0.) // 1.f
 *
 *
 * Each float or double gets an integer valuation val(x) which satisfies
 *     val(0.) == 0
 * and
 *     val(x, x + eps) == 1
 * where x + eps is the next floating point number after x.
 *
 * Floats almost have this naturally when reinterpreted as integers,
 * but are reversed for negative numbers.
 * We just reverse negative numbers' order.
 *
 *
 * The dulp directed distance from x to y equals val(y) - val(x), in
 * double precision for convenience with small and large distances.
 *
 *
 * dulpbits converts the dulp distance to a bits-precision equivalent.
 *
 *
 * Assumes IEEE 764 binary64 and binary32 for doubles and floats.
 *
 *
 * Context:
 *
 * math.h
 *     fabs, log2
 *
 * stdint.h
 *     int_least32_t int_least64_t
 *     uint_least32_t uint_least64_t
 *     uint_fast8_t
 */

static double dulpbits(double delta);

static double dulp(double x, double y);
static double dulpf(float x, float y);

static int_least64_t dulpval(double x);
static int_least32_t dulpvalf(float x);

static double dulpdif(int_least64_t valx, int_least64_t valy);
static double dulpdiff(int_least32_t valx, int_least32_t valy);

static int_least64_t dulpsar(int_least64_t m, uint_fast8_t n);


/*
 * Bits-equivalent of dulp distance delta.
 *
 * The form log2(|delta| + 1) satisfies
 *     bits(0) == 0
 *     bits(1) == 1
 *     bits(0b111) == 3               (0b111 == 7)
 * with interpolation such that
 *     3 < bits(0b1000) < 4          (0b1000 == 8)
 * and so on.
 */
static double
dulpbits(double delta)
{
    double distance = fabs(delta);
    return log2(distance + 1.);
}


/*
 * Directed distances for double and float.
 *
 * Returns double since 53 bits of precision are plenty, and inexact
 * representations allow signed differences between 64 bit numbers.
 *
 * Please cast to float for increased memory performance.
 */
static double
dulp(double x, double y)
{
    int_least64_t valx = dulpval(x);
    int_least64_t valy = dulpval(y);
    return dulpdif(valx, valy);
}


static double
dulpf(float x, float y)
{
    int_least32_t valx = dulpvalf(x);
    int_least32_t valy = dulpvalf(y);
    return dulpdiff(valx, valy);
}


/*
 * Integer valuations of double and float.
 *
 * The binary representation naturally has negative numbers in reverse.
 * This bit-twiddle reverses the order of negative values again, while
 * leaving others unchanged.
 *
 * Equivalent to
 * if (i < 0)
 *     return -((uint)1 << (bits - 1)) - i - 1;
 * else
 *     return i;
 */
static int_least64_t
dulpval(double x)
{
    const int_least64_t mask = ((uint_least64_t)1 << 63) - 1;
    union {double f64; int_least64_t i64;} word = {x};
    return -(word.i64 < 0) ^ (word.i64 & mask);
}


static int_least32_t
dulpvalf(float x)
{
    const int_least32_t mask = ((uint_least32_t)1 << 31) - 1;
    union {float f32; int_least32_t i32;} word = {x};
    return -(word.i32 < 0) ^ (word.i32 & mask);
}


/*
 * Find the difference of valuations and cast to double.
 *
 * Lacking signed types larger than 64 bits, we split into high and low
 * 32-bit parts and recombine them as doubles.
 */
static double
dulpdif(int_least64_t valx, int_least64_t valy)
{
    const int shift = 32;
    const int_least64_t mask = ((int_least64_t)1 << shift) - 1;
    const double scale = mask + 1;
    int_least64_t hi = dulpsar(valy, shift) - dulpsar(valx, shift);
    int_least64_t lo = (valy & mask) - (valx & mask);
    return scale*hi + lo;
}


static double
dulpdiff(int_least32_t valx, int_least32_t valy)
{
    return (int_least64_t)valy - valx;
}


/*
 * Portable arithmetic right shift
 * From github.com/Rupt/c-arithmetic-right-shift
 */
static int_least64_t
dulpsar(int_least64_t m, uint_fast8_t n)
{
    const int logical = (((int_least64_t)-1) >> 1) > 0;
    uint_least64_t fixu = -(logical & (m < 0));
    /* Cast type punning is defined for signed/unsigned pairs */
    int_least64_t fix = *(int_least64_t*)&fixu;
    return (m >> n) | (fix ^ (fix >> n));
}
