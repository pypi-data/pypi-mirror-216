import os
import io
import re
import tempfile
from functools import partial
from contextlib import contextmanager
from typing import Optional, Generator, BinaryIO, Union, List
from pathlib import Path
from filelock import FileLock
from requests.adapters import Retry
from tqdm import tqdm

from scoamp.api import global_api as api
from scoamp.utils.error import FileDownloadError

def model_file_list(
    model_id: str,
    *,
    is_public: bool = False,
    revision: Optional[str] = None,
) -> list:
    """List all files in a model recursively
    Args:
        model_id (`str`):
            model id.
        is_public (`bool`):
            whether public model, default to user model
        revision (`str`, *optional*):
            An optional Git revision id which can be a branch name, a tag, or a
            commit hash.

    Returns:
        flatten file list
    """
    if is_public:
        return api.list_public_model_files(model_id, revision)
    else:
        return api.list_user_model_files(model_id, revision)


# TODO local cache system
def model_file_download(
    model_id: str,
    file_path: str,
    *,
    is_public: bool = False,
    revision: Optional[str] = None,
    local_dir: Optional[str] = None,
    force_download: bool = False,
    resume_download: bool = True,
) -> str:
    """Download a given file from amp server
    Args:
        model_id (`str`):
            model id.
        file_path (`str`):
            file path in the repo, with subfolder.
        is_public (`bool`, *optional*):
            whether public model, default to user model
        revision (`str`, *optional*):
            An optional Git revision id which can be a branch name, a tag, or a
            commit hash.
        local_dir (`str` or `Path`, *optional*):
            If provided, the downloaded file will be placed under this directory
        force_download (`bool`, *optional*, defaults to `False`):
            Whether the file should be downloaded even if it already exists in
            the local dir.
        resume_download (`bool`, *optional*, defaults to `False`):
            If `True`, resume a previously interrupted download.

    Returns:
        Local path (string) of file
    """
    if not model_id:
        raise ValueError('model_id shoud not be empty')

    if not file_path:
        raise ValueError('file_path should not be empty')

    if not local_dir:
        local_dir = '.'
    local_dir = Path(local_dir).expanduser()
    if not local_dir.exists():
        raise ValueError(f"local directory '{local_dir}' not exists")

    local_file_path = local_dir / file_path
    if local_file_path.exists() and not force_download:
        raise ValueError(f"'{file_path}' already exists at local, set 'force_download=True' to overwrite")

    local_file_path.parent.mkdir(parents=True, exist_ok=True)
    # Prevent parallel downloads of the same file with a lock.
    lock_path = Path(str(local_file_path) + ".lock")
    with FileLock(lock_path):
        if resume_download:
            incomplete_path = Path(str(local_file_path) + ".incomplete")

            @contextmanager
            def _resumable_file_manager() -> Generator[io.BufferedWriter, None, None]:
                with open(incomplete_path, "ab") as f:
                    yield f

            temp_file_manager = _resumable_file_manager
        else:
            temp_file_manager = partial(  # type: ignore
                tempfile.NamedTemporaryFile, mode="wb", dir=local_dir, delete=False
            )

        # Download to temporary file, then copy to local dir once finished.
        # Otherwise you get corrupt entries if the download gets interrupted.
        with temp_file_manager() as temp_file:
            _http_get_model_file(
                temp_file,
                model_id,
                file_path,
                is_public = is_public,
                revision = revision,
            )

        os.replace(temp_file.name, local_file_path)

    try:
        lock_path.unlink()
    except OSError:
        pass

    return str(local_file_path)

API_FILE_DOWNLOAD_RETRY_TIMES = 3
API_FILE_DOWNLOAD_TIMEOUT = 60 * 5
API_FILE_DOWNLOAD_CHUNK_SIZE = 1024 * 1024

