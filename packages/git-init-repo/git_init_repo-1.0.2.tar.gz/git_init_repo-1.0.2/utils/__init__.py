import os
import shutil

def run_git() -> None:
    """Initializes a git repository in the current directory.

    Raises:
        FileNotFoundError: if git is not found in the system.
        RuntimeError: If git init fails.
    """
    if os.path.exists('.git'):
        print('Git repository already exists in the current directory.')
        return
    
    if shutil.which('git') is None:
        raise FileNotFoundError('Git not found in the system.')
    
    if os.system('git init') != 0:
        raise RuntimeError('Git init failed.')
    else:
        print('Git repository initialized in the current directory.')

def parse_args(args : list[str]) -> dict[str, str | bool]:
    """Parses arguments

    Args:
        args (list[str]): List of arguments.

    Raises:
        ValueError: Raised if no file is specified with option ``-f``.
        ValueError: Raised if no directory is specified with option ``-d`` or ``--dir``.

    Returns:
        dict[str, str | bool]: output dictionary of options.
    """
    try:
        output = {"filename": None, "vscode": False}
        for i in range(len(args)):
            if not args[i].startswith('-'):
                continue
            
            if args[i] == '-d' or args[i] == '--dir':
                if i + 1 >= len(args):
                    raise ValueError("No directory specified.")
                
                os.chdir(args[i + 1])
                args.pop(i + 1)
            
            elif args[i] == '-f':
                if i + 1 >= len(args):
                    raise ValueError("No file specified.")
                
                output['filename'] = args[i + 1]
                args.pop(i + 1)
            elif args[i] == '--vscode' or args[i] == '-vs':
                output['vscode'] = True
    except IndexError:
        pass
    return output