# -*- coding: utf-8 -*-
# Copyright 2021 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING, Mapping

from twisted.web.resource import Resource

from synapse.rest.synapse.client.pick_idp import PickIdpResource
from synapse.rest.synapse.client.pick_username import pick_username_resource
from synapse.rest.synapse.client.sso_register import SsoRegisterResource

if TYPE_CHECKING:
    from synapse.server import HomeServer


def build_synapse_client_resource_tree(hs: "HomeServer") -> Mapping[str, Resource]:
    """Builds a resource tree to include synapse-specific client resources

    These are resources which should be loaded on all workers which expose a C-S API:
    ie, the main process, and any generic workers so configured.

    Returns:
         map from path to Resource.
    """
    resources = {
        # SSO bits. These are always loaded, whether or not SSO login is actually
        # enabled (they just won't work very well if it's not)
        "/_synapse/client/pick_idp": PickIdpResource(hs),
        "/_synapse/client/pick_username": pick_username_resource(hs),
        "/_synapse/client/sso_register": SsoRegisterResource(hs),
    }

    # provider-specific SSO bits. Only load these if they are enabled, since they
    # rely on optional dependencies.
    if hs.config.oidc_enabled:
        from synapse.rest.oidc import OIDCResource

        resources["/_synapse/oidc"] = OIDCResource(hs)

    if hs.config.saml2_enabled:
        from synapse.rest.saml2 import SAML2Resource

        resources["/_matrix/saml2"] = SAML2Resource(hs)

    return resources


__all__ = ["build_synapse_client_resource_tree"]
