import os
from dataclasses import InitVar, dataclass, field
from typing import Dict, List, NamedTuple, Optional, Tuple, TypedDict

import validators

from ..errors import CliError, InvalidResource, MissingResource
from .config import Config
from .flags import FlagsConfig, get_resource_list, get_sso_profile


class Profile(NamedTuple):
    display_name: str
    region: str
    arn: str
    sso_profile: Optional[str] = None
    aws_saml_url: Optional[str] = None
    ansible_bucket: Optional[str] = None
    aliases: List[str] = []


@dataclass
class OrgParams:
    resource_env_var: Optional[str]
    users: Dict[str, str]
    domain: str
    aws_saml_url: str
    aws_okta_params: Dict[str, str]
    saml2aws_params: Dict[str, str]
    flags_config: FlagsConfig

    default_profiles: Dict[str, Profile]

    _profiles: Dict[str, Profile] = field(init=False)
    _sso_profiles: Dict[str, str] = field(init=False)
    _sso_enabled: bool = field(init=False)

    def __post_init__(self):
        self._profiles = None
        self._sso_profiles = {}
        self._sso_enabled = False

    @property
    def sso_enabled(self) -> bool:
        """Find out whether we should be using sso as an option for this org"""
        if not self._profiles:
            self._profiles = self._load_profiles()
        return self._sso_enabled

    @property
    def profiles(self) -> Dict[str, Profile]:
        """Get the list of profile options for this org"""
        if not self._profiles:
            self._profiles = self._load_profiles()
        return self._profiles

    def _load_profiles(self) -> Dict[str, Profile]:
        """
        Use LaunchDarkly to look up a listing of resources, and overlay that
        config on top of the hard-coded config if possible
        """
        if not Config.should_analytics():
            return self.default_profiles

        email = Config.get_email()
        sso_enabled, resources = get_resource_list(email, self.flags_config)
        self._sso_enabled = sso_enabled
        if not sso_enabled or not resources:
            return self.default_profiles

        result = {}
        for resource in resources:
            if profile := self.default_profiles.get(resource):
                result[resource] = profile
            else:
                result[resource] = Profile(
                    display_name=resource,
                    region="us-east-1",
                    arn="n/a",
                    aliases=[],
                )
        return result

    def sso_profile(self, resource: str) -> str:
        """
        Use LaunchDarkly to look up an AWS SSO profile name for the current
        resource, if possible.
        """
        if result := self._sso_profiles.get(resource):
            return result

        if not Config.should_analytics():
            return resource

        email = Config.get_email()
        _, profile = get_sso_profile(resource, email, self.flags_config)
        if profile:
            self._sso_profiles[resource] = profile
            return profile
        return resource

    def __getitem__(self, item):
        return getattr(self, item)


LaunchDarklyParams = OrgParams(
    resource_env_var="ENVIRONMENT",
    users={"ssh": "ubuntu", "ansible": "ansible"},
    domain="launchdarkly.com",
    aws_saml_url=(
        "https://launchdarkly.okta.com/home/amazon_aws/0oaj4aow7gPk26Fy6356/272"
    ),
    aws_okta_params={
        "mfa_provider": "OKTA",
        "mfa_factor_type": "auto",
        "assume_role_ttl": "1h",
        "session_ttl": "30m",
    },
    saml2aws_params={"mfa": "Auto", "aws_session_duration": "1800"},
    flags_config=FlagsConfig(
        client_id="647e348b49e9c114656d9506",
        api_url="app.ld.catamorphic.com",
    ),
    default_profiles={
        "production": Profile(
            display_name="Production",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-production",
            ansible_bucket="launchdarkly-sym-ansible-production",
            aliases=["prod"],
            sso_profile="launchdarkly-main-ssh",
        ),
        "staging": Profile(
            display_name="Staging",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-staging",
            ansible_bucket="launchdarkly-sym-ansible-staging",
            sso_profile="launchdarkly-main-ssh",
        ),
        "dr": Profile(
            display_name="DR",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-dr",
            ansible_bucket="launchdarkly-sym-ansible-dr",
            aliases=["production_dr"],
            sso_profile="launchdarkly-main-ssh",
        ),
        "dev": Profile(
            display_name="Dev",
            region="us-east-1",
            arn="arn:aws:iam::506919356135:role/ops/SSHAdmin-development",
            ansible_bucket="launchdarkly-sym-ansible-dev",
            aliases=["development"],
            sso_profile="launchdarkly-dev-ssh",
        ),
        "shared-services": Profile(
            display_name="Shared Services",
            region="us-east-1",
            arn="arn:aws:iam::061661829416:role/ops/SSHAdmin-shared-services",
            ansible_bucket="launchdarkly-sym-ansible-shared-services",
            aliases=["shared_services"],
            sso_profile="launchdarkly-shared-services-ssh",
        ),
        "catamorphic": Profile(
            display_name="Catamorphic",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-catamorphic",
            ansible_bucket="launchdarkly-sym-ansible-catamorphic",
            sso_profile="launchdarkly-main-ssh",
        ),
        "catamorphic-dr": Profile(
            display_name="Catamorphic DR",
            region="us-east-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-catamorphic_dr",
            ansible_bucket="launchdarkly-sym-ansible-catamorphic-dr",
            aliases=["catamorphic_dr"],
            sso_profile="launchdarkly-main-ssh",
        ),
        "intuit-production": Profile(
            display_name="Intuit: Production",
            region="us-west-2",
            arn="arn:aws:iam::527291094460:role/ops/SSHAdmin-production",
            ansible_bucket="launchdarkly-sym-ansible-intuit-production",
            aliases=[
                "production-intuit",
                "intuit_production",
                "intuit_production_use2",
            ],
            sso_profile="launchdarkly-intuit-ssh",
        ),
        "intuit-dr": Profile(
            display_name="Intuit: DR",
            region="us-east-2",
            arn="arn:aws:iam::527291094460:role/ops/SSHAdmin-dr",
            ansible_bucket="launchdarkly-sym-ansible-intuit-production-dr",
            aliases=["intuit_dr", "intuit_production_dr"],
            sso_profile="launchdarkly-intuit-ssh",
        ),
        "intuit-staging": Profile(
            display_name="Intuit: Staging",
            region="us-west-2",
            arn="arn:aws:iam::527291094460:role/ops/SSHAdmin-staging",
            ansible_bucket="launchdarkly-sym-ansible-intuit-staging",
            aliases=["staging-intuit", "intuit_staging", "intuit_staging_use2"],
            sso_profile="launchdarkly-intuit-ssh",
        ),
        "production_apac": Profile(
            display_name="Production: APAC",
            region="ap-southeast-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-production",
            ansible_bucket="launchdarkly-sym-ansible-production",
            sso_profile="launchdarkly-main-ssh-apac",
        ),
        "production_euw1": Profile(
            display_name="Production: EU West 1",
            region="eu-west-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-production",
            ansible_bucket="launchdarkly-sym-ansible-production",
            sso_profile="launchdarkly-main-ssh-euw1",
        ),
        "staging_apac": Profile(
            display_name="Staging: APAC",
            region="ap-southeast-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-staging",
            ansible_bucket="launchdarkly-sym-ansible-staging",
            sso_profile="launchdarkly-main-ssh-apac",
        ),
        "staging_euw1": Profile(
            display_name="Staging: EU West 1",
            region="eu-west-1",
            arn="arn:aws:iam::554582317989:role/ops/SSHAdmin-staging",
            ansible_bucket="launchdarkly-sym-ansible-staging",
            sso_profile="launchdarkly-main-ssh-euw1",
        ),
        "sdk": Profile(
            display_name="SDK",
            region="us-east-1",
            arn="arn:aws:iam::223148043183:role/ops/SSHAdmin-sdk",
            ansible_bucket="launchdarkly-sym-ansible-sdk",
            aliases=["sdk"],
            sso_profile="launchdarkly-sdk-ssh",
        ),
    },
)

