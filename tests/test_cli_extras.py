"""Test CLI commands for extras functionality."""

import json
import tempfile
import textwrap
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest
from click.testing import CliRunner

from dotenv_tools.cli import cli
from dotenv_tools.extras import DotenvTemplate, DotenvDiffer


class TestExportCommand:
    """Test export-dotenv command."""
    
    def test_export_json_default_file(self, tmp_path):
        """Test exporting JSON with auto-discovered file."""
        env_file = tmp_path / ".env"
        env_file.write_text("APP_NAME=TestApp\nPORT=8080\n")
        
        runner = CliRunner()
        result = runner.invoke(cli, ['export-dotenv', '--format', 'json'])
        
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["APP_NAME"] == "TestApp"
        assert data["PORT"] == "8080"
    
    def test_export_json_specific_file(self, tmp_path):
        """Test exporting JSON with specific file."""
        env_file = tmp_path / "custom.env"
        env_file.write_text("CUSTOM_VAR=test\n")
        
        runner = CliRunner()
        result = runner.invoke(cli, ['export-dotenv', '--format', 'json', str(env_file)])
        
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["CUSTOM_VAR"] == "test"
    
    def test_export_yaml(self, tmp_path):
        """Test exporting YAML format."""
        env_file = tmp_path / "test.env"
        env_file.write_text("YAML_TEST=value\n")
        
        runner = CliRunner()
        result = runner.invoke(cli, ['export-dotenv', '--format', 'yaml'])
        
        assert result.exit_code == 0
        assert "YAML_TEST: value" in result.output
    
    def test_export_to_file(self, tmp_path):
        """Test exporting to output file."""
        env_file = tmp_path / "test.env"
        env_file.write_text("OUTPUT_TEST=data\n")
        
        output_file = tmp_path / "output.json"
        
        runner = CliRunner()
        result = runner.invoke(cli, [
            'export-dotenv', 
            '--format', 'json',
            '--output', str(output_file)
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
        
        with open(output_file) as f:
            data = json.load(f)
            assert data["OUTPUT_TEST"] == "data"
    
    def test_export_file_not_found(self):
        """Test exporting non-existent file."""
        runner = CliRunner()
        result = runner.invoke(cli, ['export-dotenv', '--format', 'json', 'nonexistent.env'])
        
        assert result.exit_code != 0
        assert "File not found" in result.output


class TestGenerateTemplateCommand:
    """Test generate-template command."""
    
    def test_generate_default_template(self):
        """Test generating default template."""
        runner = CliRunner()
        result = runner.invoke(cli, ['generate-template'])
        
        assert result.exit_code == 0
        assert "# Environment variables template" in result.output
        assert "APP_NAME=" in result.output
        assert 'APP_NAME="MyApplication"' in result.output
    
    def test_generate_custom_variables(self):
        """Test generating template with custom variables."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'generate-template',
            '--variables', 'CUSTOM1',
            '--variables', 'CUSTOM2'
        ])
        
        assert result.exit_code == 0
        assert "CUSTOM1=" in result.output
        assert "CUSTOM2=" in result.output
        assert "APP_NAME=" not in result.output
    
    def test_generate_no_comments(self):
        """Test generating template without comments."""
        runner = CliRunner()
        result = runner.invoke(cli, ['generate-template', '--no-comments'])
        
        assert result.exit_code == 0
        assert "APP_NAME=" in result.output
        assert "# Application name" not in result.output
    
    def test_generate_no_examples(self):
        """Test generating template without examples."""
        runner = CliRunner()
        result = runner.invoke(cli, ['generate-template', '--no-examples'])
        
        assert result.exit_code == 0
        assert "APP_NAME=" in result.output
        assert 'APP_NAME="MyApplication"' not in result.output
    
    def test_generate_to_file(self, tmp_path):
        """Test generating template to file."""
        output_file = tmp_path / "template.env"
        
        runner = CliRunner()
        result = runner.invoke(cli, [
            'generate-template',
            '--output', str(output_file)
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "# Environment variables template" in content
        assert "APP_NAME=" in content


class TestCompareCommand:
    """Test compare-env command."""
    
    def test_compare_two_files(self, tmp_path):
        """Test comparing two .env files."""
        file1 = tmp_path / "env1.env"
        file1.write_text("VAR1=value1\nSHARED=common\n")
        
        file2 = tmp_path / "env2.env"
        file2.write_text("VAR2=value2\nSHARED=common\n")
        
        runner = CliRunner()
        result = runner.invoke(cli, [
            'compare-env', 
            str(file1), 
            str(file2)
        ])
        
        assert result.exit_code == 0
        assert "File 1 variables: 2" in result.output
        assert "File 2 variables: 2" in result.output
        assert "Only in file 1:" in result.output
        assert "VAR1 = value1" in result.output
    
    def test_compare_with_env(self, tmp_path, monkeypatch):
        """Test comparing .env file with environment."""
        env_file = tmp_path / "test.env"
        env_file.write_text("FILE_VAR=file_value\n")
        
        monkeypatch.setenv("FILE_VAR", "env_value")
        monkeypatch.setenv("ENV_ONLY", "env_only")
        
        runner = CliRunner()
        result = runner.invoke(cli, [
            'compare-env', 
            str(env_file), 
            '--env'
        ])
        
        assert result.exit_code == 0
        assert "Different values:" in result.output
        assert "FILE_VAR:" in result.output
    
    def test_compare_json_output(self, tmp_path):
        """Test comparing with JSON output format."""
        file1 = tmp_path / "env1.env"
        file1.write_text("TEST=value\n")
        
        file2 = tmp_path / "env2.env" 
        file2.write_text("TEST=different\n")
        
        runner = CliRunner()
        result = runner.invoke(cli, [
            'compare-env',
            str(file1),
            str(file2),
            '--format', 'json'
        ])
        
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "different_values" in data
        assert "TEST" in data["different_values"]
    
    def test_compare_to_file(self, tmp_path):
        """Test saving comparison to file."""
        file1 = tmp_path / "env1.env"
        file1.write_text("VAR1=value1\n")
        
        file2 = tmp_path / "env2.env"
        file2.write_text("VAR1=value1\n")
        
        output_file = tmp_path / "comparison.txt"
        
        runner = CliRunner()
        result = runner.invoke(cli, [
            'compare-env',
            str(file1),
            str(file2),
            '--output', str(output_file)
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "File 1 variables: 1" in content
    
    def test_compare_missing_file2(self):
        """Test compare with missing second file."""
        file1 = Path("nonexistent1.env")
        
        runner = CliRunner()
        result = runner.invoke(cli, [
            'compare-env',
            str(file1),
            "nonexistent2.env"
        ])
        
        assert result.exit_code != 0
    
    def test_compare_with_both_env_and_file2(self):
        """Test compare with both --env and FILE2 (should error)."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'compare-env',
            'test.env',
            'test2.env',
            '--env'
        ])
        
        assert result.exit_code != 0
        assert "Cannot specify both --env and FILE2" in result.output


