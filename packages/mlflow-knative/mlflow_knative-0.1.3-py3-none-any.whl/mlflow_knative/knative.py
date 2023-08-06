"""Knative Serving API module with event handling helpers."""
import logging
import time

import kubernetes

KUBERNETES_EVENT_TYPE_MODIFIED = "MODIFIED"

KNATIVE_RESOURCE_GROUP = "serving.knative.dev"
KNATIVE_SERVICE_PLURAL = "services"

WATCH_TIMEOUT = 600

logger = logging.getLogger(__package__)


def _handle_namespaced_service_is_ready_event(
    namespace: str, name: str, event: dict
) -> bool:
    """Handle the ready event for Knative services."""
    try:
        if event["type"] != KUBERNETES_EVENT_TYPE_MODIFIED:
            return False

        metadata = event["object"]["metadata"]
        if metadata["namespace"] != namespace or metadata["name"] != name:
            return False

        return all(
            condition["status"] == str(True)
            for condition in event["object"]["status"]["conditions"]
        )
    except KeyError:
        return False


class KnativeTimeoutError(Exception):
    """Raised when the creation or update of a Knative services reaches a timeout."""


class KnativeServingV1Api:
    """Knative Serving v1 API.

    All methods are namespaced, only top-level Service resource is implemented.

    Unlike APIs provided by the Kubernetes client for Python, it waits for service
    readiness by default.
    """

    RESOURCE_VERSION = "v1"

    def __init__(self, client: kubernetes.client.ApiClient):
        self._custom_objects_api = kubernetes.client.CustomObjectsApi(client)
        self._watch = kubernetes.watch.Watch()

    def _get_knative_namespaced_service_params(self, namespace: str) -> dict[str, str]:
        return {
            "group": KNATIVE_RESOURCE_GROUP,
            "version": self.RESOURCE_VERSION,
            "plural": KNATIVE_SERVICE_PLURAL,
            "namespace": namespace,
        }

    def create_namespaced_service(self, namespace: str, body: dict) -> dict:
        """Create a Knative service."""
        params = self._get_knative_namespaced_service_params(namespace)
        service = self._custom_objects_api.create_namespaced_custom_object(
            **params, body=body
        )

        logger.info(
            "Waiting for service '%s' to be ready in namespace '%s'",
            service["metadata"]["name"],
            service["metadata"]["namespace"],
        )
        start = time.time()
        for event in self._watch.stream(
            self._custom_objects_api.list_namespaced_custom_object,
            timeout_seconds=WATCH_TIMEOUT,
            **params,
        ):
            if _handle_namespaced_service_is_ready_event(
                namespace=service["metadata"]["namespace"],
                name=service["metadata"]["name"],
                event=event,
            ):
                self._watch.stop()
                logger.info(
                    "Service '%s' ready in namespace '%s' after %ss",
                    service["metadata"]["name"],
                    service["metadata"]["namespace"],
                    int(time.time() - start),
                )
                return service

        raise KnativeTimeoutError(
            f"timeout during service '{service['metadata']['name']}' creation."
        )

    def update_namespaced_service(self, namespace: str, name: str, body: dict) -> dict:
        """Update a Knative service."""
        params = self._get_knative_namespaced_service_params(namespace)
        service = self.get_namespaced_service(namespace=namespace, name=name)
        updated_service = self._custom_objects_api.patch_namespaced_custom_object(
            **params, name=name, body=body
        )

        # Don't wait for the service to become ready if Knative generation is unchanged:
        if (
            updated_service["metadata"]["generation"]
            == service["metadata"]["generation"]
        ):
            return updated_service

        logger.info(
            "Waiting for service '%s' to be ready in namespace '%s'",
            updated_service["metadata"]["name"],
            updated_service["metadata"]["namespace"],
        )
        start = time.time()
        for event in self._watch.stream(
            self._custom_objects_api.list_namespaced_custom_object,
            timeout_seconds=WATCH_TIMEOUT,
            **params,
        ):
            if _handle_namespaced_service_is_ready_event(
                namespace=updated_service["metadata"]["namespace"],
                name=updated_service["metadata"]["name"],
                event=event,
            ):
                self._watch.stop()
                logger.info(
                    "Service '%s' ready in namespace '%s' after %ss",
                    updated_service["metadata"]["name"],
                    updated_service["metadata"]["namespace"],
                    int(time.time() - start),
                )
                return updated_service

        raise KnativeTimeoutError(
            f"timeout during service '{updated_service['metadata']['name']}' update."
        )

    def delete_namespaced_service(self, namespace: str, name: str) -> dict:
        """Delete a Knative service."""
        return self._custom_objects_api.delete_namespaced_custom_object(
            **self._get_knative_namespaced_service_params(namespace), name=name
        )

    def get_namespaced_service(self, namespace: str, name: str) -> dict:
        """Get a Knative service."""
        return self._custom_objects_api.get_namespaced_custom_object(
            **self._get_knative_namespaced_service_params(namespace), name=name
        )

    def list_namespaced_service(self, namespace: str) -> dict:
        """List Knative services."""
        return self._custom_objects_api.list_namespaced_custom_object(
            **self._get_knative_namespaced_service_params(namespace)
        )
