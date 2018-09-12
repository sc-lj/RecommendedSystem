#coding:utf-8

"""Helper file for running the async data generation process in OSS."""

import os
import sys


_PYTHON = sys.executable
if not _PYTHON:
  raise RuntimeError("Could not find path to Python interpreter in order to "
                     "spawn subprocesses.")

_ASYNC_GEN_PATH = os.path.join(os.path.dirname(__file__),
                               "data_async_generation.py")

INVOCATION = [_PYTHON, _ASYNC_GEN_PATH]
