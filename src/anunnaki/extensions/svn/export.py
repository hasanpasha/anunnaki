import subprocess


def export(url: str, output: str = None, force: bool = False) -> bool:
    args = ["svn", "export"]

    if force:
        args.append('--force')

    args.append(url)

    if output:
        args.append(output)

    process = subprocess.run(args=args, capture_output=True)

    return process.returncode == 0
