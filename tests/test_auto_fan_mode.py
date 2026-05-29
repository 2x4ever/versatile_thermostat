# pylint: disable=wildcard-import, unused-wildcard-import, protected-access, unused-argument, line-too-long

""" Test the auto fan mode of a over_climate thermostat """
from unittest.mock import patch, call

from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant

# from homeassistant.components.climate import HVACAction
from homeassistant.config_entries import ConfigEntryState

from homeassistant.components.climate import ClimateEntityFeature, PRESET_COMFORT, PRESET_ECO, PRESET_BOOST

from pytest_homeassistant_custom_component.common import MockConfigEntry

# from custom_components.versatile_thermostat.base_thermostat import BaseThermostat
from custom_components.versatile_thermostat.thermostat_climate import (
    ThermostatOverClimate,
)
from .commons import *  # pylint: disable=wildcard-import, unused-wildcard-import


async def test_over_climate_auto_fan_mode_with_3_fan_speed_values(
    hass: HomeAssistant, skip_hass_states_is_state, skip_send_event
):
    """Test the init of an over climate thermostat with 3 fan speed values"""

    fan_modes = ["1", "2", "3", "auto"]

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: ["climate.mock_climate"],
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
        },
    )

    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mock_climate",
        name="MockClimateName",
        fan_modes=fan_modes,
    )

    # 1. Init with CONF_AUTO_FAN_TURBO
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    assert entry.state is ConfigEntryState.LOADED

    entity: ThermostatOverClimate = search_entity(hass, "climate.theoverclimatemockname", "climate")

    assert entity
    assert isinstance(entity, ThermostatOverClimate)

    assert entity.name == "TheOverClimateMockName"
    assert entity.is_over_climate is True
    assert entity.fan_modes == fan_modes
    assert entity._auto_fan_mode == "auto_fan_turbo"
    assert entity._auto_activated_fan_mode == "3"
    assert entity._auto_deactivated_fan_mode == "1"

    # 2. Change auto_fan_mode by CONF_AUTO_FAN_HIGH
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("High")
        assert entity._auto_activated_fan_mode == "3"
        assert entity._auto_deactivated_fan_mode == "1"

    # 3. Change auto_fan_mode by CONF_AUTO_FAN_MEDIUM
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Medium")
        assert entity._auto_activated_fan_mode == "2"
        assert entity._auto_deactivated_fan_mode == "1"

    # 4. Change auto_fan_mode by CONF_AUTO_FAN_LOW
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Low")
        assert entity._auto_activated_fan_mode == "1"
        assert entity._auto_deactivated_fan_mode == "1"

    entity.remove_thermostat()

async def test_over_climate_auto_fan_mode_with_4_fan_speed_values(
    hass: HomeAssistant, skip_hass_states_is_state, skip_send_event
):
    """Test the init of an over climate thermostat with 4 fan speed values"""

    fan_modes = ["low", "medium", "high", "boost", "auto"]

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: ["climate.mock_climate"],
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
        },
    )

    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mock_climate",
        name="MockClimateName",
        fan_modes=fan_modes,
    )

    # 1. Init with CONF_AUTO_FAN_TURBO
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    assert entry.state is ConfigEntryState.LOADED

    entity: ThermostatOverClimate = search_entity(hass, "climate.theoverclimatemockname", "climate")

    assert entity
    assert isinstance(entity, ThermostatOverClimate)

    assert entity.name == "TheOverClimateMockName"
    assert entity.is_over_climate is True
    assert entity.fan_modes == fan_modes
    assert entity._auto_fan_mode == "auto_fan_turbo"
    assert entity._auto_activated_fan_mode == "boost"
    assert entity._auto_deactivated_fan_mode == "low"

    # 2. Change auto_fan_mode by CONF_AUTO_FAN_HIGH
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("High")
        assert entity._auto_activated_fan_mode == "high"
        assert entity._auto_deactivated_fan_mode == "low"

    # 3. Change auto_fan_mode by CONF_AUTO_FAN_MEDIUM
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Medium")
        assert entity._auto_activated_fan_mode == "medium"
        assert entity._auto_deactivated_fan_mode == "low"

    # 4. Change auto_fan_mode by CONF_AUTO_FAN_LOW
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Low")
        assert entity._auto_activated_fan_mode == "low"
        assert entity._auto_deactivated_fan_mode == "low"

    entity.remove_thermostat()

