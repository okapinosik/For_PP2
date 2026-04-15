import pygame
import os


class MusicPlayer:

    def __init__(self, music_folder="music"):
        pygame.mixer.init()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.music_folder = os.path.join(script_dir, music_folder)
        
        self.playlist      = []      
        self.current_index = 0      
        self.is_playing    = False
        self.is_stopped    = True

        self._load_playlist()


    def _load_playlist(self):
        supported = (".wav", ".mp3", ".ogg")
        if not os.path.isdir(self.music_folder):
            print(f"[Player] Warning: '{self.music_folder}' folder not found.")
            return

        for filename in sorted(os.listdir(self.music_folder)):
            if filename.lower().endswith(supported):
                full_path = os.path.join(self.music_folder, filename)
                self.playlist.append(full_path)

        if self.playlist:
            print(f"[Player] Loaded {len(self.playlist)} track(s).")
        else:
            print(f"[Player] No audio files found in '{self.music_folder}'.")

    def get_track_name(self, index=None):
        if not self.playlist:
            return "No tracks loaded"
        idx = index if index is not None else self.current_index
        return os.path.splitext(os.path.basename(self.playlist[idx]))[0]

    def get_total_tracks(self):
        return len(self.playlist)


    def play(self):
        if not self.playlist:
            print("[Player] No tracks to play.")
            return

        track = self.playlist[self.current_index]
        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_stopped = False
            print(f"[Player] Playing: {self.get_track_name()}")
        except pygame.error as e:
            print(f"[Player] Error loading track: {e}")

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_stopped = True
        print("[Player] Stopped")

    def pause_resume(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            print("[Player] Paused.")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            print("[Player] Resumed.")

    def next_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()


    def update(self):
        if self.is_playing and not pygame.mixer.music.get_busy():
            print("[Player] Track ended, advancing to next.")
            self.next_track()

    def get_position_seconds(self):
        if self.is_playing or not self.is_stopped:
            pos_ms = pygame.mixer.music.get_pos()
            return max(pos_ms // 1000, 0)
        return 0

    def get_status(self):
        if self.is_stopped:
            return "Stopped"
        if self.is_playing:
            return "Playing"
        return "Paused"