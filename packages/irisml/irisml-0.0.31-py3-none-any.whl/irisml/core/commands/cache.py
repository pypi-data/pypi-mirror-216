import argparse
import datetime
import os
import pathlib
import pickle
import re
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient


def cache_list(blobs):
    for b in blobs:
        print(f"{b.name}: last_modified_at: {b.last_modified}")

    print(f"Total: {len(blobs)} blobs.")


def cache_remove(blobs, container_client):
    response = input(f"Removing {len(blobs)} blobs. Continue? [y/N]: ")
    if response.lower() != 'y':
        return

    chunk_size = 256
    for i in range(0, len(blobs), chunk_size):
        container_client.delete_blobs(*blobs[i:i+chunk_size])
    print("Deleted.")


def cache_show(blobs, container_client):
    for b in blobs:
        if b.size < 1024:
            data = pickle.loads(container_client.download_blob(b).readall())
            print(f"{b.name}: {data}")
        else:
            print(f"{b.name}: size={b.size}. To download the file, please use the download command.")


def cache_download(blobs, container_client):
    response = input(f"Found {len(blobs)} blobs. Download all? [y/N]: ")
    if response.lower() != 'y':
        return

    for b in blobs:
        local_filepath = pathlib.Path(b.name)
        local_filepath.parent.mkdir(parents=True, exist_ok=True)
        local_filepath.write_bytes(container_client.download_blob(b).readall())
        print(f"Saved {local_filepath}")


def get_blobs(container_client, mtime, name):
    if mtime:
        m = re.match(r'([+-])([0-9]+)$', mtime)
        assert m.group(1) in ('+', '-')
        time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=int(m.group(2)))
        time_older = m.group(1) == '+'
    else:
        time_threshold = None

    def match_condition(b):
        if time_threshold:
            is_older = b.last_modified < time_threshold
            if time_older != is_older:  # XOR
                return False

        if name and name not in b.name:
            return False

        return True

    return list(b for b in container_client.list_blobs() if match_condition(b))


def main():
    parser = argparse.ArgumentParser(description="Manage a cache storage.")
    subparser = parser.add_subparsers(dest='command', required=True)

    def add_subparser(subparser, name):
        s = subparser.add_parser(name)
        s.add_argument('--mtime', help="Select blobs that were modified n*24 hours ago.")
        s.add_argument('--name', help="Select blobs whose name contain this string.")

    add_subparser(subparser, 'download')
    add_subparser(subparser, 'list')
    add_subparser(subparser, 'remove')
    add_subparser(subparser, 'show')

    args = parser.parse_args()

    cache_storage_url = os.getenv('IRISML_CACHE_URL')
    if not cache_storage_url:
        parser.error("Please set IRISML_CACHE_URL.")

    print(f"Using cache url: {cache_storage_url}")

    container_client = ContainerClient.from_container_url(cache_storage_url, credential=DefaultAzureCredential())
    blobs = get_blobs(container_client, args.mtime, args.name)
    if not blobs:
        print("No blob found.")
        return

    if args.command == 'list':
        cache_list(blobs)
    elif args.command == 'download':
        cache_list(blobs)
        cache_download(blobs, container_client)
    elif args.command == 'remove':
        cache_list(blobs)
        cache_remove(blobs, container_client)
    elif args.command == 'show':
        cache_show(blobs, container_client)


if __name__ == '__main__':
    main()