async def test_over_climate_auto_fan_mode_with_5_fan_speed_values(
    hass: HomeAssistant, skip_hass_states_is_state, skip_send_event
):
    """Test the init of an over climate thermostat with 5 fan speed values"""

    fan_modes = ["quiet", "1", "2", "3", "4", "auto"]

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: ["climate.mock_climate"],
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
        },
    )

    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mock_climate",
        name="MockClimateName",
        fan_modes=fan_modes,
    )

    # 1. Init with CONF_AUTO_FAN_TURBO
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    assert entry.state is ConfigEntryState.LOADED

    entity: ThermostatOverClimate = search_entity(hass, "climate.theoverclimatemockname", "climate")

    assert entity
    assert isinstance(entity, ThermostatOverClimate)

    assert entity.name == "TheOverClimateMockName"
    assert entity.is_over_climate is True
    assert entity.fan_modes == fan_modes
    assert entity._auto_fan_mode == "auto_fan_turbo"
    assert entity._auto_activated_fan_mode == "4"
    assert entity._auto_deactivated_fan_mode == "quiet"

    # 2. Change auto_fan_mode by CONF_AUTO_FAN_HIGH
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("High")
        assert entity._auto_activated_fan_mode == "3"
        assert entity._auto_deactivated_fan_mode == "quiet"

    # 3. Change auto_fan_mode by CONF_AUTO_FAN_MEDIUM
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Medium")
        assert entity._auto_activated_fan_mode == "2"
        assert entity._auto_deactivated_fan_mode == "quiet"

    # 4. Change auto_fan_mode by CONF_AUTO_FAN_LOW
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Low")
        assert entity._auto_activated_fan_mode == "1"
        assert entity._auto_deactivated_fan_mode == "quiet"

    entity.remove_thermostat()

async def test_over_climate_auto_fan_mode_turbo_activation(
    hass: HomeAssistant, skip_hass_states_is_state, skip_send_event
):
    """Test the init of an over climate thermostat with auto_fan_mode = Turbo which exists"""

    fan_modes = ["low", "medium", "high", "boost", "mute", "auto", "turbo"]

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            "eco_ac_temp": 25,
            "comfort_ac_temp": 23,
            "boost_ac_temp": 21,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: ["climate.mock_climate"],
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
            CONF_AC_MODE: True,
        },
    )

    tz = get_tz(hass)  # pylint: disable=invalid-name
    now: datetime = datetime.now(tz=tz)

    # 1. Init fan mode
    entity = await create_thermostat(hass, entry, "climate.theoverclimatemockname")

    # Creates the under entity after the thermostat creation. It should works too.
    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mock_climate",
        name="MockClimateName",
        fan_modes=fan_modes,
    )
    # The state is written so we wait to wait for propagation
    await hass.async_block_till_done()

    assert entity
    assert isinstance(entity, ThermostatOverClimate)

    assert entity.name == "TheOverClimateMockName"
    assert entity.is_over_climate is True
    assert entity.fan_modes == fan_modes
    assert entity.fan_mode is None
    assert entity._auto_fan_mode == "auto_fan_turbo"
    assert entity._auto_activated_fan_mode == "turbo"
    assert entity._auto_deactivated_fan_mode == "mute"

    # 2. Turn on and set temperature cold
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        # Force preset mode
        await entity.async_set_hvac_mode(VThermHvacMode_HEAT)
        assert entity.hvac_mode == VThermHvacMode_HEAT
        await entity.async_set_preset_mode(VThermPreset.COMFORT)
        assert entity.preset_mode == VThermPreset.COMFORT
        assert entity.target_temperature == 18

        # Change the current temperature to 16 which is 2° under
        await send_temperature_change_event(entity, 16, now, True)

        assert mock_send_fan_mode.call_count == 1  # send_temperature_change_event change also the fan mode
        mock_send_fan_mode.assert_has_calls([call.set_fan_mode("turbo")])

        fake_underlying_climate.set_fan_mode("turbo")
        await hass.async_block_till_done()
        assert entity.fan_mode == "turbo"

    # 3. Set another low temperature
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        fake_underlying_climate.set_fan_mode("turbo")

        # Change the current temperature to 15 which is 3° under
        await send_temperature_change_event(entity, 15, now, True)

        # Nothing is send cause we are already in turbo fan mode
        assert mock_send_fan_mode.call_count == 0

        assert entity.fan_mode == "turbo"

    # 4. Set temperature not so cold
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        # Change the current temperature to 17 which is 1° under
        await send_temperature_change_event(entity, 17, now, True)

        assert mock_send_fan_mode.call_count == 1
        mock_send_fan_mode.assert_has_calls([call.set_fan_mode("mute")])

        fake_underlying_climate.set_fan_mode("mute")
        await hass.async_block_till_done()
        assert entity.fan_mode == "mute"

    # 5. Set temperature not so cold another time
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        fake_underlying_climate.set_fan_mode("mute")

        # Change the current temperature to 17 which is 1° under
        await send_temperature_change_event(entity, 17.1, now, True)

        assert mock_send_fan_mode.call_count == 0
        assert entity.fan_mode == "mute"

    # 6. Set temperature very high above the target
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        fake_underlying_climate.set_fan_mode("mute")

        # Change the current temperature to 17 which is 1° under
        await send_temperature_change_event(entity, 21, now, True)

        assert mock_send_fan_mode.call_count == 0
        assert entity.fan_mode == "mute"

    # 7. In AC mode, set temperature very high under the target
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.async_set_hvac_mode(VThermHvacMode_COOL)
        assert entity.hvac_mode == VThermHvacMode_COOL
        assert entity.preset_mode == VThermPreset.COMFORT
        assert entity.target_temperature == 23

        assert entity.current_temperature == 21

        fake_underlying_climate.set_fan_mode("mute")

        # Change the current temperature to 17 which is 1° under
        await send_temperature_change_event(entity, 20, now, True)

        assert mock_send_fan_mode.call_count == 0
        assert entity.fan_mode == "mute"

    # 8. In AC mode, set temperature not so high above the target
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        assert entity.target_temperature == 23
        await send_temperature_change_event(entity, 24, now, True)
        assert entity.current_temperature == 24
        fake_underlying_climate.set_fan_mode("mute")

        assert mock_send_fan_mode.call_count == 0
        assert entity.fan_mode == "mute"

    # 9. In AC mode, set temperature high above the target
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        assert entity.target_temperature == 23
        await send_temperature_change_event(entity, 25.1, now, True)
        assert entity.current_temperature == 25.1

        assert mock_send_fan_mode.call_count == 1
        mock_send_fan_mode.assert_has_calls([call.set_fan_mode("turbo")])

        fake_underlying_climate.set_fan_mode("turbo")
        await hass.async_block_till_done()
        assert entity.fan_mode == "turbo"

    entity.remove_thermostat()

