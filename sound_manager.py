from arcade import Sound, load_sound

DEFAULT_VOLUME = 0.7
SFX_BEETLE_HIT = "Assets/Sound/SFX/impact2_noisecollector.wav"
SFX_BEETLE_DEAD = "Assets/Sound/SFX/beetle_dead_mixkit.wav"
SFX_PEASHOOTER = "Assets/Sound/SFX/pew_xtrgamr.wav"

MUSIC_BANJOS_PLACEHOLDER = "Assets/Sound/Music/banjo_loop.wav"

BEETLE_HIT = "BeetleHit"
BEETLE_DEAD = "BeetleDead"
PEASHOOTER_PEW = "PeashooterPew"
BANJOS = "Banjos"

class SoundManager:
    # This creates the sound manager as a singleton instance
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SoundManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.sounds = {
            BEETLE_HIT: load_sound(SFX_BEETLE_HIT), 
            BEETLE_DEAD: load_sound(SFX_BEETLE_DEAD), 
            PEASHOOTER_PEW: load_sound(SFX_PEASHOOTER)
        }
        self.music = {
            BANJOS: load_sound(MUSIC_BANJOS_PLACEHOLDER)
        }
        self.audio_player = None

    def set_volume(self, volume=None):
        if not volume:
            self.audio_player.set_volume = DEFAULT_VOLUME
        else:
            self.audio_player.set_volume = volume

    def play_sound(self, sound_key):
        if not sound_key:
            raise Exception("No sound to play!")
        else:
            self.audio_player = self.sounds[sound_key].play(DEFAULT_VOLUME)

    def stop_sound(self, sound_key):
        if not sound_key:
            pass
        else:
            self.audio_player = self.sounds[sound_key].stop

    def play_music(self, music_key):
        if not music_key:
            pass
        else:
            self.audio_player = self.music[music_key].play(DEFAULT_VOLUME)

    def change_music(self, current_music, new_music):
        # TODO: Methods of changing the music. Hard stop, fade, other?
        if not new_music or not current_music:
            pass
        else:
            self.fade_music(current_music, new_music)

    # Called in on_update to fade the music in one or two directions
    def fade_music(self, current_track, new_track = None, target_volume = 0):
        # TODO: Figure out fade method. Maybe set target volume, then decrease by a rate per on_update?
        if not new_track:
            # TODO: Get current track & set_volume each on_update by a small decrement
            pass
        elif current_track and new_track:
            # TODO: Get current track & next track, start playing new_track at get_length(current_track) - seconds
            # TODO: Begin in/decrementing each track per on_update
            pass
        else:
            pass

    def stop_music(self, music_key):
        if not music_key:
            pass
        else:
            self.music[music_key].stop