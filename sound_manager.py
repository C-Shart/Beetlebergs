from arcade import Sound, load_sound

DEFAULT_VOLUME = 0.7
SFXPATH_BEETLE_HIT = "Assets/Sound/SFX/impact2_noisecollector.wav"
SFXPATH_BEETLE_DEAD = "Assets/Sound/SFX/beetle_dead_mixkit.wav"
SFX_PATH_PEASHOOTER = "Assets\Sound\SFX\pew_xtrgamr.wav"

class SoundManager:
    def __init__(self):
        self.audio_player = Sound()
        self.sfx_beetle_dead = load_sound(SFXPATH_BEETLE_DEAD)
        self.sfx_beetle_hit = load_sound(SFXPATH_BEETLE_HIT)
        self.peashooter_pew = load_sound(SFX_PATH_PEASHOOTER)

    def setup(self):
        self.set_volume(DEFAULT_VOLUME)

    def set_volume(self, volume=None):
        if not volume:
            self.audio_player.set_volume = 0.7
        else:
            self.audio_player.set_volume = volume

    def play_sound(self, sound):
        if not sound:
            pass
        else:
            self.audio_player.play(sound)

    def stop_sound(self, sound):
        if not sound:
            pass
        else:
            self.audio_player.stop(sound)

    def play_music(self, music):
        if not music:
            pass
        else:
            self.audio_player.play(music)

    def change_music(self, current_track, new_track):
        # TODO: Methods of changing the music. Hard stop, fade, other?
        if not new_track or not current_track:
            pass
        else:
            self.fade_music(current_track, new_track)

    def fade_music(self, current_track, new_track = None):
        # TODO: Figure out fade method. Maybe set target volume, then decrease by a rate per on_update?
        if not new_track:
            # TODO: Fade music one direction
            pass
        elif current_track and new_track:
            # TODO: Cross-fade music
            pass
        else:
            pass

    def stop_music(self, music):
        if not music:
            pass
        else:
            self.audio_player.stop(music)