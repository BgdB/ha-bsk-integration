"""Constants for the bsk-fan-integration integration."""

DOMAIN = "bskintegration"

API_BASE_URL = "https://api.bskhvac.com.tr/device-user/zephyr/"
UPDATE_URL = f"{API_BASE_URL}update-group-settings"
STATUS_URL = f"{API_BASE_URL}master-device-list"
RENEW_TOKEN_URL = "https://api.bskhvac.com.tr/auth/google/callback"
DEVICE_ID = "48E72911E06C"  # Example device ID, can be dynamic
GROUP_ID = "48E72911E06C"  # Example group ID, can be dynamic
