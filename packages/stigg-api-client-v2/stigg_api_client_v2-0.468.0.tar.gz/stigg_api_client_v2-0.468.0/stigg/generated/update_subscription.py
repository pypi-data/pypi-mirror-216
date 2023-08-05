# Generated by ariadne-codegen on 2023-06-26 16:36
# Source: operations.graphql

from pydantic import Field

from .base_model import BaseModel
from .fragments import SlimSubscriptionFragment


class UpdateSubscription(BaseModel):
    update_subscription: "UpdateSubscriptionUpdateSubscription" = Field(
        alias="updateSubscription"
    )


class UpdateSubscriptionUpdateSubscription(SlimSubscriptionFragment):
    pass


UpdateSubscription.update_forward_refs()
UpdateSubscriptionUpdateSubscription.update_forward_refs()