async def test_over_climate_auto_fan_mode_with_descending_speed_list(hass: HomeAssistant, skip_hass_states_is_state, skip_send_event):
    """Test the init of an over climate thermostat with 4 fan speed values"""

    fan_modes = ["high", "medium", "low", "diffuse", "auto"]

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: ["climate.mock_climate"],
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
        },
    )

    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mock_climate",
        name="MockClimateName",
        fan_modes=fan_modes,
    )

    # 1. Init with CONF_AUTO_FAN_TURBO
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    assert entry.state is ConfigEntryState.LOADED

    entity: ThermostatOverClimate = search_entity(hass, "climate.theoverclimatemockname", "climate")

    assert entity
    assert isinstance(entity, ThermostatOverClimate)

    assert entity.name == "TheOverClimateMockName"
    assert entity.is_over_climate is True
    assert entity.fan_modes == fan_modes
    assert entity._auto_fan_mode == "auto_fan_turbo"
    assert entity._auto_activated_fan_mode == "high"
    assert entity._auto_deactivated_fan_mode == "low"

    # 2. Change auto_fan_mode by CONF_AUTO_FAN_HIGH
    with patch("custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode") as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("High")
        assert entity._auto_activated_fan_mode == "medium"
        assert entity._auto_deactivated_fan_mode == "low"

    # 3. Change auto_fan_mode by CONF_AUTO_FAN_MEDIUM
    with patch("custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode") as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Medium")
        assert entity._auto_activated_fan_mode == "low"
        assert entity._auto_deactivated_fan_mode == "low"

    # 4. Change auto_fan_mode by CONF_AUTO_FAN_LOW
    with patch("custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode") as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Low")
        assert entity._auto_activated_fan_mode == "diffuse"
        assert entity._auto_deactivated_fan_mode == "low"

    entity.remove_thermostat()