def _http_get_model_file(
    temp_file: BinaryIO,
    model_id: str,
    file_path: str,
    *,
    is_public: bool = False,
    revision: Optional[str] = None,
):
    # TODO retry policy
    ## retry sleep 0.5s, 1s, 2s
    #retry = Retry(
    #    total= API_FILE_DOWNLOAD_RETRY_TIMES,
    #    backoff_factor=1,
    #    allowed_methods=['GET'])

    downloaded_size = temp_file.tell()
    r = api.download_file(
            model_id,
            file_path,
            revision=revision,
            is_public=is_public,
            resume_size=downloaded_size,
            timeout=API_FILE_DOWNLOAD_TIMEOUT,
        )
    content_length = r.headers.get('Content-Length')
    total = downloaded_size + int(content_length) if content_length is not None else None

    desc_file_name = file_path
    if len(desc_file_name) > 22:
        desc_file_name = f"(…){desc_file_name[-20:]}"

    progress = tqdm(
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        total=total,
        initial=downloaded_size,
        desc=f'Downloading {desc_file_name}',
    )
    for chunk in r.iter_content(chunk_size=API_FILE_DOWNLOAD_CHUNK_SIZE):
        if chunk:  # filter out keep-alive new chunks
            progress.update(len(chunk))
            temp_file.write(chunk)
    progress.close()
    temp_file.flush()

    downloaded_length = os.path.getsize(temp_file.name)
    if total and total != downloaded_length:
        msg = f"download file '{file_path}' from model '{model_id}' error: expect file size is '{total}', but download size is '{downloaded_length}'"
        raise FileDownloadError(msg)

    return downloaded_length


# TODO
#   1. parallel download
#   2. cache system
def snapshot_download(
    model_id: str,
    local_dir: str,
    *,
    is_public: bool = False,
    revision: Optional[str] = None,
    force_download: bool = False,
    resume_download: bool = True,
    ignore_patterns: Optional[Union[List[str], str]] = None,
) -> str:
    """Download repo files.

    Download a whole snapshot of a repo's files at the specified revision. This is useful when you want all files from
    a repo, because you don't know which ones you will need a priori. All files are nested inside a folder in order
    to keep their actual filename relative to that folder. You can also filter which files to download using
    `allow_patterns` and `ignore_patterns`.

    An alternative would be to clone the repo but this requires git and git-lfs to be installed and properly
    configured. It is also not possible to filter which files to download when cloning a repository using git.

    Args:
        model_id (`str`):
            model_id
        local_dir (`str` or `Path`, *optional*:
            the downloaded files will be placed under this directory 
        is_public (`bool`, *optional*):
            whether public model, default to user model
        revision (`str`, *optional*):
            An optional Git revision id which can be a branch name, a tag, or a
            commit hash.
        force_download (`bool`, *optional*, defaults to `False`):
            Whether the file should be downloaded even if it already exists in the local dir.
        resume_download (`bool`, *optional*, defaults to `False):
            If `True`, resume a previously interrupted download.
        ignore_patterns (`List[str]` or `str`, *optional*):
            If provided, files matching any of the patterns are not downloaded.

    Returns:
        Local folder path (string) of repo snapshot

    <Tip>

    Raises the following errors:

    - [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
      if `token=True` and the token cannot be found.
    - [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError) if
      ETag cannot be determined.
    - [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
      if some parameter value is invalid

    </Tip>
    """
    if not model_id:
        raise ValueError('model_id shoud not be empty')

    if not local_dir:
        raise ValueError('local_dir shoud not be specified')
    local_dir_path = Path(local_dir).expanduser()
    if not local_dir_path.exists():
        raise ValueError(f"local directory '{local_dir}' not exists")
    
    if not ignore_patterns:
        ignore_patterns = []
    elif isinstance(ignore_patterns, str):
        ignore_patterns = [ignore_patterns]

    model_files = model_file_list(model_id, is_public=is_public, revision=revision)

    for model_file in model_files:
        if model_file['file_type'] == 'FileType_Dir' or \
                any([re.search(pattern, model_file['name']) is not None for pattern in ignore_patterns]):
            # TODO add log
            continue

        file_path = model_file['path']
        local_file_path = local_dir_path / file_path
        # check model_file exists, if exists and force_download=False, then skip, otherwise download
        if not force_download and local_file_path.exists():
            # TODO add log
            continue

        model_file_download(
            model_id,
            file_path,
            is_public=is_public,
            revision=revision,
            local_dir=local_dir,
            force_download=force_download,
            resume_download=resume_download,
        )
    return local_dir

