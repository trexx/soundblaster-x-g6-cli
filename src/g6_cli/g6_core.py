import datetime
import re
import sys

import hid
import usb.core
import usb.util

from g6_cli.g6_spec import UsbAudioData, UsbHidDataFragment

# G6 specific USB information
G6_VENDOR_ID = 0x041e
G6_PRODUCT_ID = 0x3256
# The G6 has five interfaces: 1 Audio Control, 2 Audio Streams and 2 HIDs.
# The endpoint of the first interface is used for audio control.
# The endpoint of the fourth interface is used by SoundBlaster Connect for HID communication - so
# will we, since data sent to the third interface is ignored by the device.
G6_AUDIO_CONTROL_INTERFACE = 0
G6_HID_INTERFACE = 4

# The udev rule to create in /etc/udev/rules.d/50-soundblaster-x-g6.rules
UDEV_RULE = f'SUBSYSTEM=="usb", ATTRS{{idVendor}}=="{G6_VENDOR_ID:04x}", ATTRS{{idProduct}}=="{G6_PRODUCT_ID:04x}", TAG+="uaccess"'

# The payloads available to send to the G6
PAYLOAD_HEX_LINE_PATTERN = r'^[a-f0-9]{128}$'


class G6Device:
    AVAILABILITY_CHECK_INTERVAL_SECONDS = 0.1

    class AudioInterface:
        def __init__(self, usb_device: usb.core.Device, device_path: str, b_configuration_value: int):
            self.__usb_device = usb_device
            self.__device_path = device_path
            self.__b_configuration_value = b_configuration_value
            self.__available = False
            self.__availability_last_checked = None
            self.__kernel_driver_attached = True
            self.__interface_claimed = False

        def get_device_path(self) -> str:
            return self.__device_path

        def get_b_configuration_value(self) -> int:
            return self.__b_configuration_value

        def is_available(self, dry_run: bool) -> bool:
            try:
                # check availability in intervals
                if self.__availability_last_checked is None or (
                        self.__availability_last_checked + G6Device.AVAILABILITY_CHECK_INTERVAL_SECONDS) < datetime.datetime.now().timestamp():
                    self.__availability_last_checked = datetime.datetime.now().timestamp()

                    # check the G6 is connected
                    device_connected = _detect_device_audio_control().get_device_path() == self.__device_path
                    if device_connected:
                        # refresh kernel driver attached state
                        self.__kernel_driver_attached = self.__check_kernel_driver_attached(dry_run=dry_run)

                    # interface is available if the G6 is connected and the kernel driver is not attached
                    self.__available = device_connected and not self.__kernel_driver_attached and self.__interface_claimed
            except IOError:
                print(f'Failed to check availability of AudioControl interface at path: {self.__device_path}',
                      file=sys.stderr)
                self.__available = False

            return self.__available

        def claim_interface(self, dry_run: bool):
            # refresh kernel driver attached state
            self.__kernel_driver_attached = self.__check_kernel_driver_attached(dry_run=dry_run)

            # try to detach the kernel driver
            if self.__kernel_driver_attached:
                try:
                    print('About to detach kernel driver from G6 device ...')
                    if dry_run:
                        print('This is a dry run. No kernel driver is detached from the G6 device!')
                        self.__kernel_driver_attached = False
                    else:
                        self.__usb_device.detach_kernel_driver(G6_AUDIO_CONTROL_INTERFACE)
                        self.__kernel_driver_attached = False
                    print('About to detach kernel driver from G6 device: ok.')
                except usb.core.USBError as e:
                    print('About to detach kernel driver from G6 device: failed!')
                    print(f'Failed to detach kernel driver from G6 device: {e}', file=sys.stderr)
                    self.__interface_claimed = False

            # try to claim the interface
            if not self.__kernel_driver_attached:
                try:
                    # claim the interface
                    print('About to claim the audio interface from G6 device ...')
                    if dry_run:
                        print('This is a dry run. No interface is claimed from the G6 device!')
                    else:
                        usb.util.claim_interface(self.__usb_device, G6_AUDIO_CONTROL_INTERFACE)
                    self.__interface_claimed = True
                    print('About to claim the audio interface from G6 device: ok.')

                    # try to configure the device
                    try:
                        print('About to configure USB device ...')
                        if dry_run:
                            print('This is a dry run. No configuration is applied to the G6 device!')
                        else:
                            self.__usb_device.set_configuration(self.__b_configuration_value)
                        print('About to configure USB device: ok.')
                    except usb.core.USBError as e:
                        print('About to configure USB device: failed.')
                        print(f'USB device is already in a configured state: {e}', file=sys.stderr)

                except usb.core.USBError as e:
                    print('About to claim the audio interface from G6 device: failed!')
                    print(f'Failed to claim the audio interface from G6 device: {e}', file=sys.stderr)
                    self.__interface_claimed = False

        def release_interface(self, dry_run: bool):
            # refresh kernel driver attached state
            self.__kernel_driver_attached = self.__check_kernel_driver_attached(dry_run=dry_run)

            # try to release the interface
            if self.__interface_claimed:
                try:
                    print('About to release the audio interface from G6 device ...')
                    usb.util.release_interface(self.__usb_device, G6_AUDIO_CONTROL_INTERFACE)
                    self.__interface_claimed = False
                    print('About to release the audio interface from G6 device: ok.')
                except usb.core.USBError as e:
                    print('About to release the audio interface from G6 device: failed!')
                    print(f'Failed to release the audio interface from G6 device: {e}', file=sys.stderr)

            # dispose all resources
            try:
                print('About to dispose USB device resources ...')
                usb.util.dispose_resources(self.__usb_device)
                print('About to dispose USB device resources: ok.')
            except usb.core.USBError as e:
                print('About to dispose USB device resources: failed!')
                print(f'Failed to dispose USB device resources: {e}', file=sys.stderr)

            # try to attach the kernel driver again
            if not self.__interface_claimed:
                try:
                    print('About to attach kernel driver to G6 device ...')
                    self.__usb_device.attach_kernel_driver(G6_AUDIO_CONTROL_INTERFACE)
                    self.__kernel_driver_attached = True
                    print('About to attach kernel driver to G6 device: ok.')
                except usb.core.USBError as e:
                    print('About to attach kernel driver to G6 device: failed!')
                    print(f'Failed to attach kernel driver to G6 device: {e}', file=sys.stderr)

        def send_audio_data_to_device(self, audio_data_list: list[UsbAudioData], dry_run: bool, debug: bool) -> None:
            """
            Convert the audio_data_list to a list of hex strings and send them to the device.
            :param audio_data_list: The list of UsbAudioData objects to send to the G6.
            :param dry_run: Whether to simulate communication with the device for program testing purposes.
            :param debug: Print communication data with the G6 device to the console.

            A bmRequestType has a length of one byte and is a bitmap, containing three fields:
            - Direction (Bit 7)
            - Type (Bits 6-5)
            - Recipient (Bits 4-0)
            (see: https://beyondlogic.org/usbnutshell/usb6.shtml)

            Since the kernel sound driver snd-usb-audio has the claim to the audio interface, it blocks regular Type=Class(=0x1) requests. But the kernel driver would allow Type=Vendor(=0x2) requests.
            We could detach the interface from the kernel and send the Type=Class(0x1) request directly to the interface, but this would require us to reattach the interface to the kernel afterward.
            In this case, we would also have to reload ALSA and PulseAudio (through PipeWire) every time, since both would have lost the connection to the sound card.

            -> But unfortunately, the G6 does not support Vendor requests. So we have to detach the interface from the kernel.
               This forces us to let the kernel driver lose connection, and we have to reconfigure ALSA and PulseAudio to make sound for the system available again.
            """

            # check the interface is claimed
            if not dry_run and not self.__interface_claimed:
                raise IOError(f"The audio interface of the G6 device is not claimed. Please claim the interface first!")

            # check the kernel driver is not attached
            if not dry_run and self.__kernel_driver_attached:
                raise IOError(f"The kernel driver of the G6 device is attached. Please detach the kernel driver first!")

            # Send audio_data to device
            print('Sending audio data to G6 ...')
            transmission_ok = True
            for audio_data in audio_data_list:
                bm_request_type_int = int.from_bytes(audio_data.get_bm_request_type(), byteorder='little')
                b_request_int = int.from_bytes(audio_data.get_b_request(), byteorder='little')
                w_value_int = int.from_bytes(audio_data.get_w_value(), byteorder='little')
                w_index_int = int.from_bytes(audio_data.get_w_index(), byteorder='little')

                if debug:
                    print(f'bmRequestType: {audio_data.get_bm_request_type().hex()}')
                    print(f'bRequest: {audio_data.get_b_request().hex()}')
                    print(f'wValue: {audio_data.get_w_value().hex()}')
                    print(f'wIndex: {audio_data.get_w_index().hex()}')
                    print(f'wLength: {audio_data.get_w_length().hex()}')
                    print(f'data_fragment: {audio_data.get_data_fragment().hex()}')

                # dry run: do not send any data to the device
                if dry_run:
                    print('This is a dry run. No data has been sent to the G6!')
                else:
                    # issue a 'get active configuration' request
                    configuration = self.__usb_device.get_active_configuration()

                    # execute the control request
                    try:
                        result = self.__usb_device.ctrl_transfer(
                            bmRequestType=bm_request_type_int,
                            bRequest=b_request_int,
                            wValue=w_value_int,
                            wIndex=w_index_int,
                            data_or_wLength=audio_data.get_data_fragment(),
                            timeout=1000
                        )
                        if debug:
                            print(f'Sending audio data to G6: ok -> {result}')
                    except usb.core.USBError as e:
                        transmission_ok = False
                        print(f'Sending audio data to G6: failed!')
                        print(f'Failed to send audio data to G6 device: {e}', file=sys.stderr)
            print(f'Sending audio data to G6: {"ok" if transmission_ok else "failed"}.')

        def __check_kernel_driver_attached(self, dry_run: bool) -> bool:
            print('About to check if kernel driver is attached to G6 device ...')
            try:
                if dry_run:
                    print(
                        'About to check if kernel driver is attached to G6 device: This is a dry run - kernel driver is not checked!')
                    return False
                else:
                    if self.__usb_device.is_kernel_driver_active(G6_AUDIO_CONTROL_INTERFACE):
                        print('About to check if kernel driver is attached to G6 device: kernel is attached.')
                        return True
                    else:
                        print('About to check if kernel driver is attached to G6 device: kernel is detached.')
                        return False
            except usb.core.USBError as e:
                print('About to check if kernel driver is attached to G6 device: failed!')
                print(f'Failed to check if kernel driver is attached to G6 device: {e}', file=sys.stderr)
                return True  # consider the kernel driver attached by default

    class HidInterface:

        def __init__(self, device_path: str):
            self.__device_path = device_path
            self.__available = False
            self.__availability_last_checked = None

        def is_available(self, dry_run: bool) -> bool:
            try:
                if self.__availability_last_checked is None or (
                        self.__availability_last_checked + G6Device.AVAILABILITY_CHECK_INTERVAL_SECONDS) < datetime.datetime.now().timestamp():
                    self.__availability_last_checked = datetime.datetime.now().timestamp()
                    # check the G6 is connected, and thus available
                    print(f"About to check availability of HID interface at path: {self.__device_path} ...")
                    if dry_run:
                        print(f"About to check availability of HID interface at path: {self.__device_path}:"
                              f" This is a dry run. No availability check is performed!")
                        self.__available = True
                    else:
                        self.__available = _detect_device_hid().get_device_path() == self.get_device_path()
                        print(f"About to check availability of HID interface at path: {self.__device_path}:"
                              f" {"available" if self.__available else "unavailable"}")
            except IOError:
                print(f'Failed to check availability of HID interface at path: {self.__device_path}', file=sys.stderr)
                self.__available = False
            return self.__available

        def get_device_path(self) -> str:
            return self.__device_path

        def send_hid_data_to_device(self, hid_data_list: list[UsbHidDataFragment], dry_run: bool, debug: bool) -> None:
            """
            Send the payload_hex_lines to an endpoint from the usb device, identified by the device_path.
            :param hid_data_list: The list of UsbHidDataFragment objects to send to the G6. Each data line must be 128 characters long (64 bytes).
            :param dry_run: whether to simulate communication with the device for program testing purposes.
                            If set to true, no data is sent to the G6!
            :param debug: Print communication data with the G6 device to the console.
            """
            try:
                print(f"Opening the device '{self.__device_path}' ...")
                h = hid.device()
                try:
                    if dry_run:
                        print(f"Opening the device '{self.__device_path}':"
                              f" This is a dry run. Device has not been opened.")
                    else:
                        h.open_path(self.__device_path)
                        print(f"Opening the device '{self.__device_path}': ok.")

                        print(f"Manufacturer: '{h.get_manufacturer_string()}'")
                        print(f"Product: '{h.get_product_string()}'")
                        print(f"Serial No: '{h.get_serial_number_string()}'")

                    # enable non-blocking mode
                    if not dry_run:
                        h.set_nonblocking(1)

                    # Convert objects to hex_lines
                    payload_hex_lines = [hid_data.__str__() for hid_data in hid_data_list]

                    # Validate all hex_lines
                    regex_pattern = re.compile(PAYLOAD_HEX_LINE_PATTERN)
                    for hex_line in payload_hex_lines:
                        if not regex_pattern.fullmatch(hex_line):
                            raise ValueError(
                                f"The following hex_line is part of the payload, but it did not match the expected regex pattern! "
                                f"Pattern: '{PAYLOAD_HEX_LINE_PATTERN}'; "
                                f"Hex-Line: '{hex_line}'")

                    print("Sending HID data to G6 ...")
                    for hex_line in payload_hex_lines:
                        # Prepend an additional zero byte as report_id to the hex_line. Otherwise, the first byte from the actual
                        # 64 byte payload is cut off, since it is interpreted as report_id and thus, not sent to the device.
                        hex_line = '00' + hex_line

                        # Convert the hex string to a list of integers
                        integer_list = [int(hex_line[i:i + 2], 16) for i in range(0, len(hex_line), 2)]

                        # send the data to the device
                        if debug:
                            print(hex_line)
                        if dry_run:
                            print('This is a dry run. No data has been sent to the G6!')
                        else:
                            h.write(integer_list)

                        # read back the response
                        if not dry_run:
                            while True:
                                response = h.read(64)
                                if response and debug:
                                    print(f"Response: {response}")
                                else:
                                    break
                    print("Sending HID data to G6: ok.")
                finally:
                    if not dry_run:
                        print("Closing the device ...")
                        h.close()
                        print("Closing the device: ok.")

            except IOError as ex:
                print(f'Unable to open a connection to the device by path: {self.__device_path}')
                print(ex)
                print('\nAre the udev rules set and used by the kernel?')
                print(
                    'Create a udev-rule file at `/etc/udev/rules.d/50-soundblaster-x-g6.rules` with the following content:')
                print(UDEV_RULE)
                print(
                    '\nIf the file already exists, it might not be used by the kernel. Try to reload the configuration with:')
                print("`sudo udevadm trigger`")

    def __init__(self, audio_interface: AudioInterface, hid_interface: HidInterface, dry_run: bool, debug: bool):
        self.__audio_interface = audio_interface
        self.__hid_interface = hid_interface
        self.__dry_run = dry_run
        self.__debug = debug

    def get_audio_interface_device_path(self) -> str:
        return self.__audio_interface.get_device_path()

    def get_hid_interface_device_path(self) -> str:
        return self.__hid_interface.get_device_path()

    def is_audio_interface_available(self) -> bool:
        return self.__audio_interface.is_available(dry_run=self.__dry_run)

    def claim_audio_interface(self):
        self.__audio_interface.claim_interface(dry_run=self.__dry_run)

    def release_audio_interface(self):
        self.__audio_interface.release_interface(dry_run=self.__dry_run)

    def send_audio_data_to_device(self, audio_data_list: list[UsbAudioData]) -> None:
        self.__audio_interface.send_audio_data_to_device(audio_data_list=audio_data_list, dry_run=self.__dry_run,
                                                         debug=self.__debug)

    def is_hid_interface_available(self) -> bool:
        return self.__hid_interface.is_available(dry_run=self.__dry_run)

    def send_hid_data_to_device(self, hid_data_list: list[UsbHidDataFragment]) -> None:
        self.__hid_interface.send_hid_data_to_device(hid_data_list=hid_data_list, dry_run=self.__dry_run,
                                                     debug=self.__debug)


