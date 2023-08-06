from argparse import ArgumentParser

from weathon.base.cli import CLICommand
from weathon.utils.hub.utils import snapshot_download


def subparser_func(args):
    """ Function which will be called for a specific sub parser.
    """
    return DownloadCMD(args)


class DownloadCMD(CLICommand):
    name = 'download'

    def __init__(self, args):
        self.args = args

    @staticmethod
    def define_args(parsers: ArgumentParser):
        """ define args for download command.
        """
        parser = parsers.add_parser(DownloadCMD.name)
        parser.add_argument(
            'model', type=str, help='Name of the model to be downloaded.')
        parser.add_argument(
            '--revision',
            type=str,
            default=None,
            help='Revision of the model.')
        parser.add_argument(
            '--cache_dir',
            type=str,
            default=None,
            help='Cache directory to save model.')
        parser.set_defaults(func=subparser_func)

    def execute(self):
        snapshot_download(
            self.args.model,
            cache_dir=self.args.cache_dir,
            revision=self.args.revision)
