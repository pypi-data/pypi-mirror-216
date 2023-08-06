# flake8: noqa
import sys

try:
    from blockit.__main__ import main
except:
    sys.exit(1)

sys.exit(0)
