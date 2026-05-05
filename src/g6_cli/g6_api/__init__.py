import os
import shutil
import subprocess
import sys

from g6_cli.g6_core import (
    detect_device, G6_VENDOR_ID, G6_PRODUCT_ID
)
from g6_cli.g6_model import G6Model
from g6_cli.g6_model.playback import AudioMode
from g6_cli.g6_model.sbx import Profile
from g6_cli.g6_spec import AudioFeature, PlaybackFilter, SmartVolumeSpecialHex, Channel, BOTH_CHANNELS
from g6_cli.g6_spec.decoder import DecoderMode
from g6_cli.g6_spec.decoder import decoder_mode as decoder_mode_spec
from g6_cli.g6_spec.lighting import (
    lighting_disable as lighting_disable_spec,
    lighting_enable_set_rgb as lighting_enable_set_rgb_spec,
    lighting_volume_ring as lighting_volume_ring_spec,
)
from g6_cli.g6_spec.mixer import (
    monitoring_external_mic_mute as monitoring_external_mic_mute_spec,
    monitoring_external_mic_volume as monitoring_external_mic_volume_spec,
    monitoring_line_in_mute as monitoring_line_in_mute_spec,
    monitoring_line_in_volume as monitoring_line_in_volume_spec,
    monitoring_spdif_in_mute as monitoring_spdif_in_mute_spec,
    monitoring_spdif_in_volume as monitoring_spdif_in_volume_spec,
    playback_mute as mixer_playback_mute_spec,
    recording_external_mic_mute as recording_external_mic_mute_spec,
    recording_external_mic_volume as recording_external_mic_volume_spec,
    recording_line_in_mute as recording_line_in_mute_spec,
    recording_line_in_volume as recording_line_in_volume_spec,
    recording_spdif_in_mute as recording_spdif_in_mute_spec,
    recording_spdif_in_volume as recording_spdif_in_volume_spec,
    recording_what_u_hear_mute as recording_what_u_hear_mute_spec,
    recording_what_u_hear_volume as recording_what_u_hear_volume_spec,
)
from g6_cli.g6_spec.playback import (
    enable_direct_mode as enable_direct_mode_spec,
    enable_spdif_out_direct_mode as enable_spdif_out_direct_mode_spec,
    headphones_to_5_1 as headphones_to_5_1_spec,
    headphones_to_7_1 as headphones_to_7_1_spec,
    headphones_to_stereo as headphones_to_stereo_spec,
    playback_filter as playback_filter_spec,
    playback_mute as playback_mute_spec,
    playback_volume as playback_volume_spec,
    speakers_to_5_1 as speakers_to_5_1_spec,
    speakers_to_7_1 as speakers_to_7_1_spec,
    speakers_to_stereo as speakers_to_stereo_spec,
    toggle_to_headphones as toggle_to_headphones_spec,
    toggle_to_speakers as toggle_to_speakers_spec,
)
from g6_cli.g6_spec.recording import MicrophoneEqualizerPreset
from g6_cli.g6_spec.recording import (
    voice_clarity_acoustic_echo_cancellation_enabled as voice_clarity_acoustic_echo_cancellation_enabled_spec,
    mic_boost as mic_boost_spec,
    voice_clarity_mic_equalizer_enabled as voice_clarity_mic_equalizer_enabled_spec,
    voice_clarity_mic_equalizer_preset as voice_clarity_mic_equalizer_preset_spec,
    mic_monitoring_mute as mic_monitoring_mute_spec,
    mic_monitoring_volume as mic_monitoring_volume_spec,
    mic_recording_volume as mic_recording_volume_spec,
    recording_mute as recording_mute_spec,
    voice_clarity_smart_volume_enabled as voice_clarity_smart_volume_enabled_spec,
    voice_clarity_noise_reduction_enabled as voice_clarity_noise_reduction_enabled_spec,
    voice_clarity_noise_reduction_level as voice_clarity_noise_reduction_level_spec,
)
from g6_cli.g6_spec.sbx import (
    sbx_slider as sbx_slider_spec,
    sbx_smart_volume_special as sbx_smart_volume_special_spec,
    sbx_toggle as sbx_toggle_spec,
)

DEFAULT_MODEL_PATH = "~/.soundblaster-x-g6/g6.json"


