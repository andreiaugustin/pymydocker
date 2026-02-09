from omnis_calls import sendResponse, sendError, sendEvent

import docker
from docker.errors import DockerException


def is_running(param, response):
    try:
        client = docker.from_env()
        client.ping()
        return sendResponse({"running": True}, response)
    except Exception as e:
        return sendResponse({"running": False}, response)


def run_container(param, response):
    try:
        client = docker.from_env()

        ports = None
        if param.get("ports") and param["ports"] != "None":
            ports = {param["ports"]["C1"]: param["ports"]["C2"]}

        container = client.containers.run(
            image=param["image"],
            command=None if param.get("command") == "None" else param.get("command"),
            auto_remove=param.get("auto_remove", False),
            detach=True,
            name=None if param.get("name") == "None" else param.get("name"),
            ports=ports,
        )

        return sendResponse(
            {
                "container": {
                    "id": container.id,
                    "short_id": container.short_id,
                    "name": container.name,
                    "image": container.attrs["Config"]["Image"],
                }
            },
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def build_image(param, response):
    try:
        client = docker.from_env()
        image, logs = client.images.build(path=param["path"], tag=param["tag"])

        return sendResponse(
            {"image": {"id": image.id, "short_id": image.short_id, "tags": image.tags}},
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def get_image(param, response):
    try:
        client = docker.from_env()
        image = client.images.get(param["name"])

        return sendResponse(
            {"image": {"id": image.id, "short_id": image.short_id, "tags": image.tags}},
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def prune_images(param, response):
    try:
        client = docker.from_env()
        result = client.images.prune()

        return sendResponse(
            {
                "images_deleted": result["ImagesDeleted"],
                "space_reclaimed": result["SpaceReclaimed"],
            },
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def pull_image(param, response):
    try:
        client = docker.from_env()
        image = client.images.pull(
            param["repository"],
            tag=param.get("tag", "latest"),
        )

        return sendResponse(
            {"image": {"id": image.id, "short_id": image.short_id, "tags": image.tags}},
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def push_image(param, response):
    try:
        client = docker.from_env()
        result = client.images.push(
            param["repository"],
            tag=param.get("tag", "latest"),
            stream=True,
            decode=True,
        )

        return sendResponse({"result": list(result)}, response)
    except DockerException as e:
        return sendError(str(e), response)


def search_images(param, response):
    try:
        client = docker.from_env()
        results = client.images.search(
            param["term"],
            limit=param.get("limit", 25),
        )

        return sendResponse({"results": results}, response)
    except DockerException as e:
        return sendError(str(e), response)


def remove_image(param, response):
    try:
        client = docker.from_env()
        client.images.remove(
            param["image"],
            force=param.get("force", False),
        )

        return sendResponse({"removed": param["image"]}, response)
    except DockerException as e:
        return sendError(str(e), response)


def data_usage(param, response):
    try:
        client = docker.from_env()
        df_data = client.df()

        return sendResponse(
            {
                "data": df_data,
            },
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def list_secrets(param, response):
    try:
        client = docker.from_env()
        secrets = client.secrets.list()

        return sendResponse(
            {
                "secrets": [
                    {
                        "id": s.id,
                        "short_id": s.short_id,
                        "name": s.name,
                    }
                    for s in secrets
                ]
            },
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def list_networks(param, response):
    try:
        client = docker.from_env()
        networks = client.networks.list()

        return sendResponse(
            {
                "networks": [
                    {
                        "id": n.id,
                        "short_id": n.short_id,
                        "name": n.name,
                        "driver": n.attrs["Driver"],
                    }
                    for n in networks
                ]
            },
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def list_volumes(param, response):
    try:
        client = docker.from_env()
        volumes = client.volumes.list()

        return sendResponse(
            {
                "volumes": [
                    {
                        "id": v.id,
                        "short_id": v.short_id,
                        "name": v.name,
                        "mountpoint": v.attrs["Mountpoint"],
                    }
                    for v in volumes
                ]
            },
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def list_images(param, response):
    try:
        client = docker.from_env()
        images = client.images.list()

        return sendResponse(
            {
                "images": [
                    {
                        "id": i.id,
                        "labels": i.labels,
                        "short_id": i.short_id,
                        "tags": i.tags,
                    }
                    for i in images
                ]
            },
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)


def list_containers(param, response):
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)

        return sendResponse(
            {
                "containers": [
                    {
                        "id": c.id,
                        "image": c.attrs["Config"]["Image"],
                        "labels": c.attrs["Config"]["Labels"],
                        "name": c.name,
                        "short_id": c.short_id,
                        "status": c.status,
                    }
                    for c in containers
                ]
            },
            response,
        )
    except DockerException as e:
        return sendError(str(e), response)
