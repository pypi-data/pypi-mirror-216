import argparse
from weathon.utils.cli.download import DownloadCMD
from weathon.utils.cli.modelcard import ModelCardCMD
from weathon.utils.cli.pipeline import PipelineCMD
from weathon.utils.cli.plugins import PluginsCMD


def run_cmd():
    parser = argparse.ArgumentParser(
        'weathon Command Line tool', usage='weathon <command> [<args>]')
    subparsers = parser.add_subparsers(help='weathon commands helpers')

    DownloadCMD.define_args(subparsers)
    PluginsCMD.define_args(subparsers)
    PipelineCMD.define_args(subparsers)
    ModelCardCMD.define_args(subparsers)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        exit(1)

    cmd = args.func(args)
    cmd.execute()


if __name__ == '__main__':
    run_cmd()