def list_all_hid_devices():
    """
    Simply prints information of all detected usb devices to the console
    """
    for device_dict in hid.enumerate():
        keys = list(device_dict.keys())
        keys.sort()
        for key in keys:
            print("%s : %s" % (key, device_dict[key]))
        print()


def detect_device(dry_run: bool, debug: bool) -> G6Device:
    """
    Tries to detect the SoundBlaster X G6 device and returns the device path to it.

    From all connected USB HID devices, we filter all devices that do not match the desired vendor_id and product_id.
    Since we know, that we have to communicate with USB-Interface 0 (AudioControl) and 4 (HID), we also filter all
    other interfaces of the device. This approach is required, because the G6's endpoint of USB-Interface 3 (HID)
    ignores any data transmitted to it. We have to use the endpoint of the fourth interface!

    If the device itself or the required interfaces could not be found, an IOError is risen to let the program terminate.

    Example for a device_path: "b'5-2.1:1.4'"
    - Bus 5
    - Port 2 (USB-Hub at Bus)
    - Port 1 (G6 at Hub)
    - bConfigurationValue 1
    - Interface 4

    A tree output of all connected USB devices can be generated with the command `lsusb -t`.
    :return: The unique device_path to the G6.
    """
    return G6Device(audio_interface=_detect_device_audio_control(),
                    hid_interface=_detect_device_hid(),
                    dry_run=dry_run,
                    debug=debug)


