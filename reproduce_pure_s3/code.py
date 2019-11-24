import os
from concurrent.futures import ThreadPoolExecutor


def make_client():
    import boto3
    session = boto3.session.Session(
        profile_name=None, region_name=None
    )

    s3 = session.client("s3", endpoint_url=None, use_ssl=True)
    return s3


def prepare_files(num, single_file_size=100):
    import os
    from random import randint

    data_path = os.path.join(os.getcwd(), "data")

    if os.path.exists(data_path):
        import shutil
        shutil.rmtree(data_path)

    os.mkdir(data_path)
    file_paths = []
    for i in range(num):
        file_path = os.path.join(data_path, str(randint(0, 1000000)))
        file_paths.append(file_path)
        with open(file_path, "w+") as fd:
            fd.write(str(os.urandom(single_file_size)))

    return file_paths


CLIENT = make_client()
def upload_file_single_client( file):
    CLIENT.upload_file(file, BUCKET, os.path.join(DATA_PATH, os.path.basename(file)))

def upload_file_new_client(file):
    client = make_client()
    client.upload_file(file, BUCKET, os.path.join(DATA_PATH, os.path.basename(file)))


def upload_files_multiple_clients(files):
    with ThreadPoolExecutor(max_workers=JOBS) as executor:
        executor.map(upload_file_new_client, files)


BUCKET='prd-dvc-test'
DATA_PATH="data"
JOBS=32

files = prepare_files(128, 100000)
# upload_files_single_client(files)
upload_files_multiple_clients(files)

