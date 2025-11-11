"""Test extras module functionality."""

import json
import tempfile
import textwrap
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest
import yaml

from dotenv_tools.extras import (
    DotenvExporter, DotenvTemplate, DotenvDiffer, ShellCompleter,
    format_diff_text
)
from dotenv_tools.parser import DotenvParser


class TestDotenvExporter:
    """Test DotenvExporter class."""
    
    def test_export_to_json(self, tmp_path):
        """Test exporting .env to JSON."""
        env_file = tmp_path / "test.env"
        env_file.write_text(textwrap.dedent("""
            # Test file
            APP_NAME=MyApp
            PORT=3000
            DATABASE_URL=postgres://localhost/db
        """).strip())
        
        exporter = DotenvExporter(env_file)
        json_output = exporter.export_to_json()
        
        result = json.loads(json_output)
        assert result["APP_NAME"] == "MyApp"
        assert result["PORT"] == "3000"
        assert result["DATABASE_URL"] == "postgres://localhost/db"
    
    def test_export_to_yaml(self, tmp_path):
        """Test exporting .env to YAML."""
        env_file = tmp_path / "test.env"
        env_file.write_text(textwrap.dedent("""
            # Test file
            APP_NAME=MyApp
            PORT=3000
            DEBUG=true
        """).strip())
        
        exporter = DotenvExporter(env_file)
        yaml_output = exporter.export_to_yaml()
        
        result = yaml.safe_load(yaml_output)
        assert result["APP_NAME"] == "MyApp"
        assert result["PORT"] == "3000"
        assert result["DEBUG"] == "true"


class TestDotenvTemplate:
    """Test DotenvTemplate class."""
    
    def test_generate_default_template(self):
        """Test generating default template."""
        template = DotenvTemplate.generate_template()
        
        assert "# Environment variables template" in template
        assert "APP_NAME=" in template
        assert "PORT=" in template
        assert "# Application name" in template
        assert 'APP_NAME="MyApplication"' in template
    
    def test_generate_custom_variables(self):
        """Test generating template with custom variables."""
        variables = ["CUSTOM_VAR1", "CUSTOM_VAR2"]
        template = DotenvTemplate.generate_template(variables=variables)
        
        assert "CUSTOM_VAR1=" in template
        assert "CUSTOM_VAR2=" in template
        assert "APP_NAME=" not in template  # Should not include default vars
    
    def test_generate_no_comments(self):
        """Test generating template without comments."""
        template = DotenvTemplate.generate_template(include_comments=False)
        
        assert "# Application name" not in template
        assert "APP_NAME=" in template
    
    def test_generate_no_examples(self):
        """Test generating template without example values."""
        template = DotenvTemplate.generate_template(include_examples=False)
        
        assert "APP_NAME=" in template
        assert 'APP_NAME="MyApplication"' not in template


class TestDotenvDiffer:
    """Test DotenvDiffer class."""
    
    def test_compare_files(self, tmp_path):
        """Test comparing two .env files."""
        file1 = tmp_path / "env1.env"
        file1.write_text("VAR1=value1\nVAR2=shared\n")
        
        file2 = tmp_path / "env2.env"
        file2.write_text("VAR2=shared\nVAR3=value3\n")
        
        differ = DotenvDiffer()
        result = differ.compare_files(file1, file2)
        
        assert result["common_variables"] == 1  # Only VAR2
        assert "VAR1" in result["only_in_file1"]
        assert "VAR3" in result["only_in_file2"]
        assert "VAR2" in result["same_values"]
    
    def test_compare_with_env(self, tmp_path, monkeypatch):
        """Test comparing .env file with environment."""
        env_file = tmp_path / "test.env"
        env_file.write_text("ENV_VAR1=value1\nENV_VAR2=file_value\n")
        
        # Mock environment variables
        monkeypatch.setenv("ENV_VAR2", "env_value")
        monkeypatch.setenv("ENV_ONLY", "env_only_value")
        
        differ = DotenvDiffer()
        result = differ.compare_with_env(env_file)
        
        assert "ENV_VAR1" in result["only_in_file"]
        assert result["only_in_file"]["ENV_VAR1"] == "value1"
        assert "ENV_VAR2" in result["different"]
        assert "ENV_ONLY" in result["only_in_env"]


class TestShellCompleter:
    """Test ShellCompleter class."""
    
    def test_generate_bash_completion(self):
        """Test generating bash completion script."""
        completer = ShellCompleter()
        script = completer.generate_bash_completion()
        
        assert "# Bash completion for dotenv-tools" in script
        assert "load-dotenv" in script
        assert "unload-dotenv" in script
        assert "set-dotenv" in script
        assert "complete -F" in script
    
    def test_generate_zsh_completion(self):
        """Test generating zsh completion script."""
        completer = ShellCompleter()
        script = completer.generate_zsh_completion()
        
        assert "# Zsh completion for dotenv-tools" in script
        assert "load-dotenv" in script
        assert "_dotenv_tools_commands" in script
    
    def test_generate_fish_completion(self):
        """Test generating fish completion script."""
        completer = ShellCompleter()
        script = completer.generate_fish_completion()
        
        assert "# Fish completion for dotenv-tools" in script
        assert "complete -c load-dotenv" in script
        assert "complete -c unload-dotenv" in script


class TestFormatDiffText:
    """Test format_diff_text function."""
    
    def test_format_file_comparison(self):
        """Test formatting file comparison results."""
        result = {
            "total_comparison": {
                "file1": 3,
                "file2": 2,
                "common": 1,
                "differences": 0
            },
            "only_in_file1": {"VAR1": "value1"},
            "only_in_file2": {},
            "same_values": {"VAR2": "shared"},
            "different_values": {}
        }
        
        output = format_diff_text(result)
        
        assert "File 1 variables: 3" in output
        assert "File 2 variables: 2" in output
        assert "Common variables: 1" in output
        assert "Only in file 1:" in output
        assert "VAR1 = value1" in output
    
    def test_format_env_comparison(self):
        """Test formatting environment comparison results."""
        result = {
            "summary": {
                "total_env_vars": 10,
                "total_file_vars": 3,
                "matching": 2,
                "differences": 1,
                "file_only": 0,
                "env_only": 7
            },
            "different": {
                "VAR1": {"env": "env_val", "file": "file_val"}
            }
        }
        
        output = format_diff_text(result)
        
        assert "Matching variables: 2" in output
        assert "Different values: 1" in output
        assert "VAR1:" in output
        assert "environment: env_val" in output
        assert ".env file: file_val" in output