#!/usr/bin/env python3

import os
import sys
import signal
import boto3
import botocore.exceptions
from simple_term_menu import TerminalMenu

all_regions = ["af-south-1", "ap-east-1", "ap-south-1", "ap-northeast-3", "ap-northeast-2", "ap-southeast-1",
               "ap-southeast-2", "ap-northeast-1", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2",
               "eu-south-1", "eu-west-3", "eu-north-1", "me-south-1", "sa-east-1", "us-gov-east-1", "us-gov-west-1",
               "us-east-1", "us-east-2", "us-west-1", "us-west-2"]


def main(args):
    validate_region(args)
    if args[1] not in all_regions:
        region = show_items(all_regions, "Choose region")
    else:
        region = args[1]

    profile = show_items(get_profiles(), "Choose profile")
    boto3.setup_default_session(profile_name=profile, region_name=region)
    client = boto3.client("ecs")
    try:
        cluster = show_items(get_clusters(client), "Choose cluster")
        service = show_items(get_services(client, cluster), "Choose service")
        task = show_items(get_tasks(client, cluster, service), "Choose task")
        container = show_items(get_containers(client, cluster, task), "Choose container")
        command = get_command(args)
        os.system(
            f"aws ecs execute-command --region {region} --cluster {cluster} --task {task} --container {container} --command {command} --profile {profile} --interactive")
    except botocore.exceptions.ClientError as e:
        print(f"Client error: {e}")


def get_profiles():
    return boto3.session.Session().available_profiles


def show_items(items, title):
    if len(items) == 1:
        return items[0]
    if len(items) == 0:
        print("No items to show. Exit")
        exit()
    terminal_menu = TerminalMenu(items, show_search_hint=True, title=title)
    menu_entry_index = terminal_menu.show()
    return items[menu_entry_index]


def get_clusters(client):
    items = client.list_clusters()
    return items['clusterArns']


def get_services(client, cluster):
    items = client.list_services(cluster=cluster)
    return items['serviceArns']


def get_tasks(client, cluster, service):
    items = client.list_tasks(cluster=cluster, serviceName=service)
    return items['taskArns']


def get_containers(client, cluster, task):
    items = client.describe_tasks(cluster=cluster, tasks=[task])
    containers = []
    try:
        for container in items['tasks'][0]['containers']:
            containers.append(container['name'])
    except IndexError:
        print("There is a problem with list containers")
        exit()

    return containers


def index_exists(ls, i):
    return (0 <= i < len(ls)) or (-len(ls) <= i < 0)


def get_command(args):
    if index_exists(args, 2):
        return args[2]
    else:
        return "/bin/sh"


def validate_region(args):
    try:
        args[1]
    except IndexError:
        print("Region not set, please pass region as first argument.")
        exit()


def signal_handler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main(sys.argv)
