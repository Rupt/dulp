CC=cc
CFLAGS=-Wall -Wextra -pedantic -Werror -std=c99 -fsanitize=undefined
LDFLAGS=-lm
PYLINTFLAGS=--exit-zero --score n


options:
	@echo "CC=${CC}"
	@echo "CFLAGS=${CFLAGS}"
	@echo "LDFLAGS=${LDFLAGS}"
	@echo "PYLINTFLAGS=${PYLINTFLAGS}"


clean:
	rm -f *.pyc *.o test-c perf.*
	rm -rf py/dulp/{,np/}__pycache__


test-py: py/dulp/test.py
	python py/dulp/test.py


test-numpy: py/dulp/test_numpy.py
	python py/dulp/test_numpy.py


test-c: c/test.c c/dulp.c
	$(CC) c/test.c -o $@ $(CFLAGS) $(LDFLAGS)
	./$@


test: test-c test-py test-numpy


lint:
	# with a grain of salt
	pylint py/dulp $(PYLINTFLAGS)


bench-numpy:
	python -m timeit -vv -s "\
	from py.dulp.np import dulp;\
	from py.dulp.bench_numpy import init;\
	x, y = init()" \
	"dulp(x, y)"


bench-numpyf:
	python -m timeit -vv -s "\
	from py.dulp.np import dulp;\
	from py.dulp.bench_numpy import initf;\
	x, y = initf()" \
	"dulp(x, y)"


bench: bench-numpy bench-numpyf


.PHONY: options clean \
	lint \
	bench-numpy bench-numpyf bench
