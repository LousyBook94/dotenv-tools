#!/usr/bin/env python3
"""Simple test script to verify the new functionality works."""

import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

from dotenv_tools.extras import DotenvTemplate, DotenvExporter, DotenvDiffer, ShellCompleter

def test_template_generation():
    """Test template generation."""
    print("Testing template generation...")
    template = DotenvTemplate.generate_template()
    print("SUCCESS: Template generated successfully")
    print("First few lines:")
    for line in template.split('\n')[:5]:
        print(f"  {line}")
    return True

def test_exporter():
    """Test exporter functionality."""
    print("\nTesting exporter...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("TEST_VAR=test_value\nANOTHER_VAR=another_value\n")
        env_file = Path(f.name)
    
    try:
        exporter = DotenvExporter(env_file)
        json_output = exporter.export_to_json()
        print("SUCCESS: JSON export successful")
        print(f"JSON output:\n{json_output}")
        
        yaml_output = exporter.export_to_yaml()
        print("SUCCESS: YAML export successful")
        print(f"YAML output:\n{yaml_output}")
        return True
    finally:
        env_file.unlink()

def test_differ():
    """Test differ functionality."""
    print("\nTesting differ...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f1:
        f1.write("VAR1=value1\nSHARED=same\n")
        file1 = Path(f1.name)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f2:
        f2.write("VAR2=value2\nSHARED=same\n")
        file2 = Path(f2.name)
    
    try:
        differ = DotenvDiffer()
        result = differ.compare_files(file1, file2)
        print("SUCCESS: File comparison successful")
        print(f"Common variables: {result['common_variables']}")
        print(f"Only in file 1: {list(result['only_in_file1'].keys())}")
        print(f"Only in file 2: {list(result['only_in_file2'].keys())}")
        return True
    finally:
        file1.unlink()
        file2.unlink()

def test_completer():
    """Test shell completion generation."""
    print("\nTesting shell completion...")
    completer = ShellCompleter()
    
    bash_script = completer.generate_bash_completion()
    print("SUCCESS: Bash completion generated")
    print(f"Script length: {len(bash_script)} characters")
    
    zsh_script = completer.generate_zsh_completion()
    print("SUCCESS: Zsh completion generated")
    
    fish_script = completer.generate_fish_completion()
    print("SUCCESS: Fish completion generated")
    return True

if __name__ == "__main__":
    print("Testing dotenv-tools extra features...\n")
    
    try:
        test_template_generation()
        test_exporter()
        test_differ()
        test_completer()
        print("\nALL TESTS PASSED! The extra features are working correctly.")
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)