async def test_over_climate_auto_fan_mode_with_none_fan_speed_values(
    hass: HomeAssistant, skip_hass_states_is_state, skip_send_event
):
    """Test the init of an over climate thermostat with none fan speed values"""

    fan_modes = ["on", "auto", "diffuse"]

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: ["climate.mock_climate"],
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
        },
    )

    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mock_climate",
        name="MockClimateName",
        fan_modes=fan_modes,
    )

    # 1. Init with CONF_AUTO_FAN_TURBO
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    assert entry.state is ConfigEntryState.LOADED

    entity: ThermostatOverClimate = search_entity(hass, "climate.theoverclimatemockname", "climate")

    assert entity
    assert isinstance(entity, ThermostatOverClimate)

    assert entity.name == "TheOverClimateMockName"
    assert entity.is_over_climate is True
    assert entity.fan_modes == fan_modes
    assert entity._auto_fan_mode == "auto_fan_turbo"
    assert entity._auto_activated_fan_mode is None
    assert entity._auto_deactivated_fan_mode is None

    # 2. Change auto_fan_mode by CONF_AUTO_FAN_HIGH
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("High")
        assert entity._auto_activated_fan_mode is None
        assert entity._auto_deactivated_fan_mode is None

    # 3. Change auto_fan_mode by CONF_AUTO_FAN_MEDIUM
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Medium")
        assert entity._auto_activated_fan_mode is None
        assert entity._auto_deactivated_fan_mode is None

    # 4. Change auto_fan_mode by CONF_AUTO_FAN_LOW
    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        await entity.service_set_auto_fan_mode("Low")
        assert entity._auto_activated_fan_mode is None
        assert entity._auto_deactivated_fan_mode is None

    entity.remove_thermostat()

async def test_over_climate_auto_fan_mode_check_delay_command(hass: HomeAssistant, skip_hass_states_is_state, skip_send_event):
    """Test the delay of the fan_mode command when the setpoint temperature triggers auto_fan_mode"""

    fan_modes = ["low", "medium", "high", "boost", "mute", "auto", "turbo"]
    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mockUniqueId",
        name="MockClimateName",
        fan_modes=fan_modes,
    )

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            "eco_ac_temp": 25,
            "comfort_ac_temp": 23,
            "boost_ac_temp": 21,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: [fake_underlying_climate.entity_id],
            CONF_MINIMAL_ACTIVATION_DELAY: 30,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
            CONF_AC_MODE: True,
        },
    )

    tz = get_tz(hass)  # pylint: disable=invalid-name
    now: datetime = datetime.now(tz=tz)

    entity = await create_thermostat(hass, entry, "climate.theoverclimatemockname")

    assert entity
    assert isinstance(entity, ThermostatOverClimate)

    assert entity.name == "TheOverClimateMockName"
    assert entity.is_over_climate is True
    assert entity.fan_modes == fan_modes
    assert entity.fan_mode is None

    assert entity._auto_fan_mode == "auto_fan_turbo"
    assert entity._auto_activated_fan_mode == "turbo"
    assert entity._auto_deactivated_fan_mode == "mute"

    # Force heating mode and preset
    await entity.async_set_hvac_mode(VThermHvacMode_HEAT)
    await entity.async_set_preset_mode(VThermPreset.COMFORT)

    assert entity.hvac_mode == VThermHvacMode_HEAT
    assert entity.preset_mode == VThermPreset.COMFORT
    assert entity.target_temperature == 18

    planned_commands = []

    def fake_async_call_later(hass, delay, callback):
        value = None
        if hasattr(callback, "__closure__") and callback.__closure__:
            free_vars = callback.__code__.co_freevars
            if "fan_mode" in free_vars:
                index = free_vars.index("fan_mode")
                value = callback.__closure__[index].cell_contents

        planned_commands.append({"delay": delay, "fan_mode": value})
        return lambda: None

    # room temp is 18°C
    await send_temperature_change_event(entity, 18, now)

    with patch("custom_components.versatile_thermostat.underlyings.async_call_later", side_effect=fake_async_call_later) as mock_send:
        # --------------------------------------------------
        # 1. Temperature target at 20°C (+2 °C) → auto fan_mode (DELAYED)
        # --------------------------------------------------
        underlying = entity._underlyings[0]
        underlying._last_command_sent_datetime = now + timedelta(seconds=-10)

        await entity.async_set_temperature(temperature=20)

        assert len(planned_commands) == 1
        assert planned_commands[0]["delay"] == 2.0
        assert planned_commands[0]["fan_mode"] == "turbo"

        # --------------------------------------------------
        # 2. Manual fan_mode change withou previous command → NO DELAY
        # --------------------------------------------------
        underlying._last_command_sent_datetime = now + timedelta(seconds=-10)

        await entity.async_set_fan_mode("high")
        await hass.async_block_till_done()
        assert len(planned_commands) == 1
        assert entity._fan_mode == "high"

        # Simulate that the fan mode is now "turbo" (due to auto_fan activation)
        entity._last_change_time_from_vtherm = None
        entity._last_auto_fan_mode_sent = "turbo"
        fake_underlying_climate.set_fan_mode("turbo")
        await hass.async_block_till_done()

        # --------------------------------------------------
        # 3. Temperature target at 18°C (like room temp) → auto deactivation (DELAYED)
        # --------------------------------------------------
        underlying._last_command_sent_datetime = now + timedelta(seconds=-10)

        await entity.async_set_temperature(temperature=18)

        assert len(planned_commands) == 2
        assert planned_commands[1]["delay"] == 2.0
        assert planned_commands[1]["fan_mode"] == "mute"

    entity.remove_thermostat()


