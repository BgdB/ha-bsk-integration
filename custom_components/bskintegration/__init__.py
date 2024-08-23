from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the integration from a config entry."""
    try:
        # Your setup logic here, for example:
        # Initialize the API client, validate credentials, etc.
        token = entry.data.get("jwt_token")
        # (Optional) Perform a quick validation of the token by calling the API

        if not token or not await validate_token(hass, token):
            raise ConfigEntryNotReady("Invalid JWT token")

        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = token

        # Example: setting up a platform, if your integration has one
        await hass.config_entries.async_forward_entry_setup(entry, "fan")
        await hass.config_entries.async_forward_entry_setup(entry, "sensor")
        return True
    except Exception as e:
        # If any error occurs, we log it and return False to signal failure
        print(f"Error setting up {DOMAIN}: {str(e)}")
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "fan")
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def validate_token(hass, token):
    """Example validation function for the JWT token."""
    # Implement your token validation logic here (e.g., an API call)
    return True  # For this example, assume it's always valid
