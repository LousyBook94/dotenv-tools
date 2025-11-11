# Changelog 📝✨

All notable changes to this project will be documented in this file (because we care about transparency! 💖).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) 📚,
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) 🎯.

## [0.0.2] - 2025-11-10 🎉

### Added (Roadmap Features Implemented!) ✨

#### Advanced Features (All Roadmap Items Complete!) 🚀
- **Shell auto-completion support** 🐚:
  - `shell-completion` command with bash, zsh, and fish support
  - Auto-installation capabilities with manual configuration instructions
  - Full command and option completion for all dotenv-tools commands

- **Environment diffing command** ⚖️:
  - `compare-env` command to compare .env files or with current environment
  - Text and JSON output formats
  - Detailed comparison showing common, different, and unique variables
  - Save comparison results to file

- **Template generation** 📝:
  - `generate-template` command for creating .env templates
  - Customizable variable lists
  - Include/exclude comments and example values
  - Built-in help text and example values for common variables

- **YAML/JSON export functionality** 📊:
  - `export-dotenv` command supporting JSON and YAML formats
  - Preserves variable values and structure
  - Output to stdout or file
  - Auto-discovery of .env files

#### New CLI Commands 🎮
- `export-dotenv` - Export .env files to JSON/YAML format
- `generate-template` - Generate .env template files
- `compare-env` - Compare .env files or environments
- `shell-completion` - Generate/install shell completion scripts

#### Technical Improvements 🛠️
- Added PyYAML dependency for YAML support
- Enhanced project scripts in pyproject.toml
- Comprehensive test coverage for new features
- Updated documentation with all new commands

## [Unreleased] 🚀

### Planned (Future Enhancements) 🌟
- Multiple file loading support 📁
- Environment variable validation
- Integration with popular frameworks
- Windows PowerShell completion
- Docker container support

## [0.0.1] - 2025-11-10 🎊

### Added (So Many Cool Things!) ✨

#### Core Functionality 💪
- Full support for all assignment operators (yay! 🎉):
  - `=` - Standard assignment 📝
  - `:=` - Immediate expansion (Makefile-style) ⚡
  - `+=` - Append to existing variable ➕
  - `?=` - Conditional assignment (only if unset) ❓✨

- Comprehensive variable expansion (how awesome! 🔄):
  - `${VAR}` - Basic expansion from environment 🌐
  - `${VAR:-default}` - Use default if unset (no assignment) 🎁
  - `${VAR:=default}` - Assign default if unset, then use it 💎
  - `${VAR:+alt}` - Use alternate value if set 🔆

- Environment variable tracking (super smart! 🧠):
  - Track loaded variables for proper unloading 👀
  - Persist state across CLI invocations 💾
  - Safe unloading of only loaded variables 🛡️

- File parsing (so flexible! 🎨):
  - Comment support (`#` and inline) 💬
  - Quoted value support (single and double quotes) "🗣️"
  - Escape sequence processing in double quotes 🔤
  - Multiline value support 📏
  - Export prefix support (`export KEY=value`) 🚀
  - Empty value handling 🕳️

#### CLI Commands 🎮
- `load-dotenv` command (loading made easy! 📥):
  - Auto-discover .env files from current directory or parents 🔍
  - Load from specific file path 📂
  - `--override` flag to force override existing variables 🔄
  - `--verbose` flag for detailed output 📢
  - `--state-file` option to customize state file location 📍

- `unload-dotenv` command (clean up time! 🧹):
  - Remove all tracked environment variables 🗑️
  - `--verbose` flag for detailed output 📢
  - `--force` flag to skip confirmation prompt ⚡
  - `--state-file` option to customize state file location 📍

- `set-dotenv` command (editing made fun! ✏️🎉):
  - Set individual variables: `set-dotenv KEY VALUE` or `set-dotenv KEY=VALUE` 🎯
  - Remove variables: `set-dotenv --remove KEY` 🗑️
  - List all variables: `set-dotenv --list` 📋
  - Edit .env file: `set-dotenv --edit` 📝
  - `--operator` flag to choose assignment operator (=, :=, +=, ?=) 🎛️
  - `--file` option to work with custom .env files 📂
  - `--editor` option to specify custom editor ✨
  - Auto-creates .env file if it doesn't exist (how thoughtful! 💖)
  - Infers operator from `KEY=VALUE` format (so smart! 🧠)

#### Testing (We've Got You Covered!) 🧪✅
- Comprehensive test suite with 100% coverage (so thorough! ✨):
  - Parser tests (test_parser.py) 📝
  - Expansion tests (test_expansion.py) 🔄
  - Tracker tests (test_tracker.py) 📊
  - Core tests (test_core.py) 💪
  - CLI tests (test_cli.py) 🎮

#### Documentation (We've Thought of Everything!) 📚💖
- README.md with (your starting point! 🚀):
  - Project overview 🌟
  - Quick start guide ⚡
  - Feature highlights 🎨
  - Installation instructions 📦
  - Basic usage examples 💡

- USAGE.md with (your complete guide! 📖):
  - Complete command reference 🎛️
  - Detailed syntax documentation 📋
  - Assignment operator explanations 🎯
  - Variable expansion guide 🔄
  - Real-world examples 💼
  - Integration guides (Shell, Python, Makefile, Docker) 🔗
  - Troubleshooting section 🛠️
  - FAQ ❓

#### Packaging (Modern & Clean!) 📦🎨
- Modern packaging with pyproject.toml ⚙️
- Entry points for CLI commands (load-dotenv, unload-dotenv, set-dotenv) 🎯
- Package renamed from `load-dotenv` to `dotenv-tools` ✨
- Comprehensive metadata 📋
- Development dependencies configuration 🔧
- Python 3.8+ support 🐍
- MIT License (super permissive! ⚖️)

#### Build System (Ready to Go!) 🏗️🚀
- Hatchling build backend 🛠️
- Source and wheel distribution support 📦
- Twine upload configuration ☁️
- GitHub repository ready 🌟

### Technical Details (For the Curious!) 🧠💻
- **Parser:** Custom regex-based parser supporting all operators 🔍
- **Expansion Engine:** Recursive variable substitution with circular reference detection 🔄🛡️
- **Tracker:** JSON-based state persistence with restrictive file permissions 💾🔐
- **SetDotenv:** Class for setting, updating, and removing variables in .env files ✏️
- **CLI Framework:** Click for professional command-line interface 🎨
- **Dependencies:** Only Click (click>=8.0.0) 🎯
- **Python Compatibility:** 3.8, 3.9, 3.10, 3.11, 3.12 🐍

### Author (That's Me!) ✍️😊
- LousyBook01 (GitHub: [@LousyBook94](https://github.com/LousyBook94)) 💖

---

## Version History 📜

- **0.0.1** - Initial release with full feature set (load, unload, set, edit, list, remove) 🎉✨

---

## Support (We're Here to Help!) 💪🤝

For issues or questions, visit (don't be shy! 😊):
- GitHub: https://github.com/LousyBook94/load-dotenv 🏠
- Issues: https://github.com/LousyBook94/load-dotenv/issues 🐛💬
