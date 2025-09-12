"""Main entry point for check_msdefender Nagios plugin."""

import sys
from check_msdefender.cli import main

if __name__ == "__main__":
    sys.exit(main())