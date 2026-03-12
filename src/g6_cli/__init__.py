import argparse
import os.path
import tempfile

from g6_cli.g6_api import G6Api
from g6_cli.g6_spec import (
    AudioFeature,
    Channel,
    PlaybackFilter,
    SmartVolumeSpecialHex,
    BOTH_CHANNELS,
)
from g6_cli.g6_spec.decoder import DecoderMode
from g6_cli.g6_spec.recording import MicrophoneEqualizerPreset
from g6_cli.g6_util import to_bool

VERSION = '1.0.0'

# The name of the temporary file to remember the last toggle state in. If the file could not be found. The program
# lets the G6 to toggle to Speakers by default.
TOGGLE_STATE_TEMP_FILE_NAME = 'g6-cli-toggle-state'
TOGGLE_STATE_SPEAKERS = 'Speakers'
TOGGLE_STATE_HEADPHONES = 'Headphones'


def _channels_from_cli(value: str) -> set[Channel]:
    """
    Convert a CLI channels string into a set[Channel].
    :param value: One of 'Both', 'Left', 'Right'
    :return: A set[Channel] compatible with g6_api methods.
    """
    if value == 'Both':
        return BOTH_CHANNELS
    elif value == 'Left':
        return {Channel.CHANNEL_1}
    elif value == 'Right':
        return {Channel.CHANNEL_2}
    else:
        raise ValueError(f'Unsupported channels value: {value}')


def _decoder_mode_from_cli(value: str) -> DecoderMode:
    """
    Convert a CLI decoder mode string into a DecoderMode enum.
    :param value: One of 'Normal', 'Full', 'Night'
    :return: The DecoderMode enum value.
    """
    return DecoderMode[value.upper()]


