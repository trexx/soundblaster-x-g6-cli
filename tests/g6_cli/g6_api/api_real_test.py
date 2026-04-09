from __future__ import annotations

import pytest

import g6_cli.g6_api as g6_api


@pytest.fixture(scope="session")
def api() -> g6_api.G6Api:
    return g6_api.G6Api(dry_run=False, debug=True, persist_model=False)


@pytest.fixture(scope="session", autouse=True)
def around_session(api: g6_api.G6Api):
    # setup: claim interface
    api.claim_audio_interface()

    # run tests
    yield

    # teardown: release interface and reload ALSA
    api.release_audio_interface()
    api.reload_audio()


@pytest.mark.skip(reason="Only run manually!")
def test_playback_volume_0(api: g6_api.G6Api):
    """
    Test that playback volume can be set to 0.
    """
    api.playback_volume(0)


@pytest.mark.skip(reason="Only run manually!")
def test_playback_volume_50(api: g6_api.G6Api):
    """
    Test that playback volume can be set to 50.
    """
    api.playback_volume(10)


@pytest.mark.skip(reason="Only run manually!")
def test_playback_volume_100(api: g6_api.G6Api):
    """
    Test that playback volume can be set to 100.
    """
    api.playback_volume(100)


@pytest.mark.skip(reason="Only run manually!")
def test_toggle_to_speakers(api: g6_api.G6Api):
    """
    Test that playback volume can be set to 100.
    """
    api.playback_toggle_to_speakers()


@pytest.mark.skip(reason="Only run manually!")
def test_toggle_to_headphones(api: g6_api.G6Api):
    """
    Test that playback volume can be set to 100.
    """
    api.playback_toggle_to_headphones()


@pytest.mark.skip(reason="Only run manually!")
def test_rgb_red(api: g6_api.G6Api):
    """
    Test that playback volume can be set to 100.
    """
    api.lighting_enable_set_rgb(255, 0, 0)


@pytest.mark.skip(reason="Only run manually!")
def test_rgb_green(api: g6_api.G6Api):
    """
    Test that playback volume can be set to 100.
    """
    api.lighting_enable_set_rgb(0, 255, 0)


@pytest.mark.skip(reason="Only run manually!")
def test_rgb_blue(api: g6_api.G6Api):
    """
    Test that playback volume can be set to 100.
    """
    api.lighting_enable_set_rgb(0, 0, 255)