async def test_over_climate_auto_fan_mode_default_speed(
    hass: HomeAssistant, skip_hass_states_is_state, skip_send_event
):
    """Test that the auto fan mode returns to the configured CONF_AUTO_FAN_DEFAULT_SPEED when auto fan deactivates."""
    fan_modes = ["low", "medium", "high", "boost", "mute", "auto", "turbo"]

    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mock_climate",
        name="MockClimateName",
        fan_modes=fan_modes,
    )

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: [fake_underlying_climate.entity_id],
            CONF_MINIMAL_ACTIVATION_DELAY: 0,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
            CONF_AUTO_FAN_DEFAULT_SPEED: "medium",
        },
    )

    tz = get_tz(hass)
    now: datetime = datetime.now(tz=tz)

    entity = await create_thermostat(hass, entry, "climate.theoverclimatemockname")
    assert entity
    assert entity._auto_fan_default_speed == "medium"

    under = entity._underlyings[0]

    # Force heating mode and preset
    await entity.async_set_hvac_mode(VThermHvacMode_HEAT)
    await entity.async_set_preset_mode(VThermPreset.COMFORT)
    assert entity.target_temperature == 18

    # 1. Set room temp to target (no delta) -> auto fan off -> must evaluate to default speed "medium"
    under._last_command_sent_datetime = now - timedelta(seconds=10)
    await send_temperature_change_event(entity, 18, now, True)
    await hass.async_block_till_done()
    assert entity.fan_mode == "medium"

    # 2. Trigger auto fan activation (+2 delta temp)
    under._last_command_sent_datetime = now - timedelta(seconds=10)
    await entity.async_set_temperature(temperature=20)
    under._last_command_sent_datetime = now - timedelta(seconds=10)
    await send_temperature_change_event(entity, 18, now, True)
    await hass.async_block_till_done()

    # Verify auto fan changed to "turbo"
    assert entity.fan_mode == "turbo"

    # 3. Trigger auto fan deactivation (restore delta to 0)
    under._last_command_sent_datetime = now - timedelta(seconds=10)
    await entity.async_set_temperature(temperature=18)
    under._last_command_sent_datetime = now - timedelta(seconds=10)
    await send_temperature_change_event(entity, 18, now, True)
    await hass.async_block_till_done()

    # Verify that the fan mode restored to "medium"
    assert entity.fan_mode == "medium"

    # Verify custom attributes has "auto_fan_default_speed"
    entity.update_custom_attributes()
    attrs = entity._attr_extra_state_attributes["vtherm_over_climate"]
    assert attrs["auto_fan_default_speed"] == "medium"

    entity.remove_thermostat()



