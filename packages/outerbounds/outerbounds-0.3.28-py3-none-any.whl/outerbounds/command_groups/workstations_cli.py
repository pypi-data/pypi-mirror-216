import click
import yaml
import requests
import base64
import datetime
import hashlib
import json
import os
from os import path
from pathlib import Path
from ..utils import kubeconfig, metaflowconfig
from requests.exceptions import HTTPError


@click.group()
def cli(**kwargs):
    pass


@cli.command(help="Generate a token to use your cloud workstation", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
def generate_workstation_token(config_dir=None, profile=None):
    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        auth_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_AUTH_SERVER"
        )
        k8s_response = requests.get(
            f"{auth_url}/generate/k8s", headers={"x-api-key": metaflow_token}
        )
        try:
            k8s_response.raise_for_status()
            k8s_response_json = k8s_response.json()
            token = k8s_response_json["token"]
            token_data = base64.b64decode(token.split(".")[1] + "==")
            exec_creds = {
                "kind": "ExecCredential",
                "apiVersion": "client.authentication.k8s.io/v1beta1",
                "spec": {},
                "status": {
                    "token": token,
                    "expirationTimestamp": datetime.datetime.fromtimestamp(
                        json.loads(token_data)["exp"], datetime.timezone.utc
                    ).isoformat(),
                },
            }
            click.echo(json.dumps(exec_creds))
        except HTTPError:
            click.secho("Failed to generate workstation token.", fg="red")
            click.secho("Error: {}".format(json.dumps(k8s_response.json(), indent=4)))
    except Exception as e:
        click.secho("Failed to generate workstation token.", fg="red")
        click.secho("Error: {}".format(str(e)))


@cli.command(help="Configure a cloud workstation", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
@click.option(
    "-b",
    "--binary",
    default="outerbounds",
    help="Path to the location of your outerbounds binary",
)
def configure_cloud_workstation(config_dir=None, profile=None, binary=None):
    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        auth_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_AUTH_SERVER"
        )
        k8s_response = requests.get(
            f"{auth_url}/generate/k8s", headers={"x-api-key": metaflow_token}
        )

        try:
            k8s_response.raise_for_status()
            k8s_response_json = k8s_response.json()
            token_data = base64.b64decode(
                k8s_response_json["token"].split(".")[1] + "=="
            )
            ws_namespace = "ws-{}".format(
                hashlib.md5(
                    bytes(json.loads(token_data)["username"], "utf-8")
                ).hexdigest()
            )

            kubeconfig.set_context(
                "outerbounds-workstations",
                "outerbounds-cluster",
                ws_namespace,
                "obp-user",
            )
            kubeconfig.set_cluster(
                "outerbounds-cluster", k8s_response_json["endpoint"], True
            )
            kubeconfig.add_user_with_exec_credential(
                "obp-user", binary, config_dir, profile
            )
            kubeconfig.use_context("outerbounds-workstations")
        except HTTPError:
            click.secho("Failed to generate workstation token.", fg="red")
            click.secho("Error: {}".format(json.dumps(k8s_response.json(), indent=4)))
    except Exception as e:
        click.secho("Failed to configure cloud workstation", fg="red")
        click.secho("Error: {}".format(str(e)))


@cli.command(help="List all existing workstations", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
def list_workstations(config_dir=None, profile=None):
    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        api_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_API_SERVER"
        )
        workstations_response = requests.get(
            f"{api_url}/v1/workstations", headers={"x-api-key": metaflow_token}
        )
        try:
            workstations_response.raise_for_status()
            click.echo(json.dumps(workstations_response.json(), indent=4))
        except HTTPError:
            click.secho("Failed to generate workstation token.", fg="red")
            click.secho(
                "Error: {}".format(json.dumps(workstations_response.json(), indent=4))
            )
    except Exception as e:
        click.secho("Failed to list workstations", fg="red")
        click.secho("Error: {}".format(str(e)))


@cli.command(help="Hibernate workstation", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
@click.option(
    "-w",
    "--workstation",
    default="",
    help="The ID of the workstation to hibernate",
)
def hibernate_workstation(config_dir=None, profile=None, workstation=None):
    if workstation is None or workstation == "":
        click.secho("Please specify a workstation ID", fg="red")
        return
    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        api_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_API_SERVER"
        )
        hibernate_response = requests.put(
            f"{api_url}/v1/workstations/hibernate/{workstation}",
            headers={"x-api-key": metaflow_token},
        )
        try:
            hibernate_response.raise_for_status()
            response_json = hibernate_response.json()
            if len(response_json) > 0:
                click.echo(json.dumps(response_json, indent=4))
            else:
                click.secho("Success", fg="green", bold=True)
        except HTTPError:
            click.secho("Failed to hibernate workstation", fg="red")
            click.secho(
                "Error: {}".format(json.dumps(hibernate_response.json(), indent=4))
            )
    except Exception as e:
        click.secho("Failed to hibernate workstation", fg="red")
        click.secho("Error: {}".format(str(e)))


@cli.command(help="Restart workstation to the int", hidden=True)
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
@click.option(
    "-w",
    "--workstation",
    default="",
    help="The ID of the workstation to restart",
)
def restart_workstation(config_dir=None, profile=None, workstation=None):
    if workstation is None or workstation == "":
        click.secho("Please specify a workstation ID", fg="red")
        return
    try:
        metaflow_token = metaflowconfig.get_metaflow_token_from_config(
            config_dir, profile
        )
        api_url = metaflowconfig.get_sanitized_url_from_config(
            config_dir, profile, "OBP_API_SERVER"
        )
        restart_response = requests.put(
            f"{api_url}/v1/workstations/restart/{workstation}",
            headers={"x-api-key": metaflow_token},
        )
        try:
            restart_response.raise_for_status()
            response_json = restart_response.json()
            if len(response_json) > 0:
                click.echo(json.dumps(response_json, indent=4))
            else:
                click.secho("Success", fg="green", bold=True)
        except HTTPError:
            click.secho("Failed to restart workstation", fg="red")
            click.secho(
                "Error: {}".format(json.dumps(restart_response.json(), indent=4))
            )
    except Exception as e:
        click.secho("Failed to restart workstation", fg="red")
        click.secho("Error: {}".format(str(e)))
