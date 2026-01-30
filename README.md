# FandanGO - core plugin

[![OSV Scanner](https://github.com/FragmentScreen/fandanGO-core/actions/workflows/osv-scanner.yml/badge.svg)](https://github.com/FragmentScreen/fandanGO-core/actions/workflows/osv-scanner.yml)

This is the core plugin of the FandanGO application.

## How to deploy it

1. FandanGO uses conda package manager for installation. If you do not have conda already installed (run `which conda` in your console), install Miniconda as in example below (replace `/path/for/miniconda/` with the proper path):
   ```
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh -b -p /path/for/miniconda
   ```
   
   On a Mac you can use the command `brew install miniconda`


2. Make sure you are running bash shell (run `echo $SHELL` in your console), then initialize conda (replace `/path/for/miniconda/` with the proper path):
   ```
   source /path/for/miniconda/etc/profile.d/conda.sh
   ```

3. Create the conda environment:
   ```
   conda create --name fandanGO python=3.12
   ```

4. Activate environment and install the core (replace `/path/for/fandanGO-core` with the proper path):
   ```
   conda activate fandanGO
   git clone https://github.com/FragmentScreen/fandanGO-core.git
   pip install -e /path/for/fandanGO-core
   ```
   
   You will need to run `conda init SHELLNAME` prior to this, on Mac this is likely to be `conda init zsh`
   

5. Create a launcher file, let's call it "fandanGO", with the following content (replace `/path/for/miniconda/` with the proper path):
   ```
   #!/usr/bin/env python3
   import os
   import sys
   
   cmd = 'eval "$(/path/for/miniconda/bin/conda shell.bash hook)" && conda activate fandanGO && '
   cmd += "python -m core %s" % " ".join(sys.argv[1:])
   
   exit(os.WEXITSTATUS(os.system(cmd)))
   ```

5. Give execution permissions to it:
   ```
   chmod +x fandanGO
   ```

6. Create an alias for the FandanGO launcher in your `.bashrc` file (replace `/path/for/fandanGO` with the proper path):
   ```
   alias fandanGO='/path/for/fandanGO'
   ```

7. Play with FandangGO!💃:
   ```
   fandanGO --help
   ```

## Plugins

### How to install/uninstall a plugin

- Install:
   ```
   fandanGO install-plugin --plugin /path/to/fandanGO-plugin
   ```

- Uninstall:
   ```
   fandanGO uninstall-plugin --plugin fandanGO-plugin
   ```

### How to develop a new plugin

A FandanGO plugin should have:

1. The structure of a Python module installable by pip.
2. In the `setup.py` file, an entry point for `fandango.plugin` with the following structure:
   ```
   entry_points={
        'fandango.plugin': 'fandanGOPluginName = pythonModuleName'
    }
   ```
3. A `__init__.py` file with a `Plugin` class extending the `core.Plugin` class with the functions:
   - `define_args` (optional): for each action implemented in the plugin defines the parameters needed (furthermore the fandanGO project name)
   - `define_methods` (mandatory): for each action implemented in the plugin defines the method that will take care of it.

4. For integrity reasons, your plugin database should store the FandanGO project name as one of the table fields.

You can take as example the fandanGO-cryoem-cnb plugin placed at https://github.com/FragmentScreen/fandanGO-cryoem-cnb

## Security Scanning

This repo uses [OSV Scanner](https://github.com/google/osv-scanner) for vulnerability detection.

**When it runs:**
- Daily at 03:00 UTC (full scan)
- On PRs targeting main (changed deps only)
- On push to main (full scan)

**If vulnerabilities are found:**
1. Check the [Security tab](../../security) for alerts
2. To ignore false positives, add entries to `osv-scanner.toml`:
   ```toml
   [[IgnoredVulns]]
   id = "GHSA-xxxx-xxxx-xxxx"
   reason = "Justification"
   ```

**References:**
- [OSV Scanner docs](https://google.github.io/osv-scanner/)
- [GitHub Action](https://github.com/google/osv-scanner-action)
- [OSV Database](https://osv.dev/)