async def test_over_climate_auto_fan_mode_cascade_ramping(
    hass: HomeAssistant, skip_hass_states_is_state, skip_send_event
):
    """Test the cascade auto fan ramping using secondary error accumulation under PI saturation."""
    fan_modes = ["low", "medium", "high", "turbo", "auto"]

    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mock_climate",
        name="MockClimateName",
        fan_modes=fan_modes,
    )

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: [fake_underlying_climate.entity_id],
            CONF_MINIMAL_ACTIVATION_DELAY: 0,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
            CONF_AUTO_REGULATION_MODE: CONF_AUTO_REGULATION_MEDIUM,
            CONF_AUTO_FAN_CASCADE_REGULATED: True,
            CONF_AUTO_REGULATION_DTEMP: 0.1,
            CONF_AUTO_REGULATION_PERIOD_MIN: 0,
        },
    )

    tz = get_tz(hass)
    now: datetime = datetime.now(tz=tz)

    entity = await create_thermostat(hass, entry, "climate.theoverclimatemockname")
    assert entity
    assert isinstance(entity, ThermostatOverClimate)
    assert entity.is_regulated is True
    assert entity._auto_fan_cascade_regulated is True

    under = entity._underlyings[0]

    # Force heating mode and preset
    await entity.async_set_hvac_mode(VThermHvacMode_HEAT)
    await entity.async_set_preset_mode(VThermPreset.COMFORT)
    assert entity.target_temperature == 18

    # Set initial temperatures (no saturation)
    entity._set_now(now)
    under._last_command_sent_datetime = now - timedelta(seconds=10)
    await send_temperature_change_event(entity, 18, now, True)
    await send_ext_temperature_change_event(entity, 18, now, True)
    await hass.async_block_till_done()

    # Verify regulator is not saturated initially
    assert getattr(entity._regulation_algo, "is_saturated", False) is False
    assert entity._fan_accumulated_error == 0.0

    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        # 1. Set target temp to 22. At this time, room temp is 18 (not saturated).
        await entity.async_set_temperature(temperature=22)
        await hass.async_block_till_done()

        # 2. Advance time by 1 minute, and change room temp to 10. This triggers saturation.
        now = now + timedelta(minutes=1)
        entity._set_now(now)
        await send_temperature_change_event(entity, 10, now, True)
        await hass.async_block_till_done()

        # The regulation algorithm offset_max is 2.0. Target 22, current 10.
        # Total offset = 0.3 * (22-10) + 0.05 * (22-10) = 3.6 + 0.6 = 4.2, which is >= 2.0.
        # Therefore, the regulator is saturated!
        assert getattr(entity._regulation_algo, "is_saturated", False) is True

        # Check first step of accumulation (dt is 1.0, fan_error is abs(24.0 - 10) = 14.0)
        # _fan_accumulated_error should grow to 14.0, mapping to "medium"
        assert entity._fan_accumulated_error == 14.0
        assert mock_send_fan_mode.call_count == 1
        mock_send_fan_mode.assert_has_calls([call("medium")])
        mock_send_fan_mode.reset_mock()

        # Update mock climate's state
        fake_underlying_climate.set_fan_mode("medium")
        await hass.async_block_till_done()
        assert entity.fan_mode == "medium"

        # 3. Advance time by another 1 minute, keeping the regulator saturated.
        # Accumulated error should grow to 14.0 + 14.0 * 1.0 = 28.0, mapping to "turbo".
        now = now + timedelta(minutes=1)
        entity._set_now(now)
        await send_temperature_change_event(entity, 10, now, True)
        await hass.async_block_till_done()

        assert entity._fan_accumulated_error == 28.0
        assert mock_send_fan_mode.call_count == 1
        mock_send_fan_mode.assert_has_calls([call("turbo")])
        mock_send_fan_mode.reset_mock()

        fake_underlying_climate.set_fan_mode("turbo")
        await hass.async_block_till_done()
        assert entity.fan_mode == "turbo"

        # 4. Advance time by 1 minute again.
        # Accumulated error should cap at AUTO_FAN_ERROR_THRESHOLD = 30.0.
        now = now + timedelta(minutes=1)
        entity._set_now(now)
        await send_temperature_change_event(entity, 10, now, True)
        await hass.async_block_till_done()

        assert entity._fan_accumulated_error == 30.0
        # Already in turbo, so set_fan_mode should not be called again
        assert mock_send_fan_mode.call_count == 0

        # 5. Bring the room temperature close to the target temperature (22.5°C vs 22°C target)
        # The regulator should no longer be saturated.
        # Accumulated error should decay from 30.0 by AUTO_FAN_DECAY_RATE (4.0) * dt (1.0) = 4.0 -> 26.0.
        now = now + timedelta(minutes=1)
        entity._set_now(now)
        await send_temperature_change_event(entity, 22.5, now, True)
        await hass.async_block_till_done()

        assert getattr(entity._regulation_algo, "is_saturated", False) is False
        assert entity._fan_accumulated_error == 26.0
        # Remains in turbo since 26.0 maps to turbo (index 3)
        assert mock_send_fan_mode.call_count == 0

        # 6. Decay further to 22.0.
        # 26.0 - 4.0 = 22.0, mapping to index 2 which is "high".
        now = now + timedelta(minutes=1)
        entity._set_now(now)
        await send_temperature_change_event(entity, 22.5, now, True)
        await hass.async_block_till_done()

        assert entity._fan_accumulated_error == 22.0
        assert mock_send_fan_mode.call_count == 1
        mock_send_fan_mode.assert_has_calls([call("high")])
        mock_send_fan_mode.reset_mock()

        fake_underlying_climate.set_fan_mode("high")
        await hass.async_block_till_done()
        assert entity.fan_mode == "high"

        # 7. Set HVAC mode to OFF. Accumulated error should reset immediately to 0.0.
        await entity.async_set_hvac_mode(VThermHvacMode_OFF)
        await hass.async_block_till_done()
        assert entity._fan_accumulated_error == 0.0

    entity.remove_thermostat()


