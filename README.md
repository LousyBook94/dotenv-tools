# dotenv-tools 🌟✨

A super duper comprehensive CLI tool to **load, unload, and manage** environment variables in `.env` files with **complete syntax support**! 🎉💖

> *Your friendly companion for all things dotenv!* 😄👍

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with ❤️](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F-red.svg)](https://github.com/LousyBook94)

## Features 🎨🎊

✅ **All Assignment Operators**: `=`, `:=`, `+=`, `?=` 🎯  \
✅ **Variable Expansion**: `${VAR}`, `${VAR:-default}`, `${VAR:=default}`, `${VAR:+alt}` 🔄  \
✅ **Shell Export Support**: `export KEY=value` 🚀  \
✅ **Smart Parsing**: Comments, quotes, escapes, multiline values 🧠✨  \
✅ **Load/Unload**: Load variables and easily remove them later 🔃💫  \
✅ **Set/Edit/Remove**: Manage .env files directly from command line ✏️🎨  \
✅ **Flexible**: Load from any path or auto-discover `.env files` 🔍🗺️  \
✅ **Cross-Platform**: Works on Windows, macOS, and Linux 🌍💻  \

## Quick Start 🚀💨

### Installation 📦✨

Install from PyPI (super easy!):

```bash
pip install dotenv-tools
```

Or install from source (for the adventurous!):

```bash
git clone https://github.com/LousyBook94/load-dotenv.git
cd load-dotenv
pip install -e .
```

### Basic Usage 🎮🎉

**Load from `.env` in current directory** 🌟:

```bash
load-dotenv
```

**Load from a specific file** 📁:

```bash
load-dotenv /path/to/my-custom.env
```

**Unload all loaded variables** 🧹💨:

```bash
unload-dotenv
```

**Set a variable in .env** ✏️✨:

```bash
set-dotenv PORT 3000
set-dotenv API_KEY=secret123
```

**Remove a variable** ❌🗑️:

```bash
set-dotenv --remove API_KEY
```

**List all variables** 📋👀:

```bash
set-dotenv --list
```

**Edit .env file** 📝🎨:

```bash
set-dotenv --edit
```

**Verbose output** 🔍📢:

```bash
load-dotenv --verbose
set-dotenv --verbose --list
```

## Assignment Operators 🎯🔧

This tool supports all major assignment operators (and they're all super cool!):

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Standard assignment | `KEY=value` 📝 |
| `:=` | Immediate expansion | `PATH:=$PATH:/new/path` ⚡ |
| `+=` | Append to existing | `PATH+=/additional/path` ➕ |
| `?=` | Conditional assignment | `API_KEY?=${DEFAULT_KEY}` ❓✨ |

## Variable Expansion 🔄🎨

Full support for variable expansion syntax (how awesome is that?!):

| Syntax | Description | Example |
|--------|-------------|---------|
| `${VAR}` | Expand from environment | `GREETING=${USER}` 🌐 |
| `${VAR:-default}` | Use default if unset | `PORT=${PORT:-8080}` 🎁 |
| `${VAR:=default}` | Assign default if unset | `DB_NAME:=mydb` 💎 |
| `${VAR:+alt}` | Use alternate if set | `DEBUG=${DEBUG:+1}` 🔆 |

## Examples 📚🎊

### Example `.env` file 📄✨

```bash
# Database configuration 🗄️
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydatabase
DB_USER=admin
DB_PASS=secret123

# Application settings 🎨
APP_NAME=MyApp
APP_ENV=development
DEBUG=true

# Variable expansion 🔄
APP_URL=http://${DB_HOST}:${PORT}

# Conditional assignment (only set if not already set) ❓
API_KEY?=${DEFAULT_API_KEY}

# Append to existing ➕
PATH+=/opt/myapp/bin

# Immediate expansion ⚡
FULL_PATH:=${HOME}/myapp/data
```

### Using with Commands 💻🎮

**Set variables directly** ✨:

```bash
# Set individual variables 🎯
set-dotenv PORT 3000
set-dotenv API_KEY=secret123

# List all variables in .env 📋
set-dotenv --list

# Remove a variable 🗑️
set-dotenv --remove OLD_KEY

# Edit .env file 📝
set-dotenv --edit
```

**Load and unload environment** 🔃:

```bash
# Load environment 🌟
load-dotenv

# Check if variables are loaded 👀
echo $DB_HOST  # outputs: localhost

# Unload when done 🧹
unload-dotenv
```

## Use Cases 💡🎯

### Development Workflow 🚀💻

**Set up your environment** 🎉:

```bash
# Add variables to .env ✨
set-dotenv PORT 3000
set-dotenv DATABASE_URL=postgres://localhost/mydb

# Load and use 🚀
load-dotenv
python app.py

# Clean up 🧹
unload-dotenv
```

**Managing multiple environments** 🌈:

```bash
# Development 🌱
set-dotenv --file .env.development DEBUG=true
load-dotenv .env.development

# Production 🏭
set-dotenv --file .env.production DEBUG=false
load-dotenv .env.production
```

### CI/CD Pipelines 🔄🏗️

```bash
# Load environment for testing 🧪
load-dotenv --verbose

# Run tests ✨
pytest tests/

# Unload after tests 🧹
unload-dotenv --force
```

### Docker/Shells 🐳💻

Load environment in your shell (how cool is that?!):

```bash
# Add to ~/.bashrc or ~/.zshrc
load-dotenv() {
    python -m dotenv_tools.cli load-dotenv "$@"
}

unload-dotenv() {
    python -m dotenv_tools.cli unload-dotenv "$@"
}
```

## Documentation 📚🔍

For complete documentation, see **[USAGE.md](USAGE.md)** (it's absolutely amazing!):

- Detailed syntax reference 📖
- All command-line options 🎛️
- Advanced examples 💡
- Troubleshooting guide 🛠️

## Requirements 📦✨

- Python 3.8 or higher 🐍
- `click` package (automatically installed) 💖

## Installation from Source 💻⚙️

```bash
git clone https://github.com/LousyBook94/load-dotenv.git
cd load-dotenv

# Install in development mode 🔧
pip install -e .

# Or build and install 🏗️
pip install .
```

## Running Tests 🧪✅

```bash
# Install test dependencies 💾
pip install -e .[dev]

# Run tests ✨
pytest

# Run with coverage 📊
pytest --cov=src/load_dotenv
```

## Building for Distribution 🚀📦

```bash
# Build source and wheel distributions 🏭
python -m build

# Upload to PyPI (requires twine) ☁️
python -m twine upload dist/*
```

## License 📄⚖️

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (super permissive and awesome!).

## Author ✍️💖

**LousyBook01** - [@LousyBook94](https://github.com/LousyBook94) (that's me! 😊)

## Contributing 🤝🌟

Contributions are welcome! Please feel free to submit a Pull Request (let's make this even more amazing together! 🎉).

## Roadmap 🗺️🚀

- [ ] Auto-completion for shell integration 🐚
- [ ] .env template generation 📝
- [ ] Environment diffing ⚖️
- [ ] YAML/JSON export support 📊

## Issues 🐛💬

If you encounter any issues or have questions, please file an issue on [GitHub](https://github.com/LousyBook94/load-dotenv/issues) (we're here to help! 💪😊)
