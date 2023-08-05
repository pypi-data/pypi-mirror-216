# Generated by ariadne-codegen on 2023-06-26 16:36
# Source: operations.graphql

from pydantic import Field

from .base_model import BaseModel
from .fragments import CustomerPortalFragment


class GetCustomerPortalByRefId(BaseModel):
    customer_portal: "GetCustomerPortalByRefIdCustomerPortal" = Field(
        alias="customerPortal"
    )


class GetCustomerPortalByRefIdCustomerPortal(CustomerPortalFragment):
    pass


GetCustomerPortalByRefId.update_forward_refs()
GetCustomerPortalByRefIdCustomerPortal.update_forward_refs()
