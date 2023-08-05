# Generated by ariadne-codegen on 2023-06-26 16:36
# Source: operations.graphql

from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class ImportCustomerBulk(BaseModel):
    import_customers_bulk: Optional[str] = Field(alias="importCustomersBulk")


ImportCustomerBulk.update_forward_refs()
