import hashlib
import os
import os.path as osp
import re
import tempfile
from datetime import datetime
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Optional, Union, List, Dict
from urllib.error import HTTPError



import copy
import os
import tempfile
from functools import partial
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Dict, Optional, Union

import requests
from requests.adapters import Retry
from tqdm import tqdm

from weathon.errors.hub_error import FileDownloadError, NotExistError
from weathon.utils.config.config import Config
from weathon.utils.constants import DEFAULT_MODEL_REVISION, ModelFile, ConfigFields
from weathon.utils.constants.constants import (API_FILE_DOWNLOAD_CHUNK_SIZE,
                                               API_FILE_DOWNLOAD_RETRY_TIMES,
                                               API_FILE_DOWNLOAD_TIMEOUT, END_POINT,
                                               DEFAULT_MODELSCOPE_DOMAIN,
                                               DEFAULT_MODELSCOPE_GROUP,
                                               MODEL_ID_SEPARATOR, MODELSCOPE_SDK_DEBUG,
                                               MODELSCOPE_URL_SCHEME, ModelVisibility, Licenses, FILE_HASH)
from weathon.errors.hub_error import FileIntegrityError
from weathon.utils.fileio.caching import ModelFileSystemCache
from weathon.utils.fileio.file_utils import get_default_cache_dir
from weathon.utils.hub.api import ModelScopeConfig, HubApi,model_id_to_group_owner_name
from weathon.utils.logger import get_logger

logger = get_logger()





def get_cache_dir(model_id: Optional[str] = None):
    """cache dir precedence:
        function parameter > environment > ~/.cache/modelscope/hub

    Args:
        model_id (str, optional): The model id.

    Returns:
        str: the model_id dir if model_id not None, otherwise cache root dir.
    """
    default_cache_dir = get_default_cache_dir()
    base_path = os.getenv('MODELSCOPE_CACHE',
                          os.path.join(default_cache_dir, 'hub'))
    return base_path if model_id is None else os.path.join(
        base_path, model_id + '/')







def compute_hash(file_path):
    BUFFER_SIZE = 1024 * 64  # 64k buffer size
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            sha256_hash.update(data)
    return sha256_hash.hexdigest()


def file_integrity_validation(file_path, expected_sha256):
    """Validate the file hash is expected, if not, delete the file

    Args:
        file_path (str): The file to validate
        expected_sha256 (str): The expected sha256 hash

    Raises:
        FileIntegrityError: If file_path hash is not expected.

    """
    file_sha256 = compute_hash(file_path)
    if not file_sha256 == expected_sha256:
        os.remove(file_path)
        msg = 'File %s integrity check failed, the download may be incomplete, please try again.' % file_path
        logger.error(msg)
        raise FileIntegrityError(msg)


def create_model_if_not_exist(
        api,
        model_id: str,
        chinese_name: str,
        visibility: Optional[int] = ModelVisibility.PUBLIC,
        license: Optional[str] = Licenses.APACHE_V2,
        revision: Optional[str] = DEFAULT_MODEL_REVISION):
    exists = True
    try:
        api.get_model(model_id=model_id, revision=revision)
    except HTTPError:
        exists = False
    if exists:
        print(f'model {model_id} already exists, skip creation.')
        return False
    else:
        api.create_model(
            model_id=model_id,
            visibility=visibility,
            license=license,
            chinese_name=chinese_name,
        )
        print(f'model {model_id} successfully created.')
        return True


def read_config(model_id_or_path: str,
                revision: Optional[str] = DEFAULT_MODEL_REVISION):
    """ Read config from hub or local path

    Args:
        model_id_or_path (str): Model repo name or local directory path.
        revision: revision of the model when getting from the hub
    Return:
        config (:obj:`Config`): config object
    """
    if not os.path.exists(model_id_or_path):
        local_path = model_file_download(
            model_id_or_path, ModelFile.CONFIGURATION, revision=revision)
    elif os.path.isdir(model_id_or_path):
        local_path = os.path.join(model_id_or_path, ModelFile.CONFIGURATION)
    elif os.path.isfile(model_id_or_path):
        local_path = model_id_or_path

    return Config.from_file(local_path)