def parse_cli_args():
    """
    Parse the CLI arguments using argparse.
    Prints the CLI help to console and raises an error if the arguments are invalid.
    :return: The parsed cli args object
    """
    numbers_0_100 = [i for i in range(0, 101)]
    numbers_0_30_step_10 = [i * 10 for i in range(0, 4)]
    numbers_0_100_step_10 = [i * 10 for i in range(0, 11)]
    numbers_0_100_step_20 = [i * 20 for i in range(0, 6)]
    enabled_disabled = ['Enabled', 'Disabled']
    channels = ['Both', 'Left', 'Right']
    decoder_modes = ['Normal', 'Full', 'Night']

    parser = argparse.ArgumentParser(usage="soundblaster-x-g6-cli", description='SoundBlaster X G6 CLI')
    #
    # Device / services
    #
    general_options_group = parser.add_argument_group('General options')
    general_options_group.add_argument('--dry-run', required=False, action='store_true',
                                       help='Used to verify the available hex_line files, without making any calls against the G6 device.')
    general_options_group.add_argument('--debug', required=False, action='store_true',
                                       help='Print communication data with the G6 device to the console.')
    general_options_group.add_argument('--version', action='version', version=f'soundblaster-x-g6-cli {VERSION}')

    general_options_group.add_argument('--claim-and-release', required=False, action='store_true',
                                       help='Let the application exclusively claim the G6\'s USB AudioControl interface from the kernel and release it afterwards.'
                                            ' This will disconnect the G6 device from the kernel sound driver "snd-usb-audio" leading the system not having any audio output.'
                                            ' Use `--reload-audio-services` to reload the kernel sound driver and make the audio output available again.')
    general_options_group.add_argument('--reload-audio-services', required=False, action='store_true',
                                       help='Reload ALSA and restart user PipeWire services.')
    general_options_group.add_argument('--reload-audio-services-no-sudo', required=False, action='store_true',
                                       help='Reload audio services, but do not use sudo for ALSA reload.')

    #
    # Playback [HID / Audio]
    #
    playback_hid_group = parser.add_argument_group('Playback [HID]',
                                                   description="Control basic features using the G6's USB HID interface.")
    playback_audio_group = parser.add_argument_group('Playback [Audio]',
                                                     description="Control advanced features using the G6's USB AudioControl interface. See `--claim-and-release` how to use these features.")

    playback_hid_group.add_argument('--toggle-output', required=False, action='store_true',
                                    help='Toggles the sound output between Speakers and Headphones.')
    playback_hid_group.add_argument('--set-output', required=False, type=str,
                                    choices=[TOGGLE_STATE_SPEAKERS, TOGGLE_STATE_HEADPHONES],
                                    metavar="{Speakers|Headphones}",
                                    help='Sets the sound output to the specified option.')
    playback_audio_group.add_argument('--playback-mute', required=False, type=str, choices=enabled_disabled,
                                      metavar="{Enabled|Disabled}",
                                      help='Mute/unmute playback.')
    playback_audio_group.add_argument('--playback-volume', required=False, type=int, choices=numbers_0_100,
                                      metavar="{0..100}",
                                      help='Set playback volume as integer.')
    playback_audio_group.add_argument('--playback-volume-channels', required=False, type=str, choices=channels,
                                      default='Both',
                                      metavar="{Both|Left|Right}",
                                      help='Set playback volume channels for --playback-volume.')
    playback_audio_group.add_argument('--playback-speakers-to-stereo', required=False, action='store_true',
                                      help='Switch speakers output to stereo.')
    playback_audio_group.add_argument('--playback-speakers-to-5-1', required=False, action='store_true',
                                      help='Switch speakers output to 5.1.')
    playback_audio_group.add_argument('--playback-speakers-to-7-1', required=False, action='store_true',
                                      help='Switch speakers output to 7.1.')
    playback_audio_group.add_argument('--playback-headphones-to-stereo', required=False, action='store_true',
                                      help='Switch headphones output to stereo.')
    playback_audio_group.add_argument('--playback-headphones-to-5-1', required=False, action='store_true',
                                      help='Switch headphones output to 5.1.')
    playback_audio_group.add_argument('--playback-headphones-to-7-1', required=False, action='store_true',
                                      help='Switch headphones output to 7.1.')
    playback_hid_group.add_argument('--playback-direct-mode', required=False, type=str, choices=enabled_disabled,
                                    metavar="{Enabled|Disabled}",
                                    help='Enable/disable Direct Mode.')
    playback_hid_group.add_argument('--playback-spdif-out-direct-mode', required=False, type=str,
                                    choices=enabled_disabled,
                                    metavar="{Enabled|Disabled}",
                                    help='Enable/disable SPDIF-Out Direct Mode.')
    playback_hid_group.add_argument('--playback-filter', required=False, type=str,
                                    choices=[e.name for e in PlaybackFilter],
                                    metavar=(
                                        "{FAST_ROLL_OFF_MINIMUM_PHASE|SLOW_ROLL_OFF_MINIMUM_PHASE|"
                                        "FAST_ROLL_OFF_LINEAR_PHASE|SLOW_ROLL_OFF_LINEAR_PHASE}"
                                    ),
                                    help='Set playback filter by enum name.')

    #
    # Decoder [HID]
    #
    decoder_hid_group = parser.add_argument_group('Decoder [HID]',
                                                  description="Control decoder features using the G6's USB HID interface.")
    decoder_hid_group.add_argument('--decoder-mode', required=False, type=str,
                                   choices=decoder_modes,
                                   metavar="{Normal|Full|Night}",
                                   help='Set decoder mode.')

    #
    # Lighting [HID]
    #
    lighting_hid_group = parser.add_argument_group('Lighting [HID]',
                                                   description="Control lighting features using the G6's USB HID interface.")
    lighting_hid_group.add_argument('--lighting-disable', required=False, action='store_true',
                                    help='Disable device lighting.')
    lighting_hid_group.add_argument('--lighting-rgb', required=False, type=int, nargs=3,
                                    metavar=('{0..255}', '{0..255}', '{0..255}'),
                                    help='Enable lighting and set RGB.')

    #
    # Mixer [Audio]
    #
    mixer_audio_group = parser.add_argument_group('Mixer [Audio]',
                                                  description="Control mixer features using the G6's USB AudioControl interface. See `--claim-and-release` how to use these features.")
    mixer_audio_group.add_argument('--mixer-playback-mute', required=False, type=str, choices=enabled_disabled,
                                   metavar="{Enabled|Disabled}",
                                   help='Mute/unmute mixer playback.')

    mixer_audio_group.add_argument('--mixer-monitoring-line-in-mute', required=False, type=str,
                                   choices=enabled_disabled,
                                   metavar="{Enabled|Disabled}",
                                   help='Mute/unmute line-in monitoring.')
    mixer_audio_group.add_argument('--mixer-monitoring-line-in-volume', required=False, type=int,
                                   choices=numbers_0_100_step_10,
                                   metavar="{0|10|20|..|100}",
                                   help='Set line-in monitoring volume as integer.')
    mixer_audio_group.add_argument('--mixer-monitoring-line-in-volume-channels', required=False, type=str,
                                   choices=channels, default='Both',
                                   metavar="{Both|Left|Right}",
                                   help='Define channels for --mixer-monitoring-line-in-volume.')

    mixer_audio_group.add_argument('--mixer-monitoring-external-mic-mute', required=False, type=str,
                                   choices=enabled_disabled,
                                   metavar="{Enabled|Disabled}",
                                   help='Mute/unmute external mic monitoring.')
    mixer_audio_group.add_argument('--mixer-monitoring-external-mic-volume', required=False, type=int,
                                   choices=numbers_0_100_step_10,
                                   metavar="{0|10|20|..|100}",
                                   help='Set external mic monitoring volume as integer.')
    mixer_audio_group.add_argument('--mixer-monitoring-external-mic-volume-channels', required=False, type=str,
                                   choices=channels, default='Both',
                                   metavar="{Both|Left|Right}",
                                   help='Define channels for --mixer-monitoring-external-mic-volume.')

    mixer_audio_group.add_argument('--mixer-monitoring-spdif-in-mute', required=False, type=str,
                                   choices=enabled_disabled,
                                   metavar="{Enabled|Disabled}",
                                   help='Mute/unmute spdif-in monitoring.')
    mixer_audio_group.add_argument('--mixer-monitoring-spdif-in-volume', required=False, type=int,
                                   choices=numbers_0_100_step_10,
                                   metavar="{0|10|20|..|100}",
                                   help='Set spdif-in monitoring volume as integer.')
    mixer_audio_group.add_argument('--mixer-monitoring-spdif-in-volume-channels', required=False, type=str,
                                   choices=channels, default='Both',
                                   metavar="{Both|Left|Right}",
                                   help='Define channels for --mixer-monitoring-spdif-in-volume.')

    mixer_audio_group.add_argument('--mixer-recording-line-in-mute', required=False, type=str, choices=enabled_disabled,
                                   metavar="{Enabled|Disabled}",
                                   help='Mute/unmute line-in recording.')
    mixer_audio_group.add_argument('--mixer-recording-line-in-volume', required=False, type=int,
                                   choices=numbers_0_100_step_10,
                                   metavar="{0|10|20|..|100}",
                                   help='Set line-in recording volume as integer.')
    mixer_audio_group.add_argument('--mixer-recording-line-in-volume-channels', required=False, type=str,
                                   choices=channels, default='Both',
                                   metavar="{Both|Left|Right}",
                                   help='Define channels for --mixer-recording-line-in-volume.')

    mixer_audio_group.add_argument('--mixer-recording-external-mic-mute', required=False, type=str,
                                   choices=enabled_disabled,
                                   metavar="{Enabled|Disabled}",
                                   help='Mute/unmute external mic recording.')
    mixer_audio_group.add_argument('--mixer-recording-external-mic-volume', required=False, type=int,
                                   choices=numbers_0_100_step_10,
                                   metavar="{0|10|20|..|100}",
                                   help='Set external mic recording volume as integer.')
    mixer_audio_group.add_argument('--mixer-recording-external-mic-volume-channels', required=False, type=str,
                                   choices=channels, default='Both',
                                   metavar="{Both|Left|Right}",
                                   help='Define channels for --mixer-recording-external-mic-volume.')

    mixer_audio_group.add_argument('--mixer-recording-spdif-in-mute', required=False, type=str,
                                   choices=enabled_disabled,
                                   metavar="{Enabled|Disabled}",
                                   help='Mute/unmute spdif-in recording.')
    mixer_audio_group.add_argument('--mixer-recording-spdif-in-volume', required=False, type=int,
                                   choices=numbers_0_100_step_10,
                                   metavar="{0|10|20|..|100}",
                                   help='Set spdif-in recording volume as integer.')
    mixer_audio_group.add_argument('--mixer-recording-spdif-in-volume-channels', required=False, type=str,
                                   choices=channels, default='Both',
                                   metavar="{Both|Left|Right}",
                                   help='Define channels for --mixer-recording-spdif-in-volume.')

    mixer_audio_group.add_argument('--mixer-recording-what-u-hear-mute', required=False, type=str,
                                   choices=enabled_disabled,
                                   metavar="{Enabled|Disabled}",
                                   help='Mute/unmute what-u-hear recording.')
    mixer_audio_group.add_argument('--mixer-recording-what-u-hear-volume', required=False, type=int,
                                   choices=numbers_0_100_step_10,
                                   metavar="{0|10|20|..|100}",
                                   help='Set what-u-hear recording volume as integer.')
    mixer_audio_group.add_argument('--mixer-recording-what-u-hear-volume-channels', required=False, type=str,
                                   choices=channels, default='Both',
                                   metavar="{Both|Left|Right}",
                                   help='Define channels for --mixer-recording-what-u-hear-volume.')

    #
    # Recording [HID / Audio]
    #
    recording_hid_group = parser.add_argument_group('Recording [HID]',
                                                    description="Control recording features using the G6's USB HID interface.")
    recording_audio_group = parser.add_argument_group('Recording [Audio]',
                                                      description="Control recording features using the G6's USB AudioControl interface. See `--claim-and-release` how to use these features.")

    recording_audio_group.add_argument('--recording-mute', required=False, type=str, choices=enabled_disabled,
                                       metavar="{Enabled|Disabled}",
                                       help='Mute/unmute recording.')
    recording_audio_group.add_argument('--recording-mic-recording-volume', required=False, type=int,
                                       choices=numbers_0_100_step_10,
                                       metavar="{0|10|20|..|100}",
                                       help='Set mic recording volume as integer.')
    recording_audio_group.add_argument('--recording-mic-recording-volume-channels', required=False, type=str,
                                       choices=channels,
                                       default='Both',
                                       metavar="{Both|Left|Right}",
                                       help='Define channels --recording-mic-recording-volume.')
    recording_hid_group.add_argument('--recording-mic-boost-db', required=False, type=int,
                                     choices=numbers_0_30_step_10,
                                     metavar="{0|10|20|30}",
                                     help='Set mic boost in dB as integer.')

    recording_audio_group.add_argument('--recording-mic-monitoring-mute', required=False, type=str,
                                       choices=enabled_disabled,
                                       metavar="{Enabled|Disabled}",
                                       help='Enable/disable mic monitoring.')
    recording_audio_group.add_argument('--recording-mic-monitoring-volume', required=False, type=int,
                                       choices=numbers_0_100_step_10,
                                       metavar="{0|10|20|..|100}",
                                       help='Set mic monitoring volume as integer.')
    recording_audio_group.add_argument('--recording-mic-monitoring-volume-channels', required=False, type=str,
                                       choices=channels,
                                       default='Both',
                                       metavar="{Both|Left|Right}",
                                       help='Define channels for --recording-mic-monitoring-volume.')

    recording_hid_group.add_argument('--recording-voice-clarity', required=False, type=str, choices=enabled_disabled,
                                     metavar="{Enabled|Disabled}",
                                     help='Enable/disable voice clarity.')
    recording_hid_group.add_argument('--recording-voice-clarity-noise-reduction', required=False, type=int,
                                     choices=numbers_0_100_step_20,
                                     metavar="{0|20|40|..|100}",
                                     help='Set noise reduction level as integer.')
    recording_hid_group.add_argument('--recording-voice-clarity-aec', required=False, type=str,
                                     choices=enabled_disabled,
                                     metavar="{Enabled|Disabled}",
                                     help='Enable/disable acoustic echo cancellation (AEC).')
    recording_hid_group.add_argument('--recording-voice-clarity-smart-volume', required=False, type=str,
                                     choices=enabled_disabled,
                                     metavar="{Enabled|Disabled}",
                                     help='Enable/disable smart volume.')
    recording_hid_group.add_argument('--recording-voice-clarity-mic-eq', required=False, type=str,
                                     choices=enabled_disabled,
                                     metavar="{Enabled|Disabled}",
                                     help='Enable/disable mic equalizer.')
    recording_hid_group.add_argument('--recording-voice-clarity-mic-eq-preset', required=False, type=str,
                                     choices=[e.name for e in MicrophoneEqualizerPreset],
                                     metavar=(
                                         "{PRESET_1|PRESET_2|PRESET_3|PRESET_4|PRESET_5|PRESET_6|PRESET_7|PRESET_8|PRESET_9|"
                                         "PRESET_10|PRESET_DM_1}"
                                     ),
                                     help='Set mic equalizer preset by enum name.')

    #
    # Sound Effects (SBX) [HID]
    #
    sbx_hid_group = parser.add_argument_group('SBX [HID]',
                                              description="Control SBX effects using the G6's USB HID interface.")
    sbx_hid_group.add_argument('--sbx-surround', required=False, type=str, choices=enabled_disabled,
                               metavar="{Enabled|Disabled}",
                               help='Enables or disables the Surround sound effect.')
    sbx_hid_group.add_argument('--sbx-surround-value', required=False, type=int, choices=numbers_0_100,
                               metavar="{0..100}",
                               help='Set the value for the Surround sound effect as integer.')

    sbx_hid_group.add_argument('--sbx-crystalizer', required=False, type=str, choices=enabled_disabled,
                               metavar="{Enabled|Disabled}",
                               help='Enables or disables the Crystalizer sound effect.')
    sbx_hid_group.add_argument('--sbx-crystalizer-value', required=False, type=int, choices=numbers_0_100,
                               metavar="{0..100}",
                               help='Set the value for the Crystalizer sound effect as integer.')

    sbx_hid_group.add_argument('--sbx-bass', required=False, type=str, choices=enabled_disabled,
                               metavar="{Enabled|Disabled}",
                               help='Enables or disables the Bass sound effect.')
    sbx_hid_group.add_argument('--sbx-bass-value', required=False, type=int, choices=numbers_0_100,
                               metavar="{0..100}",
                               help='Set the value for the Bass sound effect as integer.')

    sbx_hid_group.add_argument('--sbx-smart-volume', required=False, type=str, choices=enabled_disabled,
                               metavar="{Enabled|Disabled}",
                               help='Enables or disables the Smart-Volume sound effect.')
    sbx_hid_group.add_argument('--sbx-smart-volume-value', required=False, type=int, choices=numbers_0_100,
                               metavar="{0..100}",
                               help='Set the value for the Smart-Volume sound effect as value.')
    sbx_hid_group.add_argument('--sbx-smart-volume-special-value', required=False, type=str, choices=['Night', 'Loud'],
                               metavar="{Night|Loud}",
                               help='Set the value for the Smart-Volume sound effect as string (supersedes --set-smart-volume-value).')

    sbx_hid_group.add_argument('--sbx-dialog-plus', required=False, type=str, choices=enabled_disabled,
                               metavar="{Enabled|Disabled}",
                               help='Enables or disables the Dialog-Plus sound effect.')
    sbx_hid_group.add_argument('--sbx-dialog-plus-value', required=False, type=int, choices=numbers_0_100,
                               metavar="{0..100}",
                               help='Set the value for the Dialog-Plus sound effect as integer.')

    # parse args and verify
    args = parser.parse_args()
    if args.toggle_output is False \
            and args.set_output is None \
            and args.claim_and_release is False \
            and args.reload_audio_services is False \
            and args.playback_mute is None \
            and args.playback_volume is None \
            and args.playback_speakers_to_stereo is False \
            and args.playback_speakers_to_5_1 is False \
            and args.playback_speakers_to_7_1 is False \
            and args.playback_headphones_to_stereo is False \
            and args.playback_headphones_to_5_1 is False \
            and args.playback_headphones_to_7_1 is False \
            and args.playback_direct_mode is None \
            and args.playback_spdif_out_direct_mode is None \
            and args.playback_filter is None \
            and args.decoder_mode is None \
            and args.lighting_disable is False \
            and args.lighting_rgb is None \
            and args.mixer_playback_mute is None \
            and args.mixer_monitoring_line_in_mute is None \
            and args.mixer_monitoring_line_in_volume is None \
            and args.mixer_monitoring_external_mic_mute is None \
            and args.mixer_monitoring_external_mic_volume is None \
            and args.mixer_monitoring_spdif_in_mute is None \
            and args.mixer_monitoring_spdif_in_volume is None \
            and args.mixer_recording_line_in_mute is None \
            and args.mixer_recording_line_in_volume is None \
            and args.mixer_recording_external_mic_mute is None \
            and args.mixer_recording_external_mic_volume is None \
            and args.mixer_recording_spdif_in_mute is None \
            and args.mixer_recording_spdif_in_volume is None \
            and args.mixer_recording_what_u_hear_mute is None \
            and args.mixer_recording_what_u_hear_volume is None \
            and args.recording_mute is None \
            and args.recording_mic_recording_volume is None \
            and args.recording_mic_boost_db is None \
            and args.recording_mic_monitoring_mute is None \
            and args.recording_mic_monitoring_volume is None \
            and args.recording_voice_clarity is None \
            and args.recording_voice_clarity_noise_reduction is None \
            and args.recording_voice_clarity_aec is None \
            and args.recording_voice_clarity_smart_volume is None \
            and args.recording_voice_clarity_mic_eq is None \
            and args.recording_voice_clarity_mic_eq_preset is None \
            and args.sbx_surround is None \
            and args.sbx_surround_value is None \
            and args.sbx_crystalizer is None \
            and args.sbx_crystalizer_value is None \
            and args.sbx_bass is None \
            and args.sbx_bass_value is None \
            and args.sbx_smart_volume is None \
            and args.sbx_smart_volume_value is None \
            and args.sbx_smart_volume_special_value is None \
            and args.sbx_dialog_plus is None \
            and args.sbx_dialog_plus_value is None:
        message = 'No meaningful argument has been specified!'
        print(message)
        parser.print_help()
        raise ValueError(message)
    elif args.toggle_output is True and args.set_output is not None:
        message = 'Only one of the following CLI arguments may be specified: \'--toggle-output', '--set-output\'!'
        print(message)
        parser.print_help()
        raise ValueError(message)

    return args