SymParams = OrgParams(
    resource_env_var="ENVIRONMENT",
    users={"ssh": "ubuntu", "ansible": "ubuntu"},
    domain="symops.io",
    aws_saml_url=("https://dev-291131.okta.com/home/amazon_aws/0oaqlmsn7GMVgAyBK4x6/272"),
    aws_okta_params={
        "mfa_provider": "OKTA",
        "assume_role_ttl": "1h",
        "session_ttl": "30m",
    },
    saml2aws_params={"mfa": "Auto", "aws_session_duration": "1800"},
    flags_config=FlagsConfig(
        client_id="61baa6c942189d14dec41c78",
    ),
    default_profiles={
        "test": Profile(
            display_name="Test",
            region="us-east-1",
            arn="arn:aws:iam::838419636750:role/SSMTestRole",
            aliases=["this_is_an_alias"],
        ),
        "test_euw1": Profile(
            display_name="Test: EU West 1",
            region="eu-west-1",
            arn="arn:aws:iam::838419636750:role/SSMTestRole",
        ),
        "test-custom": Profile(
            display_name="TestCustom",
            region="us-east-1",
            arn="arn:aws:iam::838419636750:role/SSMTestRoleCustomBucket",
            ansible_bucket="sym-ansible-dev",
            aliases=["test_custom", "test_custom2"],
        ),
    },
)

PARAMS: Dict[str, OrgParams] = {
    "launch-darkly": LaunchDarklyParams,
    "launchdarkly": LaunchDarklyParams,
    "sym": SymParams,
}


def get_org_params() -> OrgParams:
    return PARAMS[Config.get_org()]


def is_sso_enabled() -> bool:
    return get_org_params().sso_enabled


def get_aws_saml_url(resource: str) -> str:
    org_params = get_org_params()
    profile = get_profile(resource)
    return profile.aws_saml_url or org_params["aws_saml_url"]


def get_aws_okta_params() -> Dict[str, str]:
    return get_org_params()["aws_okta_params"]


def get_saml2aws_params() -> Dict[str, str]:
    return get_org_params()["saml2aws_params"]


def get_profiles() -> Dict[str, Profile]:
    return get_org_params()["profiles"]


def get_domain() -> str:
    return get_org_params()["domain"]


def get_ssh_user() -> str:
    return get_org_params()["users"]["ssh"]


def get_ansible_user() -> str:
    return get_org_params()["users"]["ansible"]


def get_resource_env_vars() -> Optional[str]:
    try:
        return ("SYM_RESOURCE", get_org_params()["resource_env_var"])
    except KeyError:
        return "SYM_RESOURCE"


def get_profile_and_name(resource: str) -> Tuple[str, Profile]:
    if not resource:
        raise MissingResource(list(get_profiles().keys()))
    try:
        return next(
            (name, profile)
            for name, profile in get_profiles().items()
            if resource == name or resource in profile.aliases
        )
    except StopIteration:
        raise InvalidResource(resource, list(get_profiles().keys()))


def get_profile(resource: str) -> Profile:
    return get_profile_and_name(resource)[1]


def set_login_fields(org: str, email: str):
    if org not in PARAMS:
        raise CliError(f"Invalid org: {org}")

    config = Config.instance()
    config["org"] = org

    if not validators.email(email):
        raise CliError(f"Invalid email: {email}")

    if (domain := email.split("@")[-1]) != get_domain():
        raise CliError(f"Invalid domain: {domain}")

    config["email"] = email
