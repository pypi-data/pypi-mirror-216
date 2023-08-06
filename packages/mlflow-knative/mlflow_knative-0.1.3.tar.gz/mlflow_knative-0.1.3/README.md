MLflow Knative Deployment Plugin
================================

[MLflow](https://mlflow.org/) plugin adding a [Knative](https://knative.dev/docs/) deployment client to MLflow CLI and Python API.

Note: [MLServer (V2 Inference API)](https://mlflow.org/docs/latest/models.html#serving-with-mlserver) is enabled for all Docker builds.


Requirements
------------

- Python 3.10+  
- MLflow 2+  
- Docker  

The target Kubernetes cluster must be running Knative 1.10+.


Installation
------------

```console
pip install mlflow-knative
```


Getting Started
---------------

A Kubernetes context is required to define the Knative target.  
You can list available contexts with `kubectl config get-contexts`.

Make sure Docker is running locally if you intend create or update a deployment, as this is required to build an image from the MLflow model.

The plugin adds support for a `knative` target scheme to the [`mlflow deployments` CLI](https://mlflow.org/docs/latest/cli.html#mlflow-deployments).

Setting the `image_repository` config key is required to make the Docker image of the model available for deployment by Knative. Additionally you may also provide an image tag with the `image_tag` config key (defaults to `latest`).

```console
mlflow deployments create \
  --target knative:/<context> \
  --name <deployment-name> \
  --model-uri models:/<model-name>/<model-version> \
  --config image_repository=<image-repository-URI> \
  --config image_tag=<image-tag>
```

The plugin provides detailed target help.

```console
mlflow deployments help --target knative
```

All features are also available as a [Python API deployment client](https://mlflow.org/docs/latest/python_api/mlflow.deployments.html).

```python
from mlflow.deployments import get_deploy_client

client = get_deploy_client("knative:/my-cluster")
client.create_deployment(
	"hello-world",
	"models:/hello-world/1",
	config={
		"image_repository": "hello-world"
	}
)
```


Using a Private Image Repository
--------------------------------

To use a private Docker image repository, simply run `docker login` defore running the deployment client, then use the full repository URI as value for the `image_repository` config key.

```console
docker login --username <username> --password-stdin <private-repository-URL>

# If using AWS ECR:
aws ecr get-login-password | docker login --username AWS --password-stdin <private-repository-URL>

mlflow deployments create \
  --target knative:/<context> \
  --name <deployment-name> \
  --model-uri models:/<model-name>/<model-version> \
  --config image_repository=<image-repository-URI>  # e.g.: 000000000000.dkr.ecr.eu-west-3.amazonaws.com/model-name
```

Using a Remote MLflow Model Registry
------------------------------------

Set an environment variable as `export MLFLOW_TRACKING_URI=<tracking-server-uri>` to use a remote MLflow model registry.
This also works with a private model registry secured with OAuth 2, using the [MLflow OIDC Client Plugin](https://pypi.org/project/mlflow-oidc-client/).


Knative Service Configuration
-----------------------------

The deployment client can use any available namespace on the target cluster by setting the `namespace` config key. The default value is `default`.

```console
mlflow deployments create \
  --target knative:/<context> \
  --name <deployment-name> \
  --model-uri models:/<model-name>/<model-version> \
  --config image_repository=<image-repository-URI> \
  --config namespace=<my-namespace>
```


To deploy a Knative service with a [custom templated manifest](https://knative.dev/docs/serving/services/creating-services/), set the `service_template` config key. The value is a path to the YAML manifest you will be using.

```console
mlflow deployments create \
  --target knative:/<context> \
  --name <deployment-name> \
  --model-uri models:/<model-name>/<model-version> \
  --config image_repository=<image-repository-URI> \
  --config service_template=<path/to/manifest>
```

`$name`, `$namespace` and `$image` templated values are respectively the deployment name, the provided namespace (or "default"), the image determined from the provided image repository and tag.


License
-------

This project is licensed under the terms of the MIT license.


A [yzr](https://www.yzr.ai/) Free and Open Source project.
