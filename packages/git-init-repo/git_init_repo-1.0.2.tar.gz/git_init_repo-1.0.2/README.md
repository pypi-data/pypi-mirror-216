# Repo init tool
Provides a Python Package to easliy initiate git repos for Python

## Installation
```bash
pip install git-init-repo
```

## Usage
```bash
python -m git_init_repo <language> [-vs] [-d <directory>] [-f <filename>]
```

- Option `-f` can be used to change the name of the `.gitignore` file if required.
- Option `-d` can be used to change the name of the directory in which the repo is to be initialized.
- Option `-vs` can be used to automatically configure VS Code tasks for the repo.

All language supported for `.gitignore` are the ones that can be requested from [gitignore.io](https://gitignore.io/).
Otherwise, only Python is supported for VS Code tasks.

## Contribution
Feel free to open an issue or a pull request if you want to contribute to this project.
If you can, please fork the project and make your changes in a separate branch before opening a pull request.