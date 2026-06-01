# MiniCompiler Makefile

PREFIX = /usr/local
TARGET = mycc

all: $(TARGET)

$(TARGET):
	chmod +x $(TARGET)

install:
	cp $(TARGET) $(PREFIX)/bin/

clean:
	rm -f *.o *.asm *.exe factorial simple array test
	rm -rf __pycache__ src/__pycache__ src/*/__pycache__ tests/__pycache__

test-all:
	@echo "=== Sprint 7 Tests ==="
	@python3 tests/test_sprint7.py
	@echo "=== Lexer Tests ==="
	@python3 tests/test_runner.py
	@echo "=== Parser Tests ==="
	@python3 tests/parser/test_parser.py
	@echo "=== Semantic Tests ==="
	@python3 tests/semantic/run_tests.py

.PHONY: all install clean test-all