async def test_over_climate_auto_fan_mode_legacy_immediate_fallback(
    hass: HomeAssistant, skip_hass_states_is_state, skip_send_event
):
    """Test that when CONF_AUTO_FAN_CASCADE_REGULATED is False, the thermostat immediately activates the target fan mode when the 2°C threshold is crossed, rather than using cascade ramping."""
    fan_modes = ["low", "medium", "high", "turbo", "auto"]

    fake_underlying_climate = await create_and_register_mock_climate(
        hass=hass,
        unique_id="mock_climate",
        name="MockClimateName",
        fan_modes=fan_modes,
    )

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: [fake_underlying_climate.entity_id],
            CONF_MINIMAL_ACTIVATION_DELAY: 0,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_TURBO,
            CONF_AUTO_REGULATION_MODE: CONF_AUTO_REGULATION_MEDIUM,
            CONF_AUTO_FAN_CASCADE_REGULATED: False,
            CONF_AUTO_REGULATION_DTEMP: 0.1,
            CONF_AUTO_REGULATION_PERIOD_MIN: 0,
        },
    )

    tz = get_tz(hass)
    now: datetime = datetime.now(tz=tz)

    entity = await create_thermostat(hass, entry, "climate.theoverclimatemockname")
    assert entity
    assert isinstance(entity, ThermostatOverClimate)
    assert entity.is_regulated is True
    assert entity._auto_fan_cascade_regulated is False

    under = entity._underlyings[0]

    # Force heating mode and preset
    await entity.async_set_hvac_mode(VThermHvacMode_HEAT)
    await entity.async_set_preset_mode(VThermPreset.COMFORT)
    assert entity.target_temperature == 18

    # Set initial room temp to target (no delta)
    entity._set_now(now)
    under._last_command_sent_datetime = now - timedelta(seconds=10)
    await send_temperature_change_event(entity, 18, now, True)
    await send_ext_temperature_change_event(entity, 18, now, True)
    await hass.async_block_till_done()

    # The default deactivated fan mode should be set
    assert entity.fan_mode == "low"

    with patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.set_fan_mode"
    ) as mock_send_fan_mode:
        # 1. Trigger temp change that is 2°C below target (target=18, current=16) -> should trigger immediate activation to max speed ("turbo")
        now = now + timedelta(minutes=1)
        entity._set_now(now)
        await send_temperature_change_event(entity, 16, now, True)
        await hass.async_block_till_done()

        # It should immediately change to "turbo" because threshold >= 2 is met
        assert mock_send_fan_mode.call_count >= 1
        mock_send_fan_mode.assert_has_calls([call("turbo")])
        mock_send_fan_mode.reset_mock()

        fake_underlying_climate.set_fan_mode("turbo")
        await hass.async_block_till_done()
        assert entity.fan_mode == "turbo"

        # 2. Change target temp to 17 (delta is 0.5°C below target) -> should deactivate immediately
        now = now + timedelta(minutes=1)
        entity._set_now(now)
        await entity.async_set_temperature(temperature=17)
        await send_temperature_change_event(entity, 16.5, now, True)
        await hass.async_block_till_done()

        # Delta is 0.5°C, which is < 2.0°C. Should immediately fall back to deactivated mode ("low")
        assert mock_send_fan_mode.call_count >= 1
        mock_send_fan_mode.assert_has_calls([call("low")])
        mock_send_fan_mode.reset_mock()

        fake_underlying_climate.set_fan_mode("low")
        await hass.async_block_till_done()
        assert entity.fan_mode == "low"

    entity.remove_thermostat()


