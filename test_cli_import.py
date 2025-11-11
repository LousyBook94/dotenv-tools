#!/usr/bin/env python3
"""Test the CLI commands directly."""

import sys
sys.path.insert(0, 'src')

def test_cli_import():
    """Test if CLI can be imported."""
    try:
        from dotenv_tools.cli import cli
        print("CLI imported successfully")
        print(f"Commands available: {list(cli.commands.keys())}")
        return cli
    except Exception as e:
        print(f"CLI import failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_extras_import():
    """Test if extras can be imported."""
    try:
        from dotenv_tools.extras import (
            export_dotenv, generate_dotenv_template, compare_dotenv_files, 
            install_shell_completion, DotenvTemplate, DotenvDiffer, DotenvExporter
        )
        print("Extras imported successfully")
        return True
    except Exception as e:
        print(f"Extras import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing CLI and extras imports...\n")
    
    cli = test_cli_import()
    if cli:
        print("\nCLI commands:")
        for name, command in cli.commands.items():
            print(f"  - {name}: {command.help}")
    
    print("\nTesting extras imports...")
    test_extras_import()