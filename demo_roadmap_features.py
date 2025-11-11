#!/usr/bin/env python3
"""Demo script showing all the new roadmap features working."""

import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

from dotenv_tools.extras import (
    DotenvTemplate, DotenvExporter, DotenvDiffer, ShellCompleter,
    format_diff_text
)

def demo_template_generation():
    """Demo template generation feature."""
    print("=" * 60)
    print("DEMO: Template Generation")
    print("=" * 60)
    
    # Generate default template
    template = DotenvTemplate.generate_template()
    print("Generated default template:")
    print(template)
    print()
    
    # Generate custom template
    custom_template = DotenvTemplate.generate_template(
        variables=["APP_NAME", "PORT", "DATABASE_URL"],
        include_comments=True,
        include_examples=False
    )
    print("Generated custom template (no examples):")
    print(custom_template)

def demo_export_functionality():
    """Demo export functionality."""
    print("=" * 60)
    print("DEMO: Export Functionality")
    print("=" * 60)
    
    # Create sample .env file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("""# Sample environment file
APP_NAME=MyAwesomeApp
ENVIRONMENT=development
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost/mydb
API_KEY=sk-1234567890abcdef
DEBUG=true
""")
        env_file = Path(f.name)
    
    try:
        exporter = DotenvExporter(env_file)
        
        print("Original .env file content:")
        print(env_file.read_text())
        print()
        
        print("Exported to JSON:")
        json_export = exporter.export_to_json()
        print(json_export)
        print()
        
        print("Exported to YAML:")
        yaml_export = exporter.export_to_yaml()
        print(yaml_export)
        
    finally:
        env_file.unlink()

def demo_environment_diffing():
    """Demo environment diffing feature."""
    print("=" * 60)
    print("DEMO: Environment Diffing")
    print("=" * 60)
    
    # Create two sample .env files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f1:
        f1.write("SHARED_VAR=common_value\nDEV_ONLY=development\nAPI_URL=https://dev.api.com\n")
        file1 = Path(f1.name)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f2:
        f2.write("SHARED_VAR=common_value\nPROD_ONLY=production\nAPI_URL=https://prod.api.com\n")
        file2 = Path(f2.name)
    
    try:
        differ = DotenvDiffer()
        result = differ.compare_files(file1, file2)
        
        print("Comparison result:")
        print(format_diff_text(result))
        print()
        
        print("Raw comparison data:")
        print(f"Common variables: {result['common_variables']}")
        print(f"Only in file 1: {result['only_in_file1']}")
        print(f"Only in file 2: {result['only_in_file2']}")
        print(f"Same values: {result['same_values']}")
        print(f"Different values: {result['different_values']}")
        
    finally:
        file1.unlink()
        file2.unlink()

def demo_shell_completion():
    """Demo shell completion generation."""
    print("=" * 60)
    print("DEMO: Shell Completion Generation")
    print("=" * 60)
    
    completer = ShellCompleter()
    
    print("Bash completion script (first 20 lines):")
    bash_script = completer.generate_bash_completion()
    for i, line in enumerate(bash_script.split('\n')[:20]):
        print(f"{i+1:2d}: {line}")
    if len(bash_script.split('\n')) > 20:
        print("    ... (truncated)")
    print()
    
    print("Zsh completion script (first 10 lines):")
    zsh_script = completer.generate_zsh_completion()
    for i, line in enumerate(zsh_script.split('\n')[:10]):
        print(f"{i+1:2d}: {line}")
    if len(zsh_script.split('\n')) > 10:
        print("    ... (truncated)")
    print()
    
    print("Fish completion script (first 10 lines):")
    fish_script = completer.generate_fish_completion()
    for i, line in enumerate(fish_script.split('\n')[:10]):
        print(f"{i+1:2d}: {line}")
    if len(fish_script.split('\n')) > 10:
        print("    ... (truncated)")

if __name__ == "__main__":
    print("Dotenv-Tools Roadmap Features Demo")
    print("=" * 60)
    print("Demonstrating all implemented roadmap features:")
    print("* Auto-completion for shell integration")
    print("* .env template generation")
    print("* Environment diffing")
    print("* YAML/JSON export support")
    print("=" * 60)
    print()
    
    try:
        demo_template_generation()
        print()
        demo_export_functionality()
        print()
        demo_environment_diffing()
        print()
        demo_shell_completion()
        
        print("=" * 60)
        print("ALL ROADMAP FEATURES HAVE BEEN SUCCESSFULLY IMPLEMENTED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)