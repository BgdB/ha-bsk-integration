import aiohttp
import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, STATUS_URL


class BSKFanIntegrationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    DOMAIN = DOMAIN

    async def _validate_jwt(self, token):
        """Synchronous JWT validation function."""

        headers = {"Authorization": f"{token}",
                   "Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.get(STATUS_URL, headers=headers) as resp:
                return resp.status_code == 200

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}
        if user_input is not None:
            token = user_input["jwt_token"]
            if self._validate_jwt(token):
                await self.async_set_unique_id(token)
                return self.async_create_entry(title="BSK Fan Integration", data=user_input)
            else:
                errors["base"] = "invalid_token"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("jwt_token"): str
            }),
            errors=errors,
        )