def auto_load(model: Union[str, List[str]]):
    if isinstance(model, str):
        if not osp.exists(model):
            model = snapshot_download(model)
    else:
        model = [
            snapshot_download(m) if not osp.exists(m) else m for m in model
        ]

    return model


def get_model_type(model_dir):
    """Get the model type from the configuration.

    This method will try to get the model type from 'model.backbone.type',
    'model.type' or 'model.model_type' field in the configuration.json file. If
    this file does not exist, the method will try to get the 'model_type' field
    from the config.json.

    Args:
        model_dir: The local model dir to use. @return: The model type
    string, returns None if nothing is found.
    """
    try:
        configuration_file = osp.join(model_dir, ModelFile.CONFIGURATION)
        config_file = osp.join(model_dir, 'config.json')
        if osp.isfile(configuration_file):
            cfg = Config.from_file(configuration_file)
            if hasattr(cfg.model, 'backbone'):
                return cfg.model.backbone.type
            elif hasattr(cfg.model,
                         'model_type') and not hasattr(cfg.model, 'type'):
                return cfg.model.model_type
            else:
                return cfg.model.type
        elif osp.isfile(config_file):
            cfg = Config.from_file(config_file)
            return cfg.model_type if hasattr(cfg, 'model_type') else None
    except Exception as e:
        logger.error(f'parse config file failed with error: {e}')


def parse_label_mapping(model_dir):
    """Get the label mapping from the model dir.

    This method will do:
    1. Try to read label-id mapping from the label_mapping.json
    2. Try to read label-id mapping from the configuration.json
    3. Try to read label-id mapping from the config.json

    Args:
        model_dir: The local model dir to use.

    Returns:
        The label2id mapping if found.
    """
    import json
    import os
    label2id = None
    label_path = os.path.join(model_dir, ModelFile.LABEL_MAPPING)
    if os.path.exists(label_path):
        with open(label_path, encoding='utf-8') as f:
            label_mapping = json.load(f)
        label2id = {name: idx for name, idx in label_mapping.items()}

    if label2id is None:
        config_path = os.path.join(model_dir, ModelFile.CONFIGURATION)
        config = Config.from_file(config_path)
        if hasattr(config, ConfigFields.model) and hasattr(
                config[ConfigFields.model], 'label2id'):
            label2id = config[ConfigFields.model].label2id
        elif hasattr(config, ConfigFields.model) and hasattr(
                config[ConfigFields.model], 'id2label'):
            id2label = config[ConfigFields.model].id2label
            label2id = {label: id for id, label in id2label.items()}
        elif hasattr(config, ConfigFields.preprocessor) and hasattr(
                config[ConfigFields.preprocessor], 'label2id'):
            label2id = config[ConfigFields.preprocessor].label2id
        elif hasattr(config, ConfigFields.preprocessor) and hasattr(
                config[ConfigFields.preprocessor], 'id2label'):
            id2label = config[ConfigFields.preprocessor].id2label
            label2id = {label: id for id, label in id2label.items()}

    config_path = os.path.join(model_dir, 'config.json')
    if label2id is None and os.path.exists(config_path):
        config = Config.from_file(config_path)
        if hasattr(config, 'label2id'):
            label2id = config.label2id
        elif hasattr(config, 'id2label'):
            id2label = config.id2label
            label2id = {label: id for id, label in id2label.items()}
    if label2id is not None:
        label2id = {label: int(id) for label, id in label2id.items()}
    return label2id


