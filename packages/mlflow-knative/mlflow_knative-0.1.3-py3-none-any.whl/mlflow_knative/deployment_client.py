"""MLflow Knative Deployment Plugin.

The plugin implements a MLflow deployment client for Knative targets
as well as helper functions.

Implementing: https://mlflow.org/docs/latest/_modules/mlflow/deployments/base.html
"""
import logging
import warnings
from http import HTTPStatus

import docker
import kubernetes
import mlflow
import pandas
import requests

from .knative import KnativeServingV1Api, KnativeTimeoutError
from .mlflow_docker import push_model_as_image
from .templating import get_service_body

MLFLOW_MODEL_FLAVOR_PYFUNC = "python_function"
IMAGE_REPOSITORY_CONFIG_KEY = "image_repository"
IMAGE_TAG_CONFIG_KEY = "image_tag"
DEFAULT_IMAGE_TAG = "latest"

NAMESPACE_CONFIG_KEY = "namespace"
DEFAULT_NAMESPACE = "default"

TEMPLATE_PATH_CONFIG_KEY = "service_template"

logger = logging.getLogger(__package__)


class EndpointArgumentNotSupported(mlflow.exceptions.MlflowException):
    """Raised when the unsupported 'endpoint' argument is used."""

    def __init__(self):
        super().__init__(
            "'endpoint' argument not supported by Knative deployment plugin."
        )


