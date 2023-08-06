import os
import os.path
import glob
import logging

from argparse import Namespace

from maccarone.openai import CachedChatAPI
from maccarone.loader import (
    DEFAULT_CACHE_SUFFIX,
    DEFAULT_MN_SUFFIX,
    replace_suffix,
)
from maccarone.preprocessor import preprocess_maccarone

logger = logging.getLogger(__name__)

def preprocess(
        mn_path: str,
        print_: bool,
        write: bool,
        rewrite: bool,
        search_suffix: str,
    ) -> None:
    # produce Python source
    logger.info("preprocessing %s", mn_path)

    cache_path = replace_suffix(mn_path, DEFAULT_CACHE_SUFFIX, search_suffix)
    chat_api = CachedChatAPI(cache_path)

    with open(mn_path, "r") as f:
        mn_source = f.read()


    py_source = preprocess_maccarone(mn_source, chat_api)

    if write:
        py_path = replace_suffix(mn_path, ".py", search_suffix)

        logger.info("writing %s", py_path)

        if py_path == mn_path:
            raise ValueError("won't overwrite input file", mn_path)
    elif rewrite:
        py_path = mn_path
    else:
        py_path = None

    if py_path is not None:
        with open(py_path, "w") as f:
            f.write(py_source)


    if print_:
        print(py_source, end="")

def main(path: str, print_: bool, write: bool, rewrite: bool, suffix: str) -> None:
    """Preprocess files with Maccarone snippets."""

    if os.path.isdir(path):
        mn_files = glob.glob(
            os.path.join(path, f"**/*{suffix}"),
            recursive=True,
        )
    else:
        mn_files = [path]

    for mn_file in mn_files:
        preprocess(mn_file, print_, write, rewrite, suffix)


def parse_args() -> Namespace:
    import argparse
    parser = argparse.ArgumentParser(description="Preprocess files with Maccarone snippets.")
    parser.add_argument("path", help="Path to the file or directory containing files to preprocess.")
    parser.add_argument("--print", dest="print_", action="store_true", help="Print the preprocessed Python source.")
    parser.add_argument("--write", action="store_true", help="Write the preprocessed Python source to a .py file.")
    parser.add_argument("--rewrite", action="store_true", help="Overwrite the input file with the preprocessed Python source.")
    parser.add_argument("--suffix", default=DEFAULT_MN_SUFFIX, help="Suffix for files to preprocess (default: %(default)s).")
    args = parser.parse_args()
    return args


def script_main():
    logging.basicConfig(level=logging.INFO)

    return main(**vars(parse_args()))

if __name__ == "__main__":
    script_main()
