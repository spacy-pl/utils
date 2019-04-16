import os
import click


def get_arg(line):
    return line.split(":")[1].strip()


@click.command(help="Get command used to generate selected dvc file")
@click.argument("dvc-filepath")
def restore_dvc_command(dvc_filepath):
    command_data = dict()
    command_data['filename'] = os.path.basename(dvc_filepath)
    command_data['deps'] = []
    command_data['outs'] = []

    with open(dvc_filepath, "r") as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]
    state = 'cmd'
    for line in lines:
        if line.startswith('cmd'):
            command_data['command'] = get_arg(line)
        elif line.startswith('deps'):
            state = 'deps'
        elif line.startswith('outs'):
            state = 'outs'
        elif line.startswith('path'):
            arg = get_arg(line)
            command_data[state].append(arg)

    command = "dvc run "
    command += f"-f {command_data['filename']} "
    for dep in command_data['deps']:
        command += f"-d {dep} "
    for out in command_data['outs']:
        command += f"-o {out} "
    command += command_data['command']
    print(command)


if __name__ == "__main__":
    restore_dvc_command()