def snapshot_download(model_id: str,
                      revision: Optional[str] = DEFAULT_MODEL_REVISION,
                      cache_dir: Union[str, Path, None] = None,
                      user_agent: Optional[Union[Dict, str]] = None,
                      local_files_only: Optional[bool] = False,
                      cookies: Optional[CookieJar] = None,
                      ignore_file_pattern: List = None) -> str:
    """Download all files of a repo.
    Downloads a whole snapshot of a repo's files at the specified revision. This
    is useful when you want all files from a repo, because you don't know which
    ones you will need a priori. All files are nested inside a folder in order
    to keep their actual filename relative to that folder.

    An alternative would be to just clone a repo but this would require that the
    user always has git and git-lfs installed, and properly configured.

    Args:
        model_id (str): A user or an organization name and a repo name separated by a `/`.
        revision (str, optional): An optional Git revision id which can be a branch name, a tag, or a
            commit hash. NOTE: currently only branch and tag name is supported
        cache_dir (str, Path, optional): Path to the folder where cached files are stored.
        user_agent (str, dict, optional): The user-agent info in the form of a dictionary or a string.
        local_files_only (bool, optional): If `True`, avoid downloading the file and return the path to the
            local cached file if it exists.
        cookies (CookieJar, optional): The cookie of the request, default None.
        ignore_file_pattern (`str` or `List`, *optional*, default to `None`):
            Any file pattern to be ignored in downloading, like exact file names or file extensions.
    Raises:
        ValueError: the value details.

    Returns:
        str: Local folder path (string) of repo snapshot

    Note:
        Raises the following errors:
        - [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
        if `use_auth_token=True` and the token cannot be found.
        - [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError) if
        ETag cannot be determined.
        - [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        if some parameter value is invalid
    """

    if cache_dir is None:
        cache_dir = get_cache_dir()
    if isinstance(cache_dir, Path):
        cache_dir = str(cache_dir)
    temporary_cache_dir = os.path.join(cache_dir, 'temp')
    os.makedirs(temporary_cache_dir, exist_ok=True)

    group_or_owner, name = model_id_to_group_owner_name(model_id)

    cache = ModelFileSystemCache(cache_dir, group_or_owner, name)
    if local_files_only:
        if len(cache.cached_files) == 0:
            raise ValueError(
                'Cannot find the requested files in the cached path and outgoing'
                ' traffic has been disabled. To enable model look-ups and downloads'
                " online, set 'local_files_only' to False.")
        logger.warning(f'We can not confirm the cached file is for revision: {revision}')
        return cache.get_root_location(
        )  # we can not confirm the cached file is for snapshot 'revision'
    else:
        # make headers
        headers = {'user-agent': ModelScopeConfig.get_user_agent(user_agent=user_agent, )}
        _api = HubApi()
        if cookies is None:
            cookies = ModelScopeConfig.get_cookies()
        revision = _api.get_valid_revision(model_id, revision=revision, cookies=cookies)

        snapshot_header = headers if 'CI_TEST' in os.environ else {
            **headers,
            **{'Snapshot': 'True'}
        }
        model_files = _api.get_model_files(model_id=model_id, revision=revision, recursive=True,
                                           use_cookies=False if cookies is None else cookies, headers=snapshot_header, )

        if ignore_file_pattern is None:
            ignore_file_pattern = []
        if isinstance(ignore_file_pattern, str):
            ignore_file_pattern = [ignore_file_pattern]

        with tempfile.TemporaryDirectory(
                dir=temporary_cache_dir) as temp_cache_dir:
            for model_file in model_files:
                if model_file['Type'] == 'tree' or any(
                        [re.search(pattern, model_file['Name']) is not None for pattern in ignore_file_pattern]):
                    continue
                # check model_file is exist in cache, if existed, skip download, otherwise download
                if cache.exists(model_file):
                    file_name = os.path.basename(model_file['Name'])
                    logger.debug(f'File {file_name} already in cache, skip downloading!')
                    continue

                # get download url
                url = get_file_download_url(
                    model_id=model_id,
                    file_path=model_file['Path'],
                    revision=revision)

                # First download to /tmp
                http_get_file(
                    url=url,
                    local_dir=temp_cache_dir,
                    file_name=model_file['Name'],
                    headers=headers,
                    cookies=cookies)
                # check file integrity
                temp_file = os.path.join(temp_cache_dir, model_file['Name'])
                if FILE_HASH in model_file:
                    file_integrity_validation(temp_file, model_file[FILE_HASH])
                # put file to cache
                cache.put_file(model_file, temp_file)

        return os.path.join(cache.get_root_location())




