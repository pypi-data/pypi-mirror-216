import argparse

import colorama
import pkg_resources
import textwrap3
import platform

from jtech.project.create_project import CreateProject


def read_banner():
    banner_path = pkg_resources.resource_filename('jtech', 'resources/banner/banner.txt')
    with open(banner_path, 'r') as file:
        banner = file.read()
    return banner


def get_linux_distribution():
    with open('/etc/os-release', 'r') as f:
        lines = f.readlines()

    dist_info = {}
    for line in lines:
        key, value = line.strip().split('=')
        dist_info[key] = value.strip('"')

    return dist_info.get('NAME'), dist_info.get('VERSION')


def print_info_system(version_cli):
    system = platform.system()
    release = platform.release()
    machine = platform.machine()

    linux_distribution, linux_version = get_linux_distribution()

    print("System Information:")
    print("-------------------")
    print(f"System:         {system}")
    print(f"Distribution:   {linux_distribution}")
    print(f"Version:        {linux_version}")
    print(f"Release:        {release}")
    print(f"Machine:        {machine}")
    print(f"CLI:            {version_cli}")


def main():
    colorama.init()

    banner = read_banner()
    banner = banner.replace('${Ansi.GREEN}', colorama.Fore.GREEN)
    banner = banner.replace('${Ansi.RED}', colorama.Fore.RED)
    banner = banner.replace('${Ansi.DEFAULT}', colorama.Style.RESET_ALL)

    version = pkg_resources.require("jtech")[0].version
    banner = banner.replace("{}", version)
    print(textwrap3.fill(banner))

    parser = argparse.ArgumentParser()

    parser.add_argument('--version', action='store_true', help='Show version')

    parser.add_argument("--create", action='store_true', help='Create a Spring Boot Project')

    parser.add_argument("project_name", nargs='?', help='Name of the project to be created. Ex: jtech --create sansys-sample')

    vargs = parser.parse_args()

    if vargs.create:
        project = CreateProject()
        if vargs.project_name:
            project.create(vargs.project_name)
        else:
            project.create()

    elif vargs.version:
        print_info_system(version)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
