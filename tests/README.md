# Cheat Sheet

Run tests:

```bash
./build_and_test.sh
```

Run a specific test:

```bash
./build_and_test.sh -k test_foo
```

Run all tests in a specific file:

```bash
./build_and_test.sh tests/test_rag.py
```

# Overview
We use `pytest`. We have two categories of tests:

1. Unit tests:
   These run locally on your own machine.

2. Integration tests: These install Open RAG and test it by connecting external services like ChatGPT, AWS Bedrock, etc.
   You need the credentials of these services for these tests.

Right now both kinds of tests are bundled together. We should probably make it easier
to run each kind of test separately.

# Requirements:
1.
