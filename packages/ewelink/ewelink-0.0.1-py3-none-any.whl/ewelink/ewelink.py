import base64
import hashlib
import hmac
import logging
from aiohttp import ClientResponse, ClientSession, JsonPayload
from typing import Any, Literal, Optional

from .types import Device

BASE_URL = "https://eu-apia.coolkit.cc"
APP_ID = "YzfeftUVcZ6twZw1OoVKPRFYTrGEg01Q"
APP_SECRET = "4G91qSoboqYO4Y0XJ0LPPKIsq8reHdfa"


class EWeLinkError(Exception):
    def __init__(self, response: ClientResponse, msg: str) -> None:
        super().__init__(
            f"eWeLink API request ({response.method}) to '{response.url}' failed. Error: {msg}."
        )

    ...


class EWeLinkPayload(JsonPayload):
    ...

    def __init__(
        self,
        value: Any,
        app_id: str,
        app_secret: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(value, *args, **kwargs)

        # Calculate and set Authentication Sign
        signature = base64.b64encode(
            hmac.new(
                bytes(app_secret, "utf-8"),
                self._value,
                digestmod=hashlib.sha256,
            ).digest()
        ).decode("utf-8")

        self._headers["X-CK-Appid"] = app_id
        self._headers["Authorization"] = f"Sign {signature}"


class EWeLink:
    def __init__(self, email: str, password: str) -> None:
        self._email = email
        self._password = password
        self._session = ClientSession()

        self._at = None

    async def __aenter__(self) -> "EWeLink":
        return self

    async def __aexit__(self) -> None:
        await self.close()

    async def close(self) -> None:
        await self.logout()
        await self._session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        async with self._session.request(
            method,
            f"{BASE_URL}/{endpoint}",
            *args,
            **kwargs,
        ) as response:
            response.raise_for_status()
            data = await response.json()

            if data["error"]:
                raise EWeLinkError(response, data["msg"])

        return data["data"]

    async def _auth_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[dict[str, str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if self._at is None:
            await self.login()

        return await self._request(
            method,
            endpoint,
            headers={
                **(headers if headers else {}),
                "Authorization": f"Bearer {self._at}",
            },
            *args,
            **kwargs,
        )

    async def login(self) -> None:
        response = await self._request(
            "POST",
            "v2/user/login",
            data=EWeLinkPayload(
                {
                    "email": self._email,
                    "password": self._password,
                    "countryCode": "+1",  # Required but irrelevant
                },
                APP_ID,
                APP_SECRET,
            ),
        )
        self._at = response["at"]

    async def logout(self) -> None:
        await self._auth_request("DELETE", "v2/user/logout", headers={"X-CK-Appid": APP_ID})

    async def get_thing_list(self) -> list[Device]:
        response = await self._auth_request("GET", "v2/device/thing")
        things = response["thingList"]

        items = []
        for thing in things:
            type = thing["itemType"]
            data = thing["itemData"]

            if type == 1:
                items.append(Device.parse_obj(data))
            else:
                raise NotImplementedError()

        return items

    async def update_thing_status(
        self,
        device: Device,
        params: dict[str, Any],
        new_params: bool = False,
    ) -> None:
        if new_params is False:
            new_keys = params.keys() - device.params.keys()
            if new_keys:
                logging.warning(
                    f"Ignoring new params ({new_keys}) not previously set."
                    " Setting new params may cause undefined behaviors. If this was"
                    " intentionally, set new_params=True when calling"
                    " update_thing_status(...)."
                )

            params = {k: v for k, v in params.items() if k in device.params}

        await self._auth_request(
            "POST",
            "v2/device/thing/status",
            json={
                "type": 1,
                "id": device.id,
                "params": params,
            },
        )

    async def set_device_power_status(
        self,
        device: Device,
        status: Literal["on", "off"],
    ) -> None:
        if device.extra.type.channels == 1:
            params = {"switch": status}
        else:
            raise NotImplementedError()

        await self.update_thing_status(device, params)
