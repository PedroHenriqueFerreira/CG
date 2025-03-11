from playsound import playsound

class Sound:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def play(self):
        try:
            playsound(self.filepath, False)
        except:
            print(f"Error: Could not play sound file {self.filepath}")