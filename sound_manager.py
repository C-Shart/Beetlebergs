from arcade import Sound, load_sound

DEFAULT_VOLUME = 0.7
SFX_BEETLE_HIT = "Assets/Sound/SFX/impact2_noisecollector.wav"
SFX_BEETLE_DEAD = "Assets/Sound/SFX/beetle_dead_mixkit.wav"
SFX_PEASHOOTER = "Assets/Sound/SFX/pew_xtrgamr.wav"

MUSIC_BANJOS_PLACEHOLDER = "Assets/Sound/Music/banjo_loop.wav"

BEETLE_HIT = "BeetleHit"
BEETLE_DEAD = "BeetleDead"
PEASHOOTER_PEW = "PeashooterPew"

class SoundManager:
    # instance = __class__() # This creates the sound manager as a singleton instance
    # https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/#

    def __init__(self):
        self.audio_player = Sound()
        self.sounds = {
            BEETLE_HIT: load_sound(SFX_BEETLE_DEAD), 
            BEETLE_DEAD: load_sound(SFX_BEETLE_HIT), 
            PEASHOOTER_PEW: load_sound(SFX_PEASHOOTER)
        }
        self.audio_player.set_volume = DEFAULT_VOLUME

    def set_volume(self, volume=None):
        if not volume:
            self.audio_player.set_volume = DEFAULT_VOLUME
        else:
            self.audio_player.set_volume = volume

    def play_sound(self, sound_key):
        if not sound_key:
            raise Exception("No sound to play!")
        else:
            self.audio_player.play(self.sounds[sound_key], DEFAULT_VOLUME)

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