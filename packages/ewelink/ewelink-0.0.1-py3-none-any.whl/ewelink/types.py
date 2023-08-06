from pydantic import BaseModel, Field
from typing import Any


class DeviceType:
    def __init__(self, name: str, channels: int) -> None:
        self.name = name
        self.channels = channels


DEVICE_TYPES = {
    1: DeviceType("SOCKET", 1),
    2: DeviceType("SOCKET_2", 2),
}


class DeviceInfo(BaseModel):
    # model: str
    # ui: str
    uiid: int
    # description: str
    # manufacturer: str
    # mac: str
    # apmac: str
    # model_info: str = Field(alias="modelInfo")
    # brand_id: str = Field(alias="brandId")
    # chip_id: str = Field(alias="chipid")

    @property
    def type(self) -> DeviceType:
        return DEVICE_TYPES[self.uiid]


class Device(BaseModel):
    name: str
    id: str = Field(alias="deviceid")
    apikey: str
    extra: DeviceInfo
    # brand_name: str = Field(alias="brandName")
    # brand_logo: str = Field(alias="brandLogo")
    # show_brand: bool = Field(alias="showBrand")
    # product_model: str = Field(alias="productModel")
    params: dict[str, Any]