def read_toggle_state_file(toggle_state_file_path):
    """
    Read the toggle state from the temporary file to determine the state from previous runs.
    :param toggle_state_file_path: The path to the file, where the last toggle state has been remembered in.
    :return: The content of the file. Should be either 'Speakers' or 'Headphones'.
    """
    with open(toggle_state_file_path, 'r') as file:
        return file.read()


def write_toggle_state_file(toggle_state_file_path, toggle_state_value):
    """
    Write the currently used toggle_state to the temporary file for next runs.
    :param toggle_state_file_path: The path to the file for remembering the last set toggle state.
    :param toggle_state_value: The toggle state to write to the file. Should be either 'Speakers' or 'Headphones'.
    """
    with open(toggle_state_file_path, 'w') as file:
        file.write(str(toggle_state_value))


def determine_toggle_state():
    """
    Reads the last used toggle_state value from the temporary file to determine the next value.
    If the temporary file does not exist, 'Speakers' is used by default.
    :return: The just set and now active toggle state value.
    """
    toggle_state_file_path = os.path.join(tempfile.gettempdir(), TOGGLE_STATE_TEMP_FILE_NAME)
    # determine toggle state from a temporary file or use SPEAKERS by default
    if os.path.exists(toggle_state_file_path):
        current_toggle_state = read_toggle_state_file(toggle_state_file_path)
        next_toggle_state = TOGGLE_STATE_SPEAKERS \
            if current_toggle_state == TOGGLE_STATE_HEADPHONES \
            else TOGGLE_STATE_HEADPHONES
        print(
            f'Toggle from '
            f'{current_toggle_state} -> {next_toggle_state}')
    else:
        next_toggle_state = TOGGLE_STATE_SPEAKERS
        print(f'Toggle to {next_toggle_state}')
    # write the next toggle state to a temporary file
    write_toggle_state_file(toggle_state_file_path, next_toggle_state)
    # return the next toggle state to send it to the G6
    return next_toggle_state