def model_file_download(
        model_id: str,
        file_path: str,
        revision: Optional[str] = DEFAULT_MODEL_REVISION,
        cache_dir: Optional[str] = None,
        user_agent: Union[Dict, str, None] = None,
        local_files_only: Optional[bool] = False,
        cookies: Optional[CookieJar] = None,
) -> Optional[str]:  # pragma: no cover
    """Download from a given URL and cache it if it's not already present in the local cache.

    Given a URL, this function looks for the corresponding file in the local
    cache. If it's not there, download it. Then return the path to the cached
    file.

    Args:
        model_id (str): The model to whom the file to be downloaded belongs.
        file_path(str): Path of the file to be downloaded, relative to the root of model repo.
        revision(str, optional): revision of the model file to be downloaded.
            Can be any of a branch, tag or commit hash.
        cache_dir (str, Path, optional): Path to the folder where cached files are stored.
        user_agent (dict, str, optional): The user-agent info in the form of a dictionary or a string.
        local_files_only (bool, optional):  If `True`, avoid downloading the file and return the path to the
            local cached file if it exists. if `False`, download the file anyway even it exists.
        cookies (CookieJar, optional): The cookie of download request.

    Returns:
        string: string of local file or if networking is off, last version of
        file cached on disk.

    Raises:
        NotExistError: The file is not exist.
        ValueError: The request parameter error.

    Note:
        Raises the following errors:

            - [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
            if `use_auth_token=True` and the token cannot be found.
            - [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError)
            if ETag cannot be determined.
            - [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            if some parameter value is invalid
    """
    if cache_dir is None:
        cache_dir = get_cache_dir()
    if isinstance(cache_dir, Path):
        cache_dir = str(cache_dir)
    temporary_cache_dir = os.path.join(cache_dir, 'temp')
    os.makedirs(temporary_cache_dir, exist_ok=True)

    group_or_owner, name = model_id_to_group_owner_name(model_id)

    cache = ModelFileSystemCache(cache_dir, group_or_owner, name)

    # if local_files_only is `True` and the file already exists in cached_path
    # return the cached path
    if local_files_only:
        cached_file_path = cache.get_file_by_path(file_path)
        if cached_file_path is not None:
            logger.warning(
                "File exists in local cache, but we're not sure it's up to date"
            )
            return cached_file_path
        else:
            raise ValueError(
                'Cannot find the requested files in the cached path and outgoing'
                ' traffic has been disabled. To enable model look-ups and downloads'
                " online, set 'local_files_only' to False.")

    _api = HubApi()
    headers = {
        'user-agent': ModelScopeConfig.get_user_agent(user_agent=user_agent, )
    }
    if cookies is None:
        cookies = ModelScopeConfig.get_cookies()

    revision = _api.get_valid_revision(model_id, revision=revision, cookies=cookies)
    file_to_download_info = None
    # we need to confirm the version is up-to-date
    # we need to get the file list to check if the latest version is cached, if so return, otherwise download
    model_files = _api.get_model_files(model_id=model_id, revision=revision, recursive=True,
                                       use_cookies=False if cookies is None else cookies)

    for model_file in model_files:
        if model_file['Type'] == 'tree':
            continue

        if model_file['Path'] == file_path:
            if cache.exists(model_file):
                logger.debug(f'File {model_file["Name"]} already in cache, skip downloading!')
                return cache.get_file_by_info(model_file)
            else:
                file_to_download_info = model_file
            break

    if file_to_download_info is None:
        raise NotExistError('The file path: %s not exist in: %s' %
                            (file_path, model_id))

    # we need to download again
    url_to_download = get_file_download_url(model_id, file_path, revision)
    file_to_download_info = {
        'Path': file_path,
        'Revision': file_to_download_info['Revision'],
        FILE_HASH: file_to_download_info[FILE_HASH]
    }

    temp_file_name = next(tempfile._get_candidate_names())
    http_get_file(
        url_to_download,
        temporary_cache_dir,
        temp_file_name,
        headers=headers,
        cookies=None if cookies is None else cookies.get_dict())
    temp_file_path = os.path.join(temporary_cache_dir, temp_file_name)
    # for download with commit we can't get Sha256
    if file_to_download_info[FILE_HASH] is not None:
        file_integrity_validation(temp_file_path,
                                  file_to_download_info[FILE_HASH])
    return cache.put_file(file_to_download_info, os.path.join(temporary_cache_dir, temp_file_name))


