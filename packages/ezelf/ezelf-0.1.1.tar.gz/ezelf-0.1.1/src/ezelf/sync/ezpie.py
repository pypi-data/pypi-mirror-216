# -*- coding=utf-8
import logging
import os
import shutil
import tarfile
import tempfile
import zipfile
from typing import List, Union

import requests
from qcloud_cos import CosConfig, CosS3Client

WORKING_DIR = "/home/workspace"
ARTIFACTS_DIR = "/home/artifacts"

# TAR_ARCHIVE_NAME = "archive.tar.gz"
ZIP_ARCHIVE_NAME = "archive.zip"

ARTIFACTS_BUCKET_NAME = "workstation-test"
APPID = "1313546141"
secret_id = "IKIDHTVO5mLpU3ReorlV4UmvxxvnV3q6JOK6"
secret_key = "ht2871scFlAWmvKcXO8lKoBRdlrQuJbn"
region = "ap-hongkong"
token = None
scheme = "https"


sync_host = "http://43.135.89.27:8080"
sync_api = "/api/common/task/project/file/sync"


config = None
client = None


class EzpieSyncError(Exception):
    def __init__(self, message: str):
        self.message: str = message


def task_id() -> str:
    """
    从环境变量获取 task id
    """
    task_id = os.environ.get("TASKID", "NO_TASKID")
    return task_id


def file_size() -> int:
    """
    获取压缩文件大小, 单位: KB
    """
    file = os.path.join(ARTIFACTS_DIR, ZIP_ARCHIVE_NAME)
    file_size = os.path.getsize(file)  # unit: bytes
    return file_size // 1024


def tencent_cos_url() -> str:
    """
    获取腾讯云对象存储的url, 由于私读私写该url实际不可访问
    """
    global config
    global client
    if config is None:
        config = CosConfig(
            Region=region,
            SecretId=secret_id,
            SecretKey=secret_key,
            Token=token,
            Scheme=scheme,
        )
    if client is None:
        client = CosS3Client(config)

    url = client.get_object_url(
        Bucket=f"{ARTIFACTS_BUCKET_NAME}-{APPID}",
        Key=f"artifacts/task-{task_id()}/archive.zip",
    )
    return url


def prepare_save_param() -> Union[dict, None]:
    """
    准备调用 ezpie 接口的数据, 该接口用于保存所提交文件的信息, 方便网页下载
    """
    tid = task_id()
    if tid == "NO_TASKID":
        logging.error("env no task id")
        return None

    data = {
        "fileKey": f"/artifacts/task-{tid}/",
        "fileSize": file_size(),
        "taskId": int(tid),
        "name": ZIP_ARCHIVE_NAME,
        "bucketName": f"{ARTIFACTS_BUCKET_NAME}-{APPID}",
        "url": tencent_cos_url(),
    }
    return data


def save_record():
    """
    失败抛出 EzpieSyncError
    """
    try:
        data = prepare_save_param()
    except Exception as e:
        raise EzpieSyncError(f"prepare param raise exception: {e}")

    if data is None:
        raise EzpieSyncError("data is None")

    sync_url = f"{sync_host}{sync_api}"

    logging.info(f"payload: {data}")
    try:
        response = requests.post(sync_url, json=data, timeout=(6, 4))
    except Exception as e:
        raise EzpieSyncError(f"requests except, {e}")

    response_code = response.status_code
    if response_code != 200:
        raise EzpieSyncError(f"status_code error, status_code={response_code}")

    try:
        response_data = response.json()
    except Exception as e:
        raise EzpieSyncError(f"decode json error, {e}")

    if not response_data["success"]:
        raise EzpieSyncError(f"sync failed: {response_data}")

    logging.info(f"sync success: {response_data}")


def ezecho(input):
    return input


def copy_dir(dir: str = None, dest_dir: str = None, include_hidden_files=False):
    """将目录下的文件打包并拷贝到 artifacts 目录"""
    if dir is None:
        dir = WORKING_DIR
    if dest_dir is None:
        dest_dir = ARTIFACTS_DIR

    create_zip_archive_from_dir(dir, dest_dir, ZIP_ARCHIVE_NAME)
    for _ in range(5):
        try:
            save_record()
            logging.info("save success")
            break
        except EzpieSyncError as e:
            logging.critical(f"save failed: {e}")


def copy_files(file_list: List[str], dest_dir: str):
    """将文件打包并拷贝到 artifacts 目录"""
    if dest_dir is None:
        dest_dir = ARTIFACTS_DIR

    create_zip_archive_from_file_list(file_list, dest_dir, ZIP_ARCHIVE_NAME)
    for _ in range(5):
        try:
            save_record()
            logging.info("save success")
            break
        except EzpieSyncError as e:
            logging.critical(f"save failed: {e}")


# **************** utils ****************


def create_zip_archive_from_dir(source_dir, destination_dir, archive_name):
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    # 创建 zip 文件
    archive_path = os.path.join(temp_dir, archive_name)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 遍历源目录中的所有文件和子目录
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, source_dir))

    # 将生成的 zip 文件移动到目标目录
    destination_path = os.path.join(destination_dir, archive_name)
    shutil.move(archive_path, destination_path)

    # 删除临时文件夹
    shutil.rmtree(temp_dir)

    # 返回 zip 文件的路径
    return destination_path


def create_tar_archive_from_dir(source_dir, destination_dir, archive_name):
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    # 创建 tar.gz 文件
    archive_path = os.path.join(temp_dir, archive_name)
    with tarfile.open(archive_path, "w:gz") as tar:
        # 遍历源目录中的所有文件和子目录
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=os.path.relpath(file_path, source_dir))

    # 将生成的 tar 包移动到目标目录
    destination_path = os.path.join(destination_dir, archive_name)
    shutil.move(archive_path, destination_path)

    # 删除临时文件夹
    shutil.rmtree(temp_dir)

    # 返回 tar.gz 文件的路径
    return destination_path


def create_zip_archive_from_file_list(files, destination_dir, archive_name):
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    # 找到路径最浅的文件
    base_dir = os.path.commonpath(files)

    # 创建 zip 文件
    archive_path = os.path.join(temp_dir, archive_name)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 遍历文件列表
        for file_path in files:
            if os.path.isfile(file_path):  # 确保文件存在
                # 计算相对路径
                rel_path = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname=rel_path)

    # 将生成的 zip 文件移动到目标目录
    destination_path = os.path.join(destination_dir, archive_name)
    shutil.move(archive_path, destination_path)

    # 删除临时文件夹
    shutil.rmtree(temp_dir)

    # 返回 zip 文件的路径
    return destination_path


def create_tar_archive_from_file_list(files, destination_dir, archive_name):
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    # 找到路径最浅的文件
    base_dir = os.path.commonpath(files)

    # 创建 tar 文件
    archive_path = os.path.join(temp_dir, archive_name)
    with tarfile.open(archive_path, "w:gz") as tar:
        # 遍历文件列表
        for file_path in files:
            if os.path.isfile(file_path):  # 确保文件存在
                # 计算相对路径
                rel_path = os.path.relpath(file_path, base_dir)
                tar.add(file_path, arcname=rel_path)

    # 将生成的 tar 文件移动到目标目录
    destination_path = os.path.join(destination_dir, archive_name)
    shutil.move(archive_path, destination_path)

    # 删除临时文件夹
    shutil.rmtree(temp_dir)

    # 返回 tar 文件的路径
    return destination_path
