import boto3
import pygame
import threading
import os

class Polly:
    def __init__(self, text):
        self.text = text

    def play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load('speech.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def synthesize_and_play(self):
        polly_client = boto3.Session(
                aws_access_key_id=os.getenv("aws_access_key_id"),                     
                aws_secret_access_key=os.getenv("aws_secret_access_key"),  
                region_name='us-west-2'
        ).client('polly')

        response = polly_client.synthesize_speech(
            VoiceId='Brian',
            OutputFormat='mp3',
            Text=self.text,
            Engine='neural'
        )

        with open('speech.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())

        self.play_audio()
        os.remove("speech.mp3")

    def start(self):
        print("PLAYING AUDIO")
        audio_thread = threading.Thread(target=self.synthesize_and_play)
        audio_thread.start()
        

# Example usage
#text = "This is a sample text to be synthesized."
#synthesizer = Polly(text)
#synthesizer.start()
