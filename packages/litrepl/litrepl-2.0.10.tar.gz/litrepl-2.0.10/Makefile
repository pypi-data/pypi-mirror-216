.DEFAULT_GOAL = all
VERSION = $(shell python3 setup.py --version)
WHEEL = dist/litrepl-$(VERSION)-py3-none-any.whl
PY = $(shell find -name '*\.py' | grep -v semver.py | grep -v revision.py)
TESTS = ./sh/test.sh

.stamp_test: $(PY) $(TESTS) Makefile python/bin/litrepl
	LITREPL_BIN="python `pwd`/python/bin/litrepl" \
	LITREPL_ROOT=`pwd`/python \
	sh ./sh/test.sh
	touch $@

.PHONY: test
test: .stamp_test

$(WHEEL): $(PY) Makefile .stamp_test
	test -n "$(VERSION)"
	rm -rf build dist || true
	python3 setup.py sdist bdist_wheel
	test -f $@

.PHONY: wheel
wheel: $(WHEEL)

.PHONY: version
version:
	@echo $(VERSION)

.PHONY: upload
upload: $(WHEEL)
	twine upload dist/*

.PHONY: all
all: wheel

