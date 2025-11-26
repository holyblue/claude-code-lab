"""
Pydantic schemas for AccountGroup.

These schemas define the data validation and serialization for account groups
in API requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class AccountGroupBase(BaseModel):
    """Base schema with common AccountGroup attributes."""

    code: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="模組代碼（如：A00）",
        examples=["A00", "O18"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="模組名稱（如：中概全權）",
        examples=["中概全權", "數據智能應用科"],
    )
    is_default: bool = Field(
        default=False,
        description="是否為常用模組",
    )


class AccountGroupCreate(AccountGroupBase):
    """Schema for creating a new account group."""

    pass


class AccountGroupUpdate(BaseModel):
    """Schema for updating an existing account group."""

    code: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="模組代碼",
    )
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="模組名稱",
    )
    is_default: Optional[bool] = Field(
        None,
        description="是否為常用模組",
    )


class AccountGroupResponse(AccountGroupBase):
    """Schema for account group responses."""

    id: int = Field(..., description="模組 ID")
    full_name: str = Field(..., description="完整名稱（代碼 + 名稱）")
    created_at: datetime = Field(..., description="創建時間")
    updated_at: datetime = Field(..., description="更新時間")

    model_config = ConfigDict(from_attributes=True)


class AccountGroupList(BaseModel):
    """Schema for list of account groups."""

    items: list[AccountGroupResponse]
    total: int = Field(..., description="總數量")
