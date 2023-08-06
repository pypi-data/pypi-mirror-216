from typing import Literal, Optional, Type

from sym.shared.cli.helpers.os import has_command
from sym.shared.cli.helpers.util import requires_all_imports

from sym.cli.helpers.config import Config
from sym.cli.helpers.params import is_sso_enabled

from ..errors import SAMLClientNotFound
from . import import_all
from .saml_client import SAMLClient

SAMLClientName = Literal["auto", "aws-okta", "saml2aws", "aws-profile", "aws-config"]
AUTO_EXCLUDED_SAML_CLIENT_NAMES = ["aws-profile"]


@requires_all_imports(import_all)
def option_values():
    return ["auto"] + [x.option_value for x in SAMLClient.sorted_subclasses()]


@requires_all_imports(import_all)
def choose_saml_client(
    saml_client_name: SAMLClientName, none_ok=False
) -> Optional[Type[SAMLClient]]:
    if saml_client_name == "auto":
        excludes = AUTO_EXCLUDED_SAML_CLIENT_NAMES
        if Config.is_logged_in() and not is_sso_enabled():
            excludes.append("aws-config")
        for client in SAMLClient.sorted_subclasses():
            if client.option_value not in excludes and has_command(client.binary):
                return client
    else:
        for client in SAMLClient.sorted_subclasses():
            if client.option_value == saml_client_name:
                return client

    if not none_ok:
        raise SAMLClientNotFound()
