"""
Main entry point for the AI Agent
"""

import asyncio
import sys
from .cli import cli

def main():
    """Main entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
