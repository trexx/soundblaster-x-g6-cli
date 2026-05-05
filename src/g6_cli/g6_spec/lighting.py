from __future__ import annotations

from g6_cli.g6_spec import UsbHidDataFragment, EMPTY_ADDITIONAL_PAYLOAD, DataFragmentMode

# Volume ring light (bright white LED under the volume knob).
# Command 0x0e, audio_feature byte: 0x00=enabled, 0x01=disabled.
LIGHTING_VOLUME_RING_MODE             = bytes.fromhex('3903')
LIGHTING_VOLUME_RING_INTERMEDIATE     = bytes.fromhex('000e')
LIGHTING_VOLUME_RING_COMMIT_MODE      = bytes.fromhex('3901')
LIGHTING_VOLUME_RING_COMMIT_INTERMEDIATE = bytes.fromhex('0100')

LIGHTING_DISABLE_MODE = bytes.fromhex('3A02')
LIGHTING_DISABLE_INTERMEDIATE = bytes.fromhex('0600')

LIGHTING_ENABLE_PRE_1_MODE = bytes.fromhex('3A02')
LIGHTING_ENABLE_PRE_1_INTERMEDIATE = bytes.fromhex('0601')

LIGHTING_ENABLE_PRE_2_MODE = bytes.fromhex('3A06')
LIGHTING_ENABLE_PRE_2_INTERMEDIATE = bytes.fromhex('0400')

LIGHTING_ENABLE_RGB_MODE = bytes.fromhex('3A09')
LIGHTING_ENABLE_RGB_INTERMEDIATE = bytes.fromhex('0A00')
LIGHTING_ENABLE_RGB_AUDIO_FEATURE = bytes.fromhex('03')


def lighting_volume_ring(enable: bool) -> list[UsbHidDataFragment]:
    return [
        UsbHidDataFragment(
            mode=LIGHTING_VOLUME_RING_MODE,
            intermediate=LIGHTING_VOLUME_RING_INTERMEDIATE,
            audio_feature=bytes.fromhex('00') if enable else bytes.fromhex('01'),
            value=bytes.fromhex('00000000'),
            additional_payload=EMPTY_ADDITIONAL_PAYLOAD,
        ),
        UsbHidDataFragment(
            mode=LIGHTING_VOLUME_RING_COMMIT_MODE,
            intermediate=LIGHTING_VOLUME_RING_COMMIT_INTERMEDIATE,
            audio_feature=bytes.fromhex('00'),
            value=bytes.fromhex('00000000'),
            additional_payload=EMPTY_ADDITIONAL_PAYLOAD,
        ),
    ]


def lighting_disable() -> list[UsbHidDataFragment]:
    """
    Disable the RGB lighting on the G6 device.
    :return: The list of UsbHidDataFragment objects to send to the G6, to disable the RGB lighting.
    """
    return [
        UsbHidDataFragment(
            mode=LIGHTING_DISABLE_MODE,
            intermediate=LIGHTING_DISABLE_INTERMEDIATE,
            audio_feature=bytes.fromhex('00'),
            value=bytes.fromhex('0000 0000'),
            additional_payload=EMPTY_ADDITIONAL_PAYLOAD,
        )
    ]


def lighting_enable_set_rgb(red: int, green: int, blue: int) -> list[UsbHidDataFragment]:
    """
    Set the RGB lighting on the G6 device to the specified color.
    :param red: The red component of the color (0..255).
    :param green: The green component of the color (0..255).
    :param blue: The blue component of the color (0..255).
    :return: The list of UsbHidDataFragment objects to send to the G6, to set the RGB lighting to the specified color.
    """
    if red < 0 or red > 255:
        raise ValueError(f"red must be between 0 and 255, got {red}")
    if green < 0 or green > 255:
        raise ValueError(f"green must be between 0 and 255, got {green}")
    if blue < 0 or blue > 255:
        raise ValueError(f"blue must be between 0 and 255, got {blue}")

    usb_hid_fragment_list: list[UsbHidDataFragment] = []
    for i in range(3):
        usb_hid_fragment_list.append(
            UsbHidDataFragment(
                mode=LIGHTING_ENABLE_PRE_1_MODE,
                intermediate=LIGHTING_ENABLE_PRE_1_INTERMEDIATE,
                audio_feature=bytes.fromhex('00'),
                value=bytes.fromhex('0000 0000'),
                additional_payload=EMPTY_ADDITIONAL_PAYLOAD
            )
        )
        usb_hid_fragment_list.append(
            UsbHidDataFragment(
                mode=LIGHTING_ENABLE_PRE_2_MODE,
                intermediate=LIGHTING_ENABLE_PRE_2_INTERMEDIATE,
                audio_feature=LIGHTING_ENABLE_RGB_AUDIO_FEATURE,
                value=bytes.fromhex('0100 0100'),
                additional_payload=EMPTY_ADDITIONAL_PAYLOAD
            )
        )
        usb_hid_fragment_list.append(
            UsbHidDataFragment(
                mode=LIGHTING_ENABLE_RGB_MODE,
                intermediate=LIGHTING_ENABLE_RGB_INTERMEDIATE,
                audio_feature=LIGHTING_ENABLE_RGB_AUDIO_FEATURE,
                value=bytes.fromhex('0101ff' + format(blue, '02x')),
                additional_payload=bytes.fromhex(format(green, '02x') + format(red, '02x') + ''.zfill(104)),
            )
        )

    return usb_hid_fragment_list
