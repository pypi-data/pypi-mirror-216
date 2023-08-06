"""MLflow Docker helpers."""
import io
import json
import logging
import warnings
from contextlib import redirect_stderr, redirect_stdout

import docker
import mlflow

logger = logging.getLogger(__package__)


def _mlflow_build_docker_image(model_uri: str, image: str) -> None:
    logger.info("Building image '%s' from '%s'", image, model_uri)

    with warnings.catch_warnings(), redirect_stdout(io.StringIO()), redirect_stderr(
        io.StringIO()
    ) as output:
        warnings.simplefilter("ignore")
        mlflow.models.build_docker(
            model_uri=model_uri,
            name=image,
            enable_mlserver=True,
        )
        build_log = output.getvalue()
        if "ERROR" in build_log:
            raise mlflow.exceptions.MlflowException(build_log)


def _docker_safe_push_image(client, repository: str, tag: str | None = None) -> None:
    logger.info("Pushing image '%s:%s'", repository, tag)

    response = client.images.push(repository, tag=tag)
    data = json.loads(response.strip().split("\n").pop())
    if "error" in data and data["error"]:
        raise docker.errors.APIError(data["error"])


def push_model_as_image(
    client, model_uri: str, repository: str, tag: str | None = None
) -> str:
    """Build a Docker image from a MLFlow model, push it to a Docker repository."""
    image = f"{repository}:{tag}" if tag else repository
    _mlflow_build_docker_image(model_uri, image)

    try:
        _docker_safe_push_image(client, repository, tag)
    except docker.errors.APIError as error:
        raise mlflow.exceptions.MlflowException(
            f"failed to push image '{image}'."
        ) from error

    return image