class TestShellCompletionCommand:
    """Test shell-completion command."""
    
    def test_generate_bash_completion(self):
        """Test generating bash completion script."""
        runner = CliRunner()
        result = runner.invoke(cli, ['shell-completion', 'bash'])
        
        assert result.exit_code == 0
        assert "# Bash completion for dotenv-tools" in result.output
        assert "load-dotenv" in result.output
        assert "complete -F" in result.output
    
    def test_generate_zsh_completion(self):
        """Test generating zsh completion script."""
        runner = CliRunner()
        result = runner.invoke(cli, ['shell-completion', 'zsh'])
        
        assert result.exit_code == 0
        assert "# Zsh completion for dotenv-tools" in result.output
        assert "_dotenv_tools_commands" in result.output
    
    def test_generate_fish_completion(self):
        """Test generating fish completion script."""
        runner = CliRunner()
        result = runner.invoke(cli, ['shell-completion', 'fish'])
        
        assert result.exit_code == 0
        assert "# Fish completion for dotenv-tools" in result.output
        assert "complete -c load-dotenv" in result.output
    
    def test_generate_to_file(self, tmp_path):
        """Test generating completion to file."""
        output_file = tmp_path / "completion.bash"
        
        runner = CliRunner()
        result = runner.invoke(cli, [
            'shell-completion',
            'bash',
            '--output', str(output_file)
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "# Bash completion for dotenv-tools" in content
    
    def test_invalid_shell(self):
        """Test with invalid shell type."""
        runner = CliRunner()
        result = runner.invoke(cli, ['shell-completion', 'invalid-shell'])
        
        assert result.exit_code != 0
        assert "Unsupported shell" in result.output
    
    def test_case_insensitive_shell(self):
        """Test shell name is case insensitive."""
        runner = CliRunner()
        result = runner.invoke(cli, ['shell-completion', 'BASH'])
        
        assert result.exit_code == 0
        assert "# Bash completion for dotenv-tools" in result.output