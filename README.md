# ha-solax

Home Assistant custom integration for SolaX inverters via local HTTP API.

## Installation

### HACS (recommended)

1. Add this repository as a custom repository in HACS
2. Install "SolaX Local"
3. Restart Home Assistant
4. Add the integration via Settings > Devices & Services > Add Integration > SolaX Local

### Manual

Copy `custom_components/solax_local` to your Home Assistant `custom_components` directory.

## Configuration

- **Host**: IP address of your SolaX PocketWiFi dongle (e.g., 192.168.1.106)
- **Password**: Dongle serial number (printed on the dongle label)
- **Port**: HTTP port (default: 80)
- **Username**: Optional, required for newer firmware with Basic Auth

## Sensors

21 sensors covering grid, PV1, PV2, battery, inverter, power flow, and energy totals.