def device_toggle_output(api: G6Api):
    """
    Toggles the device's output. Either Speakers -> Headphones or Headphones -> Speakers.
    :param api: The G6Api instance to use for communication with the device.
    """
    # determine the next toggle state
    toggle_state = determine_toggle_state()
    # toggle playback output
    if toggle_state == TOGGLE_STATE_SPEAKERS:
        api.playback_toggle_to_headphones()
    else:
        api.playback_toggle_to_speakers()


def device_set_output(api: G6Api, toggle_state: str):
    """
    Set a specific device output. Either 'Speakers' or 'Headphones'
    :param api: The G6Api instance to use for communication with the device.
    :param toggle_state: The toggle_state value to set the G6's output to. Should be either 'Speakers' or 'Headphones'.
    """
    # toggle playback output to the specified toggle_state
    if toggle_state == TOGGLE_STATE_SPEAKERS:
        api.playback_toggle_to_speakers()
    elif toggle_state == TOGGLE_STATE_HEADPHONES:
        api.playback_toggle_to_headphones()
    else:
        raise ValueError(
            f'The given toggle_state must either be {TOGGLE_STATE_SPEAKERS} or {TOGGLE_STATE_HEADPHONES}, '
            f'but was {toggle_state}!')


def device_set_audio_effects(api: G6Api, args: argparse.Namespace):
    """
    Processes all CLI arguments and calls the required API functions.
    :param api: The G6Api instance to use for communication with the device.
    :param args: The CLI arguments, recently parsed by argparse in parse_cli_args()
    """

    # Double-check if the G6's USB HID interface is available
    if not api.is_hid_interface_available():
        raise RuntimeError('The G6 HID interface should be available at this point!')

    # Try to claim the USB AudioControl interface first, if requested.
    if args.claim_and_release:
        # claim the USB AudioControl interface
        api.claim_audio_interface()

        # double-check if the USB AudioControl interface is available
        if not api.is_audio_interface_available():
            raise RuntimeError(
                'The G6 AudioControl interface should be available at this point! Claiming the interface failed.')

    # Process audio features
    try:

        #
        # Playback
        #
        # toggle or set playback output
        if args.toggle_output:
            device_toggle_output(api=api)
        elif args.set_output is not None:
            device_set_output(api=api, toggle_state=args.set_output)
        # playback mute
        if args.playback_mute is not None:
            # 'Enabled' means mute=True (same semantics as other toggles)
            api.playback_mute(mute=to_bool(args.playback_mute))
        # playback volume
        if args.playback_volume is not None:
            api.playback_volume(
                volume_percent=args.playback_volume,
                channels=_channels_from_cli(args.playback_volume_channels))
        # playback output mode
        if args.playback_speakers_to_stereo:
            api.playback_speakers_to_stereo()
        if args.playback_speakers_to_5_1:
            api.playback_speakers_to_5_1()
        if args.playback_speakers_to_7_1:
            api.playback_speakers_to_7_1()
        if args.playback_headphones_to_stereo:
            api.playback_headphones_to_stereo()
        if args.playback_headphones_to_5_1:
            api.playback_headphones_to_5_1()
        if args.playback_headphones_to_7_1:
            api.playback_headphones_to_7_1()
        # playback direct mode
        if args.playback_direct_mode is not None:
            api.playback_enable_direct_mode(enable=to_bool(args.playback_direct_mode))
        # playback spdif-out direct mode
        if args.playback_spdif_out_direct_mode is not None:
            api.playback_enable_spdif_out_direct_mode(enable=to_bool(args.playback_spdif_out_direct_mode))
        # playback filter
        if args.playback_filter is not None:
            api.playback_filter(playback_filter_enum=PlaybackFilter[args.playback_filter])
        # playback decoder mode
        if args.decoder_mode is not None:
            api.decoder_mode(decoder_mode_enum=_decoder_mode_from_cli(args.decoder_mode))

        #
        # Lighting
        #
        if args.lighting_disable:
            api.lighting_disable()
        if args.lighting_rgb is not None:
            red, green, blue = args.lighting_rgb
            api.lighting_enable_set_rgb(red=red, green=green, blue=blue)

        #
        # Mixer
        #
        # playback mute
        if args.mixer_playback_mute is not None:
            api.mixer_playback_mute(mute=to_bool(args.mixer_playback_mute))
        # monitoring > line-in
        if args.mixer_monitoring_line_in_mute is not None:
            api.mixer_monitoring_line_in_mute(mute=to_bool(args.mixer_monitoring_line_in_mute))
        if args.mixer_monitoring_line_in_volume is not None:
            api.mixer_monitoring_line_in_volume(
                volume_percent=args.mixer_monitoring_line_in_volume,
                channels=_channels_from_cli(args.mixer_monitoring_line_in_volume_channels))
        # monitoring > external-mic
        if args.mixer_monitoring_external_mic_mute is not None:
            api.mixer_monitoring_external_mic_mute(mute=to_bool(args.mixer_monitoring_external_mic_mute))
        if args.mixer_monitoring_external_mic_volume is not None:
            api.mixer_monitoring_external_mic_volume(
                volume_percent=args.mixer_monitoring_external_mic_volume,
                channels=_channels_from_cli(args.mixer_monitoring_external_mic_volume_channels))
        # monitoring > spdif-in
        if args.mixer_monitoring_spdif_in_mute is not None:
            api.mixer_monitoring_spdif_in_mute(mute=to_bool(args.mixer_monitoring_spdif_in_mute))
        if args.mixer_monitoring_spdif_in_volume is not None:
            api.mixer_monitoring_spdif_in_volume(
                volume_percent=args.mixer_monitoring_spdif_in_volume,
                channels=_channels_from_cli(args.mixer_monitoring_spdif_in_volume_channels))
        # recording > line-in
        if args.mixer_recording_line_in_mute is not None:
            api.mixer_recording_line_in_mute(mute=to_bool(args.mixer_recording_line_in_mute))
        if args.mixer_recording_line_in_volume is not None:
            api.mixer_recording_line_in_volume(
                volume_percent=args.mixer_recording_line_in_volume,
                channels=_channels_from_cli(args.mixer_recording_line_in_volume_channels))
        # recording > external-mic
        if args.mixer_recording_external_mic_mute is not None:
            api.mixer_recording_external_mic_mute(mute=to_bool(args.mixer_recording_external_mic_mute))
        if args.mixer_recording_external_mic_volume is not None:
            api.mixer_recording_external_mic_volume(
                volume_percent=args.mixer_recording_external_mic_volume,
                channels=_channels_from_cli(args.mixer_recording_external_mic_volume_channels))
        # recording > spdif-in
        if args.mixer_recording_spdif_in_mute is not None:
            api.mixer_recording_spdif_in_mute(mute=to_bool(args.mixer_recording_spdif_in_mute))
        if args.mixer_recording_spdif_in_volume is not None:
            api.mixer_recording_spdif_in_volume(
                volume_percent=args.mixer_recording_spdif_in_volume,
                channels=_channels_from_cli(args.mixer_recording_spdif_in_volume_channels))
        # recording > what-u-hear
        if args.mixer_recording_what_u_hear_mute is not None:
            api.mixer_recording_what_u_hear_mute(mute=to_bool(args.mixer_recording_what_u_hear_mute))
        if args.mixer_recording_what_u_hear_volume is not None:
            api.mixer_recording_what_u_hear_volume(
                volume_percent=args.mixer_recording_what_u_hear_volume,
                channels=_channels_from_cli(args.mixer_recording_what_u_hear_volume_channels))

        #
        # Recording
        #
        # mic recording
        if args.recording_mute is not None:
            api.recording_mute(mute=to_bool(args.recording_mute))

        if args.recording_mic_recording_volume is not None:
            api.recording_mic_recording_volume(
                volume_percent=args.recording_mic_recording_volume,
                channels=_channels_from_cli(args.recording_mic_recording_volume_channels))
        # mic boost
        if args.recording_mic_boost_db is not None:
            api.recording_mic_boost(decibel=args.recording_mic_boost_db)
        # mic monitoring
        if args.recording_mic_monitoring_mute is not None:
            api.recording_mic_monitoring_mute(mute=to_bool(args.recording_mic_monitoring_mute))
        if args.recording_mic_monitoring_volume is not None:
            api.recording_mic_monitoring_volume(
                volume_percent=args.recording_mic_monitoring_volume,
                channels=_channels_from_cli(args.recording_mic_monitoring_volume_channels))
        # voice clarity
        if args.recording_voice_clarity is not None:
            api.recording_voice_clarity_enabled(enable=to_bool(args.recording_voice_clarity))
        if args.recording_voice_clarity_noise_reduction is not None:
            api.recording_voice_clarity_noise_reduction_level(
                level_percent=args.recording_voice_clarity_noise_reduction)
        if args.recording_voice_clarity_aec is not None:
            api.recording_voice_clarity_acoustic_echo_cancellation_enabled(
                enable=to_bool(args.recording_voice_clarity_aec))
        if args.recording_voice_clarity_smart_volume is not None:
            api.recording_voice_clarity_smart_volume_enabled(
                enable=to_bool(args.recording_voice_clarity_smart_volume))
        if args.recording_voice_clarity_mic_eq is not None:
            api.recording_voice_clarity_mic_equalizer_enabled(enable=to_bool(args.recording_voice_clarity_mic_eq))
        if args.recording_voice_clarity_mic_eq_preset is not None:
            api.recording_voice_clarity_mic_equalizer_preset(
                preset=MicrophoneEqualizerPreset[args.recording_voice_clarity_mic_eq_preset])

        #
        # SBX Effects
        #
        # surround
        if args.sbx_surround is not None:
            api.sbx_toggle(AudioFeature.SURROUND_TOGGLE, to_bool(args.sbx_surround))
        if args.sbx_surround_value is not None:
            api.sbx_slider(AudioFeature.SURROUND_SLIDER, args.sbx_surround_value)
        # crystalizer
        if args.sbx_crystalizer is not None:
            api.sbx_toggle(AudioFeature.CRYSTALIZER_TOGGLE, to_bool(args.sbx_crystalizer))
        if args.sbx_crystalizer_value is not None:
            api.sbx_slider(AudioFeature.CRYSTALIZER_SLIDER, args.sbx_crystalizer_value)
        # bass
        if args.sbx_bass is not None:
            api.sbx_toggle(AudioFeature.BASS_TOGGLE, to_bool(args.sbx_bass))
        if args.sbx_bass_value is not None:
            api.sbx_slider(AudioFeature.BASS_SLIDER, args.sbx_bass_value)
        # smart-volume
        if args.sbx_smart_volume is not None:
            api.sbx_toggle(AudioFeature.SMART_VOLUME_TOGGLE, to_bool(args.sbx_smart_volume))
        if args.sbx_smart_volume_value is not None:
            api.sbx_slider(AudioFeature.SMART_VOLUME_SLIDER, args.sbx_smart_volume_value)
        if args.sbx_smart_volume_special_value is not None:
            if args.sbx_smart_volume_special_value == 'Night':
                api.sbx_smart_volume_special(SmartVolumeSpecialHex.SMART_VOLUME_NIGHT)
            elif args.sbx_smart_volume_special_value == 'Loud':
                api.sbx_smart_volume_special(SmartVolumeSpecialHex.SMART_VOLUME_LOUD)
            else:
                raise ValueError(
                    f"Expected one of the following values for --sbx-smart-volume-special-value: "
                    f"['Night', 'Loud'], but was '{args.sbx_smart_volume_special_value}'!"
                )
        # dialog-plus
        if args.sbx_dialog_plus is not None:
            api.sbx_toggle(AudioFeature.DIALOG_PLUS_TOGGLE, to_bool(args.sbx_dialog_plus))
        if args.sbx_dialog_plus_value is not None:
            api.sbx_slider(AudioFeature.DIALOG_PLUS_SLIDER, args.sbx_dialog_plus_value)
    finally:
        # Release the USB AudioControl interface if it has been claimed.
        if args.claim_and_release and api.is_audio_interface_available():
            api.release_audio_interface()

        # Reload ALSA and PipeWire, if requested.
        if args.reload_audio_services:
            use_sudo = not args.reload_audio_services_no_sudo
            api.reload_alsa_and_pipewire(sudo=use_sudo)


def main():
    # parse CLI arguments
    args = parse_cli_args()

    # look up the G6 device
    api = G6Api(dry_run=args.dry_run, debug=args.debug, persist_model=False)

    # process arguments and call the api
    device_set_audio_effects(api=api, args=args)
