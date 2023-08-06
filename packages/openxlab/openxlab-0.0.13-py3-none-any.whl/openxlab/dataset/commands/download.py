import os

from tqdm import tqdm

from openxlab.dataset.commands.utility import ContextInfo
from openxlab.dataset.constants import FILE_THRESHOLD
from openxlab.dataset.io import downloader
from openxlab.types.command_type import *


class Download(BaseCommand):
    """This command is designed to handle single file
    or subset download of a given dataset.

    """
    def get_name(self) -> str:
        return "download"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--dataset_repo_name",
            "-n",
            type=str,
            required=True,
            help=(
                "The dataset repo you want to download file from."
            ),
        )
        parser.add_argument(
            "--source_path",
            "-s",
            type=str,
            required=True,
            help=(
                "The relative path of the file you want to download."
            ),
        )
        parser.add_argument(
            "--destination_path",
            "-d",
            type=str,
            required=False,
            help=(
                "The target path you want to store the file."
            ),
        )
        parser.add_argument(
            "--recursive",
            "-r",
            action = "store_true",
            default = False,
            help=(
                "Indicate if you want to download all files under a specific path."
            ),
        )

    def take_action(self, parsed_args: Namespace) -> int:
        print(" This command has not been implemented yet")
        # dataset_name = parsed_args.dataset_repo_name
        # source_path = parsed_args.source_path
        # destination_path = parsed_args.destination_path
        # recursive_flag = parsed_args.recursive
        
        # TODO: download specific file/files according to source_path(single file/relative path)
        
        # if not destination_path:
        #     destination_path = os.getcwd()
                
        # ctx = ContextInfo()
        # client = ctx.get_client()
        
        # # parse dataset_name 
        # parsed_ds_name = dataset_name.replace("/",",")
        # # huggingface use underscores when loading/downloading datasets
        # parsed_save_path = dataset_name.replace("/","___")            
        return 0