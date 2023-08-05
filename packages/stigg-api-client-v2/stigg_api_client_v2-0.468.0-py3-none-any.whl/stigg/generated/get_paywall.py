# Generated by ariadne-codegen on 2023-06-26 16:36
# Source: operations.graphql

from .base_model import BaseModel
from .fragments import PaywallFragment


class GetPaywall(BaseModel):
    paywall: "GetPaywallPaywall"


class GetPaywallPaywall(PaywallFragment):
    pass


GetPaywall.update_forward_refs()
GetPaywallPaywall.update_forward_refs()