async def test_over_climate_auto_fan_mode_cascade_inactive_on_low_fan_mode(
    hass: HomeAssistant, skip_hass_states_get
) -> None:
    """Test that when CONF_AUTO_FAN_CASCADE_REGULATED is True, but auto_fan_mode is CONF_AUTO_FAN_LOW, cascade regulation remains inactive and falls back to legacy logic."""
    fake_underlying_climate = await create_and_register_mock_climate(
        hass,
        "mock_climate",
        "MockClimate",
        fan_modes=["low", "medium", "high", "turbo"],
    )
    await fake_underlying_climate.async_set_fan_mode("low")
    await fake_underlying_climate.async_set_hvac_mode("heat")
    await fake_underlying_climate.async_set_temperature(temperature=18)
    hass.states.async_set(
        "sensor.mock_temp_sensor",
        "18",
        {"device_class": "temperature", "unit_of_measurement": "°C"},
    )
    hass.states.async_set(
        "sensor.mock_ext_temp_sensor",
        "10",
        {"device_class": "temperature", "unit_of_measurement": "°C"},
    )
    await hass.async_block_till_done()

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId3",
        data={
            CONF_NAME: "TheOverClimateMockName",
            CONF_THERMOSTAT_TYPE: CONF_THERMOSTAT_CLIMATE,
            CONF_TEMP_SENSOR: "sensor.mock_temp_sensor",
            CONF_EXTERNAL_TEMP_SENSOR: "sensor.mock_ext_temp_sensor",
            CONF_CYCLE_MIN: 5,
            CONF_TEMP_MIN: 15,
            CONF_TEMP_MAX: 30,
            "eco_temp": 17,
            "comfort_temp": 18,
            "boost_temp": 19,
            CONF_USE_WINDOW_FEATURE: False,
            CONF_USE_MOTION_FEATURE: False,
            CONF_USE_POWER_FEATURE: False,
            CONF_USE_PRESENCE_FEATURE: False,
            CONF_UNDERLYING_LIST: [fake_underlying_climate.entity_id],
            CONF_MINIMAL_ACTIVATION_DELAY: 0,
            CONF_MINIMAL_DEACTIVATION_DELAY: 0,
            CONF_SAFETY_DELAY_MIN: 5,
            CONF_SAFETY_MIN_ON_PERCENT: 0.3,
            CONF_AUTO_FAN_MODE: CONF_AUTO_FAN_LOW,
            CONF_AUTO_REGULATION_MODE: CONF_AUTO_REGULATION_MEDIUM,
            CONF_AUTO_FAN_CASCADE_REGULATED: True,
            CONF_AUTO_REGULATION_DTEMP: 0.1,
            CONF_AUTO_REGULATION_PERIOD_MIN: 0,
        },
    )

    tz = get_tz(hass)
    now: datetime = datetime.now(tz=tz)

    entity = await create_thermostat(hass, entry, "climate.theoverclimatemockname")
    assert entity
    assert isinstance(entity, ThermostatOverClimate)
    assert entity.is_regulated is True
    assert entity._auto_fan_cascade_regulated is True

    # is_cascade_active should be False because auto_fan_mode is CONF_AUTO_FAN_LOW
    assert entity._auto_fan_mode == CONF_AUTO_FAN_LOW

    under = entity._underlyings[0]

    # Force heating mode and preset
    await entity.async_set_hvac_mode(VThermHvacMode_HEAT)
    await entity.async_set_preset_mode(VThermPreset.COMFORT)
    assert entity.target_temperature == 18

    # Set initial temperatures (not saturated)
    entity._set_now(now)
    under._last_command_sent_datetime = now - timedelta(seconds=10)
    await send_temperature_change_event(entity, 18, now, True)
    await send_ext_temperature_change_event(entity, 18, now, True)
    await hass.async_block_till_done()

    # Advance time by 1 minute and change room temp to 5. This triggers saturation.
    now = now + timedelta(minutes=1)
    entity._set_now(now)
    await send_temperature_change_event(entity, 5, now, True)
    await hass.async_block_till_done()

    # Verify that the regulation algorithm is indeed saturated
    assert getattr(entity._regulation_algo, "is_saturated", False) is True

    # But since is_cascade_active should be False, the fan_accumulated_error must remain 0.0
    is_cascade_active = (
        entity.is_regulated
        and entity._auto_fan_mode not in (None, CONF_AUTO_FAN_NONE, CONF_AUTO_FAN_LOW)
        and entity._auto_fan_cascade_regulated
    )
    assert is_cascade_active is False
    assert entity._fan_accumulated_error == 0.0

    entity.remove_thermostat()



