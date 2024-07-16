import logging

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class MyIntegrationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        # Load data from configuration.yaml
        yaml_config = self.hass.data.get(DOMAIN, {})
        _LOGGER.debug("YAML Config: %s", yaml_config)

        if user_input is not None:
            return self.async_create_entry(title="BSK Integration", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("jwt_token"): str
            })
        )
