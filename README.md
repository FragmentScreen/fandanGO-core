# FandanGO - core plugin

This is the core plugin of the FandanGO application.

## How to deploy it

1. FandanGO uses conda package manager for installation. If you do not have conda already installed (run `which conda` in your console), install Miniconda as in example below (replace `/path/for/miniconda/` with the proper path):
   ```
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh -b -p /path/for/miniconda
   ```

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
   git clone https://github.com/I2PC/fandanGO-core.git
   pip install -e /path/for/fandanGO-core
   ```
   
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
   fandanGO installpl -p /path/to/fandanGO-plugin
   ```

- Uninstall:
   ```
   fandanGO uninstallpl -p fandanGO-plugin
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
3. A `__init.py__` file with a `Plugin` class extending the `core.Plugin` class with the functions:
   - `define_args` (optional): for each action implemented in the plugin defines the parameters needed (extending the basic ones described in the core `Plugin` class)
   - `define_methods` (mandatory): for each action implemented in the plugin defines the method that will take care of it.

4. Each of the methods described in the `define_methods` function should return a dictionary with the `success` key with the value `True` or `False` depending on whether the action went well or not.
5. For integrity reasons, your plugin database should store the FandanGO project name as one of the table fields.

You can take as example the fandanGO-template plugin placed at https://github.com/I2PC/fandanGO-template