class G6Api:
    def lighting_volume_ring(self, enable: bool) -> None:
        hid_data_list = lighting_volume_ring_spec(enable=enable)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)

    def lighting_volume_ring_available(self) -> bool:
        return self.__device.is_hid_interface_available()
    def __init__(self, dry_run: bool, debug: bool, persist_model: bool):
        """
        Instantiates the API for communicating with the G6 device.
        :param dry_run: True, if the communication should only be simulated.
        :param debug: True, if the actual hex codes of the device communication should be printed to console.
        :param persist_model: True, if the state of the G6 should be persisted to file ~/.soundblaster-x-g6/g6.json
        """
        self.__dry_run = dry_run
        self.__persist_model = persist_model
        self.__device = detect_device(dry_run=dry_run, debug=debug)
        self.__model: G6Model = G6Model()
        if self.__persist_model:
            self.load_model()

    def get_model(self) -> G6Model:
        """
        Get the complete G6Model instance holding all current device state values.
        """
        return self.__model

    # ── Model Persistence ──

    @staticmethod
    def __get_default_model_path() -> str:
        """Return the default path for model JSON persistence."""
        path = os.path.expanduser(DEFAULT_MODEL_PATH)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    def save_model(self, file_path: str | None = None) -> None:
        """
        Serialize the complete model state to a JSON file
        (default: ~/.soundblaster-x-g6/g6.json).
        """
        if file_path is None:
            file_path = self.__get_default_model_path()
        self.__model.to_json(file_path)

    def load_model(self, file_path: str | None = None) -> None:
        """
        Deserialize the model state from a JSON file
        (default: ~/.soundblaster-x-g6/g6.json).
        If the file does not exist, the current model state is kept.
        """
        if file_path is None:
            file_path = self.__get_default_model_path()
        if not os.path.exists(file_path):
            return
        self.__model = G6Model.from_json(file_path)

    # ── Claim and Release Audio Interface ──

    def claim_audio_interface(self) -> None:
        self.__device.claim_audio_interface()

    def release_audio_interface(self) -> None:
        self.__device.release_audio_interface()

    def reload_audio(self) -> None:
        """
        Reset the G6 usb device and restart user PipeWire services.
        """

        def usb_reset():
            completed_process = subprocess.run(["/usr/bin/usbreset", f"{G6_VENDOR_ID:04x}:{G6_PRODUCT_ID:04x}"],
                                               capture_output=True,
                                               encoding='utf-8',
                                               check=True)
            sys.stdout.write(completed_process.stdout)
            sys.stderr.write(completed_process.stderr)

        def reload_pipewire():
            # noinspection PyDeprecation
            systemctl = shutil.which("systemctl")
            if not systemctl:
                raise RuntimeError("systemctl not found.")

            user_env = dict(os.environ)
            user_env.setdefault("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")

            completed_process = subprocess.run(
                [systemctl, "--user", "restart", "pipewire", "pipewire-pulse", "wireplumber"],
                capture_output=True,
                encoding='utf-8',
                check=True,
                env=user_env,
            )
            sys.stdout.write(completed_process.stdout)
            sys.stderr.write(completed_process.stderr)

        # check for dryrun mode
        if self.__dry_run:
            print("This is a dry run. ALSA and PipeWire will not be reloaded.")
            return

        # ── Reset USB device ──
        usb_reset()

        # ── Restart PipeWire (user services) ──
        reload_pipewire()

    def is_hid_interface_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def is_audio_interface_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    # ── Playback ──

    def playback_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = playback_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(
            audio_data_list=audio_data_list,
        )
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_mute(mute)
            self.save_model()

    def playback_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def playback_toggle_to_speakers(self) -> None:
        # send data to G6
        hid_data_list = toggle_to_speakers_spec()
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_is_speakers(True)
            self.save_model()

    def playback_toggle_to_speakers_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def playback_toggle_to_headphones(self) -> None:
        # send data to G6
        hid_data_list = toggle_to_headphones_spec()
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_is_speakers(False)
            self.save_model()

    def playback_toggle_to_headphones_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def playback_speakers_to_stereo(self) -> None:
        # send data to G6
        audio_data_list = speakers_to_stereo_spec()
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_speakers_audio_mode(audio_mode=AudioMode.AM_STEREO)
            self.save_model()

    def playback_speakers_to_stereo_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def playback_speakers_to_5_1(self) -> None:
        # send data to G6
        audio_data_list = speakers_to_5_1_spec()
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_speakers_audio_mode(audio_mode=AudioMode.AM_5_1)
            self.save_model()

    def playback_speakers_to_5_1_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def playback_speakers_to_7_1(self) -> None:
        # send data to G6
        audio_data_list = speakers_to_7_1_spec()
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_speakers_audio_mode(audio_mode=AudioMode.AM_7_1)
            self.save_model()

    def playback_speakers_to_7_1_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def playback_headphones_to_stereo(self) -> None:
        # send data to G6
        audio_data_list = headphones_to_stereo_spec()
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_headphones_audio_mode(audio_mode=AudioMode.AM_STEREO)
            self.save_model()

    def playback_headphones_to_stereo_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def playback_headphones_to_5_1(self) -> None:
        # send data to G6
        audio_data_list = headphones_to_5_1_spec()
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_headphones_audio_mode(audio_mode=AudioMode.AM_5_1)
            self.save_model()

    def playback_headphones_to_5_1_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def playback_headphones_to_7_1(self) -> None:
        # send data to G6
        audio_data_list = headphones_to_7_1_spec()
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_headphones_audio_mode(audio_mode=AudioMode.AM_7_1)
            self.save_model()

    def playback_headphones_to_7_1_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def playback_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = playback_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_volume(volume_percent, channels)
            self.save_model()

    def playback_volume_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def playback_enable_direct_mode(self, enable: bool) -> None:
        # send data to G6
        hid_data_list = enable_direct_mode_spec(enable=enable)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_direct_mode_enabled(enable)
            self.save_model()

    def playback_enable_direct_mode_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def playback_enable_spdif_out_direct_mode(self, enable: bool) -> None:
        # send data to G6
        hid_data_list = enable_spdif_out_direct_mode_spec(enable=enable)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_spdif_out_direct_mode_enabled(enable)
            self.save_model()

    def playback_enable_spdif_out_direct_mode_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def playback_filter(self, playback_filter_enum: PlaybackFilter) -> None:
        # send data to G6
        hid_data_list = playback_filter_spec(playback_filter_enum=playback_filter_enum)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_playback().set_filter(playback_filter_enum)
            self.save_model()

    def playback_filter_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    # ── Decoder ──

    def decoder_mode(self, decoder_mode_enum: DecoderMode) -> None:
        # send data to G6
        hid_data_list = decoder_mode_spec(decoder_mode_enum=decoder_mode_enum)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_decoder().set_mode(decoder_mode_enum)
            self.save_model()

    def decoder_mode_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    # ── Lighting ──

    def lighting_disable(self) -> None:
        # send data to G6
        hid_data_list = lighting_disable_spec()
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_lighting().set_enabled(False)
            self.save_model()

    def lighting_disable_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def lighting_enable_set_rgb(self, red: int, green: int, blue: int) -> None:
        # send data to G6
        hid_data_list = lighting_enable_set_rgb_spec(red=red, green=green, blue=blue)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_lighting().set_rgb(red, green, blue)
            self.save_model()

    def lighting_enable_set_rgb_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    # ── Mixer ──

    def mixer_playback_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = mixer_playback_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_playback_mute(mute)
            self.save_model()

    def mixer_playback_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_monitoring_line_in_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = monitoring_line_in_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_monitoring_line_in_mute(mute)
            self.save_model()

    def mixer_monitoring_line_in_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_monitoring_line_in_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = monitoring_line_in_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_monitoring_line_in_volume(volume_percent, channels)
            self.save_model()

    def mixer_monitoring_line_in_volume_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_monitoring_external_mic_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = monitoring_external_mic_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_monitoring_external_mic_mute(mute)
            self.save_model()

    def mixer_monitoring_external_mic_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_monitoring_external_mic_volume(self, volume_percent: int,
                                             channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = monitoring_external_mic_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_monitoring_external_mic_volume(volume_percent, channels)
            self.save_model()

    def mixer_monitoring_external_mic_volume_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_monitoring_spdif_in_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = monitoring_spdif_in_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_monitoring_spdif_in_mute(mute)
            self.save_model()

    def mixer_monitoring_spdif_in_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_monitoring_spdif_in_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = monitoring_spdif_in_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_monitoring_spdif_in_volume(volume_percent, channels)
            self.save_model()

    def mixer_monitoring_spdif_in_volume_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_recording_line_in_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = recording_line_in_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_recording_line_in_mute(mute)
            self.save_model()

    def mixer_recording_line_in_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_recording_line_in_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = recording_line_in_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_recording_line_in_volume(volume_percent, channels)
            self.save_model()

    def mixer_recording_line_in_volume_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_recording_external_mic_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = recording_external_mic_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_recording_external_mic_mute(mute)
            self.save_model()

    def mixer_recording_external_mic_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_recording_external_mic_volume(self, volume_percent: int,
                                            channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = recording_external_mic_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_recording_external_mic_volume(volume_percent, channels)
            self.save_model()

    def mixer_recording_external_mic_volume_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_recording_spdif_in_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = recording_spdif_in_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_recording_spdif_in_mute(mute)
            self.save_model()

    def mixer_recording_spdif_in_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_recording_spdif_in_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = recording_spdif_in_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_recording_spdif_in_volume(volume_percent, channels)
            self.save_model()

    def mixer_recording_spdif_in_volume_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_recording_what_u_hear_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = recording_what_u_hear_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_recording_what_u_hear_mute(mute)
            self.save_model()

    def mixer_recording_what_u_hear_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def mixer_recording_what_u_hear_volume(self, volume_percent: int,
                                           channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = recording_what_u_hear_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_mixer().set_recording_what_u_hear_volume(volume_percent, channels)
            self.save_model()

    def mixer_recording_what_u_hear_volume_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    # ── Recording ──

    def recording_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = recording_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_mute(mute)
            self.save_model()

    def recording_mute_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def recording_mic_recording_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = mic_recording_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_mic_recording_volume(volume_percent, channels)
            self.save_model()

    def recording_mic_recording_volume_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def recording_mic_boost(self, decibel: int) -> None:
        # send data to G6
        hid_data_list = mic_boost_spec(decibel=decibel)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_mic_boost(decibel)
            self.save_model()

    def recording_mic_boost_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def recording_mic_monitoring_mute(self, mute: bool) -> None:
        # send data to G6
        audio_data_list = mic_monitoring_mute_spec(mute=mute)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_mic_monitoring_mute(mute)
            self.save_model()

    def recording_mic_monitoring_volume(self, volume_percent: int, channels: set[Channel] = BOTH_CHANNELS) -> None:
        # send data to G6
        audio_data_list = mic_monitoring_volume_spec(volume_percent=volume_percent, channels=channels)
        self.__device.send_audio_data_to_device(audio_data_list=audio_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_mic_monitoring_volume(volume_percent, channels)
            self.save_model()

    def recording_mic_monitoring_available(self) -> bool:
        return self.__device.is_audio_interface_available()

    def recording_voice_clarity_noise_reduction_enabled(self, enable: bool) -> None:
        # send data to G6
        hid_data_list = voice_clarity_noise_reduction_enabled_spec(enable=enable)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_voice_clarity_noise_reduction_enabled(enable)
            self.save_model()

    def recording_voice_clarity_noise_reduction_enabled_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def recording_voice_clarity_noise_reduction_level(self, level_percent: int) -> None:
        # send data to G6
        hid_data_list = voice_clarity_noise_reduction_level_spec(level_percent=level_percent)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_voice_clarity_noise_reduction_level(level_percent)
            self.save_model()

    def recording_voice_clarity_noise_reduction_level_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def recording_voice_clarity_acoustic_echo_cancellation_enabled(self, enable: bool) -> None:
        # send data to G6
        hid_data_list = voice_clarity_acoustic_echo_cancellation_enabled_spec(enable=enable)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_voice_clarity_acoustic_echo_cancellation_enabled(enable)
            self.save_model()

    def recording_voice_clarity_acoustic_echo_cancellation_enabled_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def recording_voice_clarity_smart_volume_enabled(self, enable: bool) -> None:
        # send data to G6
        hid_data_list = voice_clarity_smart_volume_enabled_spec(enable=enable)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_voice_clarity_smart_volume_enabled(enable)
            self.save_model()

    def recording_voice_clarity_smart_volume_enabled_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def recording_voice_clarity_mic_equalizer_enabled(self, enable: bool) -> None:
        # send data to G6
        hid_data_list = voice_clarity_mic_equalizer_enabled_spec(enable=enable)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_voice_clarity_mic_equalizer_enabled(enable)
            self.save_model()

    def recording_voice_clarity_mic_equalizer_enabled_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def recording_voice_clarity_mic_equalizer_preset(self, preset: MicrophoneEqualizerPreset) -> None:
        # send data to G6
        hid_data_list = voice_clarity_mic_equalizer_preset_spec(preset=preset)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)
        # update model
        if self.__persist_model:
            self.__model.get_recording().set_voice_clarity_mic_equalizer_preset(preset)
            self.save_model()

    def recording_voice_clarity_mic_equalizer_preset_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    # ── SBX ──

    def sbx_profile_switch(self, profile_name: Profile.Name):
        # send data to G6
        sbx = self.__model.get_sbx(profile_name=profile_name)
        ## surround
        self.sbx_toggle(profile_name=profile_name, audio_feature=AudioFeature.SURROUND_TOGGLE,
                        activate=sbx.get_surround_toggle())
        self.sbx_slider(profile_name=profile_name, audio_feature=AudioFeature.SURROUND_SLIDER,
                        value=sbx.get_surround_slider())
        ## crystalizer
        self.sbx_toggle(profile_name=profile_name, audio_feature=AudioFeature.CRYSTALIZER_TOGGLE,
                        activate=sbx.get_crystalizer_toggle())
        self.sbx_slider(profile_name=profile_name, audio_feature=AudioFeature.CRYSTALIZER_SLIDER,
                        value=sbx.get_crystalizer_slider())
        ## bass
        self.sbx_toggle(profile_name=profile_name, audio_feature=AudioFeature.BASS_TOGGLE,
                        activate=sbx.get_bass_toggle())
        self.sbx_slider(profile_name=profile_name, audio_feature=AudioFeature.BASS_SLIDER, value=sbx.get_bass_slider())
        ## smart volume
        self.sbx_toggle(profile_name=profile_name, audio_feature=AudioFeature.SMART_VOLUME_TOGGLE,
                        activate=sbx.get_smart_volume_toggle())
        smart_volume_special = sbx.get_smart_volume_special()
        if smart_volume_special is None:
            self.sbx_slider(profile_name=profile_name, audio_feature=AudioFeature.SMART_VOLUME_SLIDER,
                            value=sbx.get_smart_volume_slider())
        else:
            self.sbx_smart_volume_special(profile_name=profile_name, smart_volume_special_hex=smart_volume_special)
        ## dialog plus
        self.sbx_toggle(profile_name=profile_name, audio_feature=AudioFeature.DIALOG_PLUS_TOGGLE,
                        activate=sbx.get_dialog_plus_toggle())
        self.sbx_slider(profile_name=profile_name, audio_feature=AudioFeature.DIALOG_PLUS_SLIDER,
                        value=sbx.get_dialog_plus_slider())

        # update model
        if self.__persist_model:
            self.__model.set_sbx_profile_selection(profile_name=profile_name)
            self.save_model()

    def sbx_profile_selection(self) -> Profile.Name | None:
        return self.__model.get_sbx_profile_selection()

    def sbx_toggle(self, profile_name: Profile.Name, audio_feature: AudioFeature, activate: bool) -> None:
        # send data to G6
        hid_data_list = sbx_toggle_spec(audio_feature=audio_feature, activate=activate)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)

        # update model
        if self.__persist_model:
            sbx = self.__model.get_sbx(profile_name=profile_name)
            match audio_feature:
                case AudioFeature.SURROUND_TOGGLE:
                    sbx.set_surround_toggle(activate)
                case AudioFeature.CRYSTALIZER_TOGGLE:
                    sbx.set_crystalizer_toggle(activate)
                case AudioFeature.BASS_TOGGLE:
                    sbx.set_bass_toggle(activate)
                case AudioFeature.SMART_VOLUME_TOGGLE:
                    sbx.set_smart_volume_toggle(activate)
                case AudioFeature.DIALOG_PLUS_TOGGLE:
                    sbx.set_dialog_plus_toggle(activate)
            self.save_model()

    def sbx_toggle_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def sbx_slider(self, profile_name: Profile.Name, audio_feature: AudioFeature, value: int) -> None:
        # send data to G6
        hid_data_list = sbx_slider_spec(audio_feature=audio_feature, value=value)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)

        # update model
        if self.__persist_model:
            sbx = self.__model.get_sbx(profile_name=profile_name)
            match audio_feature:
                case AudioFeature.SURROUND_SLIDER:
                    sbx.set_surround_slider(value)
                case AudioFeature.CRYSTALIZER_SLIDER:
                    sbx.set_crystalizer_slider(value)
                case AudioFeature.BASS_SLIDER:
                    sbx.set_bass_slider(value)
                case AudioFeature.SMART_VOLUME_SLIDER:
                    sbx.set_smart_volume_slider(value)
                case AudioFeature.DIALOG_PLUS_SLIDER:
                    sbx.set_dialog_plus_slider(value)
            self.save_model()

    def sbx_slider_available(self) -> bool:
        return self.__device.is_hid_interface_available()

    def sbx_smart_volume_special(self, profile_name: Profile.Name,
                                 smart_volume_special_hex: SmartVolumeSpecialHex) -> None:
        # send data to G6
        hid_data_list = sbx_smart_volume_special_spec(smart_volume_special_hex=smart_volume_special_hex)
        self.__device.send_hid_data_to_device(hid_data_list=hid_data_list)

        # update model
        if self.__persist_model:
            self.__model.get_sbx(profile_name=profile_name).set_smart_volume_special(smart_volume_special_hex)
            self.save_model()

    def sbx_smart_volume_special_available(self) -> bool:
        return self.__device.is_hid_interface_available()
