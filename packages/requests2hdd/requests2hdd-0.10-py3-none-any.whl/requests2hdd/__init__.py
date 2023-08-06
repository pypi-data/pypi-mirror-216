import os
import requests
from touchtouch import touch
from windows_filepath import make_filepath_windows_comp


def get_and_save(
    link: str,
    path: str,
    status_codes: tuple | list = (200,),
    correct_path_on_failure: bool = True,
    *args,
    **kwargs
) -> None | str:
    r"""
    Downloads a file from the specified URL and saves it to the specified path.

    Args:
        link (str): The URL of the file to download.
        path (str): The directory path where the file should be saved.
        status_codes (tuple | list, optional): A collection of HTTP status codes to consider as successful.
                                               Defaults to (200,).
        correct_path_on_failure (bool, optional): Specifies whether to attempt to correct the file path in case of
                                                  an exception. If True, it replaces illegal characters and resolves
                                                  other path-related issues. Defaults to True.
        *args: Additional positional arguments to be passed to the requests.get() function.
        **kwargs: Additional keyword arguments to be passed to the requests.get() function.

    Returns:
        None | str: If the download is successful and the status code matches any of the provided status codes,
                    it returns the absolute path of the saved file. Otherwise, it returns None.
    """
    path = os.path.normpath(os.path.join(path, link.split("://")[-1]))
    return_val = None
    with requests.get(link, *args, **kwargs) as res:
        if res.status_code in status_codes:
            try:
                touch(path)
                with open(path, mode="wb") as f:
                    f.write(res.content)
            except Exception as e:
                if correct_path_on_failure:
                    path = make_filepath_windows_comp(
                        filepath=path,
                        fillvalue="_",  # replacement of any illegal char
                        reduce_fillvalue=False,  # */<> (illegal chars) -> ____ (replacement) -> _ (reduced replacement)
                        remove_backslash_and_col=False,  # important for multiple folders
                        spaceforbidden=False,  # '\s' -> _
                        other_to_replace=(),  # other chars you don't want in the file path
                        slash_to_backslash=True,  # replaces / with \\ before doing all the other replacements
                    )
                    touch(path)
                    with open(path, mode="wb") as f:
                        f.write(res.content)
                else:
                    raise e

            return_val = path
    return return_val
