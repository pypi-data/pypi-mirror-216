"""
There is no client SDK for Python, Patrick provided some example code
for how to use the flag evaluation API from Python
"""
import base64
import json
from typing import List, NamedTuple, Optional, Tuple, TypeVar

import click
import requests


class FlagsConfig(NamedTuple):
    """Config for the LD Client SDK API"""

    client_id: str
    api_url: str = "app.launchdarkly.com"


def _cli_context(email: str) -> dict:
    """Construct a multitype LD context for flag evaluation"""
    return {
        "kind": "multi",
        "sym-cli": {"key": "prod"},
        "sym-user": {"key": email},
    }


def _resource_context(email: str, env: str) -> dict:
    """
    Construct a multitype LD contxt that includes the
    currently requested SSH resource, so we can find the
    correctly mapped flag
    """
    cli_context = _cli_context(email)
    cli_context["sym-ssh-environment"] = {"key": env}
    return cli_context


def _encode_context(context_dict: dict) -> str:
    """Properly encode context (per Patrick)"""
    json_str = json.dumps(context_dict)
    base64_str = base64.urlsafe_b64encode(json_str.encode("utf-8"))
    return base64_str.decode()


def _evaluate_context(context_json: dict, config: FlagsConfig) -> Optional[dict]:
    """There is no client SDK for Python, Patrick provided this example"""
    ctx = _encode_context(context_json)
    url = f"https://{config.api_url}/sdk/evalx/{config.client_id}/contexts/{ctx}"
    try:
        response = requests.get(url)
        data = response.json()
        if code := data.get("code"):
            message = data.get("message")
            click.secho(
                (
                    f"Warning: unable to look up resource configuration in LaunchDarkly.\n"
                    f"Use --saml-config aws-config and specify the AWS profile name as your sym resource to connect.\n\n"
                    f"Code: '{code}'\n"
                    f"Message: '{message}'\n"
                ),
                err=True,
                fg="yellow",
                bold=True,
            )
            return None
        return data
    except requests.exceptions.RequestException as ex:
        click.secho(
            (
                f"Warning: unable to look up resource configuration in LaunchDarkly.\n"
                f"Use --saml-config aws-config and specify the AWS profile name as your sym resource to connect.\n\n"
                f"{ex}"
            ),
            err=True,
            fg="yellow",
            bold=True,
        )
        return None


T = TypeVar("T")


def _flag_value(flags: dict, flag_name: str, default: T) -> T:
    if flag := flags.get(flag_name):
        return flag.get("value", default)
    return default


def get_sso_profile(resource: str, email: str, config: FlagsConfig) -> Tuple[bool, str]:
    """
    Look up the AWS SSO profile name for the given requested resource name
    Users request access to things like "production" but the config in AWS config
    has a different name.
    """
    context_json = _resource_context(email, resource)
    sso_enabled = False
    sso_profile = ""
    if flags := _evaluate_context(context_json, config):
        sso_enabled = _flag_value(flags, "sym-sso-enabled", sso_enabled)
        sso_profile = _flag_value(flags, "sym-ssh-sso-profile", sso_profile)
    return (sso_enabled, sso_profile)


def get_resource_list(email: str, config: FlagsConfig) -> Tuple[bool, List[str]]:
    """
    Look up all possible resources in the CLI context. This overrides
    the hard-coded list in params
    """
    context_json = _cli_context(email)
    sso_enabled = False
    resource_list: List[str] = []
    if flags := _evaluate_context(context_json, config):
        sso_enabled = _flag_value(flags, "sym-sso-enabled", sso_enabled)
        resource_list = _flag_value(flags, "sym-cli-resource-list", resource_list)
    return (sso_enabled, resource_list)
