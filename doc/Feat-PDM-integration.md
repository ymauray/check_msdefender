# PDM Integration Specification

## Overview

This specification outlines the integration of PDM (Python Dependency Management) into the check_msdefender project to streamline development workflow and package publishing.

## PDM Integration Benefits

- Simplified dependency management with lock files
- Virtual environment management
- Simplified build and publish workflow
- Better development experience with standardized commands

## Development Workflow

### Setup
```bash
pdm install
```

### Code Quality Checks
```bash
# Format code
pdm run format
black .

# Type checking
pdm run typecheck
mypy check_msdefender/

# Linting
pdm run lint
flake8 check_msdefender/
```

### Build and Publish

#### Build Package
```bash
pdm run build
python -m build
```

#### Publish to PyPI
```bash
pdm run publish
python -m twine upload dist/* --verbose
```

## PDM Configuration

The project should include a `pyproject.toml` file with PDM configuration including:

- Project dependencies
- Development dependencies
- Build system configuration
- Script definitions for common tasks

## Scripts Definition

The following scripts should be defined in `pyproject.toml`:

```toml
[tool.pdm.scripts]
format = "black ."
typecheck = "mypy check_msdefender/"
lint = "flake8 check_msdefender/"
build = "python -m build"
publish = "python -m twine upload dist/* --verbose"
test = "pytest -v tests/"
all = {composite = ["format", "typecheck", ...]}

```

## Migration Steps

1. Add PDM configuration to `pyproject.toml`
2. Define project dependencies and dev dependencies
3. Create PDM scripts for common tasks
4. Update documentation to use PDM commands
5. Ensure CI/CD pipelines use PDM workflows

## Standard Commands

### Additional scripts check_msdefender 
```toml
[tool.pdm.scripts]
msdhelp = "check_msdefender --help"
msdmachines = "check_msdefender machines"
msdlastseen = "check_msdefender lastseen -d $MACHINE"
msddetail = "check_msdefender detail -d $MACHINE"
msdalerts = "check_msdefender alerts -d $MACHINE"
msdvulnerabilities = "check_msdefender vulnerabilities -d $MACHINE"
msdonboarding = "check_msdefender onboarding -d $MACHINE"
msdall = {composite = ["msdhelp", "msdmachines", ...]}

```

## Benefits for Contributors

- Single command setup: `pdm install`
- Consistent environment across developers
- Simplified command interface
- Automatic dependency resolution and locking