def _detect_device_audio_control() -> G6Device.AudioInterface:
    # Try to detect the G6 device's AudioControl interface path.
    usb_device = usb.core.find(idVendor=G6_VENDOR_ID, idProduct=G6_PRODUCT_ID)
    if usb_device is None:
        raise IOError(
            f"No SoundBlaster X G6 device could be found by pyusb library having vendor_id='{G6_VENDOR_ID:#x}' and "
            f"product_id='{G6_PRODUCT_ID:#x}'. Is the device connected to your system? Are you allowed to access the "
            f"device (missing udev-rules in linux)?")

    # List all interfaces of the device
    for configuration in usb_device:
        # Each interface number may have multiple alternate settings
        for interface in configuration:
            if interface.bInterfaceNumber == G6_AUDIO_CONTROL_INTERFACE:
                device_path = f'{usb_device.bus}-{".".join([str(p) for p in usb_device.port_numbers])}.{usb_device.address}:{interface.bInterfaceNumber}.{interface.bAlternateSetting}'
                return G6Device.AudioInterface(usb_device=usb_device,
                                               device_path=device_path,
                                               b_configuration_value=configuration.bConfigurationValue)

    # If the device itself or the required interfaces could not be found, an IOError is risen to let the program terminate.
    raise IOError(f"The SoundBlaster X G6 device could be found having vendor_id='{G6_VENDOR_ID:#x}' and "
                  f"product_id='{G6_PRODUCT_ID:#x}'. But the required AudioControl interface does not seem to be "
                  f"available. Something is wrong here, and thus, the program execution is terminated!")