def get_file_download_url(model_id: str, file_path: str, revision: str):
    """Format file download url according to `model_id`, `revision` and `file_path`.
    e.g., Given `model_id=john/bert`, `revision=master`, `file_path=README.md`,
    the resulted download url is: https://modelscope.cn/api/v1/models/john/bert/repo?Revision=master&FilePath=README.md

    Args:
        model_id (str): The model_id.
        file_path (str): File path
        revision (str): File revision.

    Returns:
        str: The file url.
    """
    download_url_template = '{endpoint}/api/v1/models/{model_id}/repo?Revision={revision}&FilePath={file_path}'
    return download_url_template.format(
        endpoint=END_POINT,
        model_id=model_id,
        revision=revision,
        file_path=file_path,
    )


def http_get_file(
        url: str,
        local_dir: str,
        file_name: str,
        cookies: CookieJar,
        headers: Optional[Dict[str, str]] = None,
):
    """Download remote file, will retry 5 times before giving up on errors.

    Args:
        url(str):
            actual download url of the file
        local_dir(str):
            local directory where the downloaded file stores
        file_name(str):
            name of the file stored in `local_dir`
        cookies(CookieJar):
            cookies used to authentication the user, which is used for downloading private repos
        headers(Dict[str, str], optional):
            http headers to carry necessary info when requesting the remote file

    Raises:
        FileDownloadError: File download failed.

    """
    total = -1
    temp_file_manager = partial(
        tempfile.NamedTemporaryFile, mode='wb', dir=local_dir, delete=False)
    get_headers = {} if headers is None else copy.deepcopy(headers)
    with temp_file_manager() as temp_file:
        logger.debug('downloading %s to %s', url, temp_file.name)
        # retry sleep 0.5s, 1s, 2s, 4s
        retry = Retry(
            total=API_FILE_DOWNLOAD_RETRY_TIMES,
            backoff_factor=1,
            allowed_methods=['GET'])
        while True:
            try:
                downloaded_size = temp_file.tell()
                get_headers['Range'] = 'bytes=%d-' % downloaded_size
                r = requests.get(url, stream=True, headers=get_headers, cookies=cookies,
                                 timeout=API_FILE_DOWNLOAD_TIMEOUT)
                r.raise_for_status()
                content_length = r.headers.get('Content-Length')
                total = int(content_length) if content_length is not None else None
                progress = tqdm(unit='B', unit_scale=True, unit_divisor=1024, total=total, initial=downloaded_size,
                                desc='Downloading', )
                for chunk in r.iter_content(chunk_size=API_FILE_DOWNLOAD_CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        progress.update(len(chunk))
                        temp_file.write(chunk)
                progress.close()
                break
            except (Exception) as e:  # no matter what happen, we will retry.
                retry = retry.increment('GET', url, error=e)
                retry.sleep()

    logger.debug('storing %s in cache at %s', url, local_dir)
    downloaded_length = os.path.getsize(temp_file.name)
    if total != downloaded_length:
        os.remove(temp_file.name)
        msg = 'File %s download incomplete, content_length: %s but the \
                    file downloaded length: %s, please download again' % (
            file_name, total, downloaded_length)
        logger.error(msg)
        raise FileDownloadError(msg)
    os.replace(temp_file.name, os.path.join(local_dir, file_name))