class KnativeDeploymentClient(mlflow.deployments.BaseDeploymentClient):
    """Knative Deployment Client for MLflow."""

    def __init__(self, uri: str):
        super().__init__(target_uri=uri)
        self._docker_client = docker.from_env()
        self._kubernetes_client = kubernetes.config.new_client_from_config(
            context=uri.removeprefix("knative:/")
        )

    def create_deployment(
        self,
        name: str,
        model_uri: str,
        flavor: str | None = None,
        config: dict[str, str] | None = None,
        endpoint: str | None = None,
    ) -> dict[str, str]:
        """Deploy a model to a Knative target."""
        if endpoint:
            raise EndpointArgumentNotSupported

        flavor = flavor if flavor is not None else MLFLOW_MODEL_FLAVOR_PYFUNC
        if flavor != MLFLOW_MODEL_FLAVOR_PYFUNC:
            raise mlflow.exceptions.MlflowException(
                f"only '{MLFLOW_MODEL_FLAVOR_PYFUNC}' model flavor is supported."
            )

        logger.info(
            "Creating deployment '%s' from model '%s' targetting '%s'",
            name,
            model_uri,
            self.target_uri,
        )

        config = config if config is not None else {}
        tag = config.get(IMAGE_TAG_CONFIG_KEY, DEFAULT_IMAGE_TAG)
        image = push_model_as_image(
            self._docker_client, model_uri, config[IMAGE_REPOSITORY_CONFIG_KEY], tag
        )

        with self._kubernetes_client as kubernetes_client:
            knative_api = KnativeServingV1Api(kubernetes_client)
            namespace = config.get(NAMESPACE_CONFIG_KEY, DEFAULT_NAMESPACE)
            try:
                service = knative_api.create_namespaced_service(
                    namespace=namespace,
                    body=get_service_body(
                        namespace=namespace,
                        name=name,
                        image=image,
                        template_path=config.get(TEMPLATE_PATH_CONFIG_KEY),
                    ),
                )
            except kubernetes.client.rest.ApiException as error:
                if error.status == HTTPStatus.CONFLICT:
                    raise mlflow.exceptions.MlflowException(
                        f"a deployment with name '{name}' "
                        f"already exists in namespace '{namespace}'."
                    )
                else:
                    raise mlflow.exceptions.MlflowException(
                        f"Kubernetes API error ({error.status})"
                    ) from error
            except KnativeTimeoutError as error:
                raise mlflow.exceptions.MlflowException(
                    f"service creation failed: {str(error)}"
                )

        return {"name": service["metadata"]["name"], "flavor": flavor}

    def update_deployment(
        self,
        name: str,
        model_uri: str,
        flavor: str | None = None,
        config: dict[str, str] | None = None,
        endpoint: str | None = None,
    ) -> dict[str, str]:
        """Update a model on a Knative target."""
        if endpoint:
            raise EndpointArgumentNotSupported

        flavor = flavor if flavor is not None else MLFLOW_MODEL_FLAVOR_PYFUNC
        if flavor != MLFLOW_MODEL_FLAVOR_PYFUNC:
            raise mlflow.exceptions.MlflowException(
                f"only '{MLFLOW_MODEL_FLAVOR_PYFUNC}' model flavor is supported."
            )

        logger.info(
            "Updating deployment '%s' from model '%s' targetting '%s'",
            name,
            model_uri,
            self.target_uri,
        )

        config = config if config is not None else {}
        tag = config.get(IMAGE_TAG_CONFIG_KEY, DEFAULT_IMAGE_TAG)
        image = push_model_as_image(
            self._docker_client, model_uri, config[IMAGE_REPOSITORY_CONFIG_KEY], tag
        )

        with self._kubernetes_client as kubernetes_client:
            knative_api = KnativeServingV1Api(kubernetes_client)
            namespace = config.get(NAMESPACE_CONFIG_KEY, DEFAULT_NAMESPACE)
            try:
                service = knative_api.update_namespaced_service(
                    namespace=namespace,
                    name=name,
                    body=get_service_body(
                        namespace=namespace,
                        name=name,
                        image=image,
                        template_path=config.get(TEMPLATE_PATH_CONFIG_KEY),
                    ),
                )
            except kubernetes.client.rest.ApiException as error:
                if error.status == HTTPStatus.NOT_FOUND:
                    raise mlflow.exceptions.MlflowException(
                        f"no deployment with name '{name}' "
                        f"found in namespace '{namespace}'."
                    )
                else:
                    raise mlflow.exceptions.MlflowException(
                        f"Kubernetes API error ({error.status})"
                    ) from error
            except KnativeTimeoutError as error:
                raise mlflow.exceptions.MlflowException(
                    f"service update failed: {str(error)}"
                )

        return {"name": service["metadata"]["name"], "flavor": flavor}

    def delete_deployment(
        self,
        name: str,
        config: dict[str, str] | None = None,
        endpoint: str | None = None,
    ) -> None:
        """Delete a model on a Knative target."""
        if endpoint:
            raise EndpointArgumentNotSupported

        logger.info("Deleting deployment '%s' on target '%s'", name, self.target_uri)

        config = config if config is not None else {}

        with self._kubernetes_client as kubernetes_client:
            knative_api = KnativeServingV1Api(kubernetes_client)
            namespace = config.get(NAMESPACE_CONFIG_KEY, DEFAULT_NAMESPACE)
            try:
                knative_api.delete_namespaced_service(namespace=namespace, name=name)
            except kubernetes.client.rest.ApiException as error:
                if error.status == HTTPStatus.NOT_FOUND:
                    raise mlflow.exceptions.MlflowException(
                        f"no deployment with name '{name}' "
                        f"found in namespace '{namespace}'."
                    )
                else:
                    raise mlflow.exceptions.MlflowException(
                        f"Kubernetes API error ({error.status})"
                    ) from error

    def list_deployments(self, endpoint: str | None = None) -> list[dict[str, str]]:
        """List deployments on a Knative target (across all namespaces)."""
        if endpoint:
            raise EndpointArgumentNotSupported

        with self._kubernetes_client as kubernetes_client:
            core_api = kubernetes.client.CoreV1Api(kubernetes_client)
            knative_api = KnativeServingV1Api(kubernetes_client)

            return [
                {
                    "name": service["metadata"]["name"],
                    "namespace": service["metadata"]["namespace"],
                    "url": service["status"]["url"],
                }
                for namespace in core_api.list_namespace().items
                for service in knative_api.list_namespaced_service(
                    namespace=namespace.metadata.name
                )["items"]
            ]

    def get_deployment(self, name: str, endpoint: str | None = None) -> dict[str, str]:
        """Get metadata for a deployment on a Knative target (across all namespaces).

        Note: this fails if multiple deployments with the same name exist across
        multiple namespaces.
        Unfortunately MLflow deployment client interface does not allow passing
        a `config` dict with a specified namespace to this method.
        """
        if endpoint:
            raise EndpointArgumentNotSupported

        with self._kubernetes_client as kubernetes_client:
            core_api = kubernetes.client.CoreV1Api(kubernetes_client)
            knative_api = KnativeServingV1Api(kubernetes_client)

            deployments = []
            for namespace in core_api.list_namespace().items:
                try:
                    service = knative_api.get_namespaced_service(
                        namespace=namespace.metadata.name, name=name
                    )
                    deployments.append(
                        {
                            "name": service["metadata"]["name"],
                            "namespace": service["metadata"]["namespace"],
                            "url": service["status"]["url"],
                        }
                    )
                except kubernetes.client.rest.ApiException as error:
                    if error.status == HTTPStatus.NOT_FOUND:
                        pass

            try:
                (deployment,) = deployments
            except ValueError as error:
                raise mlflow.exceptions.MlflowException(
                    "must return exactly one deployment matching the provided name."
                ) from error

            return deployment

    def predict(
        self,
        deployment_name: str | None = None,
        inputs: pandas.DataFrame | None = None,
        endpoint: str | None = None,
    ) -> list[dict[str, str]]:
        """Compute predictions on inputs using the specified Knative deployment."""
        if not deployment_name:
            raise mlflow.exceptions.MlflowException("a deployment name is required.")

        if endpoint:
            raise EndpointArgumentNotSupported

        inputs = inputs if inputs is not None else pandas.DataFrame()

        deployment = self.get_deployment(deployment_name)
        try:
            response = requests.post(
                f"{deployment['url']}/invocations",
                headers={"Content-Type": "application/json"},
                data=f"{{\"dataframe_split\": {inputs.to_json(orient='split')}}}",
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as error:
            raise mlflow.exceptions.MlflowException(
                "could not connect to the deployment, are you sure "
                f"the service URL '{deployment['url']}' is publicly available?"
            ) from error
        except requests.exceptions.HTTPError as error:
            raise mlflow.exceptions.MlflowException(
                "deployment request HTTP error."
            ) from error

        return response.json()


def run_local(
    name: str,
    model_uri: str,
    flavor: str | None = None,
    config: dict[str, str] | None = None,
) -> None:
    """Run a model locally and serve it as an HTTP ReST API.

    Internally, we simply use `model.serve()`.
    This is mostly useful to check the "pyfunc" works before packaging.
    """
    flavor = flavor if flavor is not None else MLFLOW_MODEL_FLAVOR_PYFUNC
    if flavor != MLFLOW_MODEL_FLAVOR_PYFUNC:
        raise mlflow.exceptions.MlflowException(
            f"only '{MLFLOW_MODEL_FLAVOR_PYFUNC}' model flavor is supported."
        )

    config = config if config is not None else {}

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = mlflow.pyfunc.load_model(model_uri)

    model.serve(enable_mlserver=True, host=config.get("host"), port=config.get("port"))


def target_help() -> str | None:
    """MLflow deployments Knative target.

    * A `target_uri` must be constructed with the scheme "knative:/<kube context>".
      (e.g. for AWS EKS clusters, the context is the ARN of the cluster
      https://docs.aws.amazon.com/eks/latest/userguide/connecting-cluster.html)

    * `create_deployment` and `update_deployment` support `config` fields:

      * `image_repository` which specifies the Docker repository to push images
        used by Knative services deployments.

      * `image_tag` which specifies the Docker image tag for the image.

      * `namespace` is the Kubernetes cluster namespace for the service.

      * `service_template` which allows providing a file path to a template YAML
        manifest for the Knative service to deploy.
        Templated values `name`, `namespace` and `image` are replaced.

    * When using `predict` make sure the Knative service is publicly available.
    """
    return target_help.__doc__