def _detect_device_hid() -> G6Device.HidInterface:
    # Try to detect the G6 device's HID interface path.
    hid_device_found = False
    hid_interface_path: str = ''
    for device_dict in hid.enumerate():
        if device_dict['vendor_id'] == G6_VENDOR_ID and device_dict['product_id'] == G6_PRODUCT_ID:
            hid_device_found = True
            if device_dict['interface_number'] == G6_HID_INTERFACE:
                hid_interface_path = device_dict['path']
                print(f'Device with HID interface detected at path: {hid_interface_path}')
                return G6Device.HidInterface(device_path=hid_interface_path)

    # If the device itself or the fourth interface could not be found, an IOError is risen to let the program terminate.
    if hid_device_found:
        raise IOError(f"The SoundBlaster X G6 device could be found having vendor_id='{G6_VENDOR_ID:#x}' and "
                      f"product_id='{G6_PRODUCT_ID:#x}'. But the required HID interface does not seem to be "
                      f"available. Something is wrong here, and thus, the program execution is terminated!")
    else:
        raise IOError(
            f"No SoundBlaster X G6 device could be found by hidapi library having vendor_id='{G6_VENDOR_ID:#x}' and "
            f"product_id='{G6_PRODUCT_ID:#x}'. Is the device connected to your system? Are you allowed to access the "
            f"device (missing udev-rules in linux)?")
