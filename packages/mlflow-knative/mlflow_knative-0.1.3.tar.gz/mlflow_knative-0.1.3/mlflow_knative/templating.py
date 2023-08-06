"""Templated Knative manifests helper module."""
import logging
from importlib.resources import files
from pathlib import Path
from string import Template
from typing import Any

import yaml

DEFAULT_SERVICE_TEMPLATE = Template(
    files(__package__).joinpath("service.yaml").read_text()
)

logger = logging.getLogger(__package__)


def get_service_body(
    namespace: str, name: str, image: str, template_path: str | Path | None = None
) -> Any:
    """Substitute variables in a Knative service template and return the result.

    If no template file is provided, a default template is used.
    """
    template = DEFAULT_SERVICE_TEMPLATE
    if template_path is not None:
        logger.debug("Loading template from '%s' for service '%s'", template_path, name)

        with open(template_path) as file:
            template = Template(file.read())
    else:
        logger.debug("Using default template for service '%s'", name)

    return yaml.safe_load(
        template.substitute(
            namespace=namespace,
            name=name,
            image=image,
        )
    )
