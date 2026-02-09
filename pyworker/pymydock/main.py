from omnis_calls import sendResponse, sendError, sendEvent

import docker
from docker.errors import DockerException

def is_running(param, response):
    try:
        client = docker.from_env()
        client.ping()
        return sendResponse(
            {'running': True},
            response
        )
    except (Exception) as e:
        return sendResponse(
            {'running': False},
            response
        )

def list_images(param, response):
    try:
        client = docker.from_env()
        images = client.images.list()

        return sendResponse(
            {
                "images": [
                    {
                        "id": img.id,
                        "tags": img.tags,
                        "short_id": img.short_id
                    }
                    for img in images
                ]
            },
            response
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
                        "name": c.name,
                        "image": c.image.tags,
                        "status": c.status,
                        "short_id": c.short_id
                    }
                    for c in containers
                ]
            },
            response
        )
    except DockerException as e:
        return sendError(str(e), response)

