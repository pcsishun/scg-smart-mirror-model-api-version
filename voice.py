# from http import client
import keras
import numpy as np
import librosa
import recorder
import pvporcupine
import pyaudio
import struct
from time import sleep
from google.cloud import speech
from google.cloud import language_v1
import json     
import os
# from tensorflow import keras 

filename="./voice.wav"
voice_to_text_file = "./voice_text.txt"

def sleep_function(num):
    try:
        print(f'Waiting for start record in {num} seconds.')
        sleep(num)
        print("Start recording...")
    except KeyboardInterrupt:
        print("stop recording")
 

def func_analyze_entity_sentiment(text_content):
    is_word = open(text_content, 'r')
    my_text = is_word.read()
    
    print("is_word ====>",my_text)

    try:
        print("=== in try ===")
        client = language_v1.LanguageServiceClient.from_service_account_file('./keys.json')
        type_ = language_v1.types.Document.Type.PLAIN_TEXT

        language = "en"
        document = {"content": my_text, "type_": type_, "language": language}

        encoding_type = language_v1.EncodingType.UTF8

        response = client.analyze_entity_sentiment(request = {'document': document, 'encoding_type': encoding_type})

        path_file = open("./my_threshold.json")
        param_set = json.load(path_file)
        # print("my param_set func_analyze_entity_sentiment ===> ",param_set)

        for entity in response.entities:

            sentiment = entity.sentiment
            # print("sentiment.score ==> ", sentiment)

            ## https://cloud.google.com/natural-language ##  

            if sentiment.score >= param_set['voice_max_threshold']:
                set_json_object = {
                    "word": is_word.read(),
                    "select_lang": response.language,
                    "sentiment_score": sentiment.score,
                    "sentiment_magnitude": sentiment.magnitude,
                    "feeling": "positive"
                } 

                # print(set_json_object)

                with open("sentiment.json", "w") as outfile:
                    json.dump(set_json_object, outfile)
                # print("finish save json file")
            elif sentiment.score <= param_set['voice_max_threshold'] and sentiment.score > param_set['voice_min_threshold']:
                set_json_object = {
                    "word": is_word.read(),
                    "select_lang": response.language,
                    "sentiment_score": sentiment.score,
                    "sentiment_magnitude": sentiment.magnitude,
                    "feeling": "normal"
                }

                # print(set_json_object)

                with open("sentiment.json", "w") as outfile:
                    json.dump(set_json_object, outfile)
                # print("finish save json file")

            elif sentiment.score <= param_set['voice_min_threshold']:
                set_json_object = {
                    "word": is_word.read(),
                    "select_lang": response.language,
                    "sentiment_score": sentiment.score,
                    "sentiment_magnitude": sentiment.magnitude,
                    "feeling": "negative"
                }

                # print(set_json_object)

                with open("sentiment.json", "w") as outfile:
                    json.dump(set_json_object, outfile)
                # print("finish save json file")

    except Exception as error:
        print("sentiment error ==>", error)


 

def func_speech_to_text(voice_path):
    # print("==== start convert voice to text. ====")
    try:
        client = speech.SpeechClient.from_service_account_file('./keys.json')
        voice_path = voice_path
        # print("set voice_path ===>", voice_path)

        with open(voice_path,'rb') as f:
            voice_data = f.read()
            # print("create voice_data")

        audio_file = speech.RecognitionAudio(content=voice_data)
        # print("set audio_file")

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US", 
            audio_channel_count=1
        )
        # print("set config")

        response = client.recognize(config=config, audio=audio_file)
        # print("call back response")

        for result in response.results:
            # print("Transcript: {}".format(result.alternatives[0].transcript))
            write_f = open("voice_text.txt", "w")
            write_f.write(result.alternatives[0].transcript)
            write_f.close()
            # print("result speech to text =>",result.alternatives[0].transcript)
    except Exception as error:
        print("error ==> ",error)   


    

def app_start():
    try:
        ## set การเปิดการทำงานด้วยเสียง
        print("start app...")
        accesskey = "PSMtKVzOysHScGy5g2mgc2ClrX1Xf/PYYafb4o7kQQMUsZmrbBAR1Q=="

        porcupine = pvporcupine.create(access_key=accesskey,keywords=["computer"])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            # rate=porcupine.sample_rate,
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            # frames_per_buffer=porcupine.frame_length
            frames_per_buffer=porcupine.frame_length
        )


        # print("porcupine.sample_rate",porcupine.sample_rate)
        # print("porcupine.frame_length",porcupine.frame_length)
        
        # print("app listening voice...")
        while True:
            # สั่งใช้งาน function ปิดการทำงาน 
            ## คำสั่งเปิดการทำงานด้วยเสียง 
            # print(1)
            pcm = audio_stream.read(porcupine.frame_length)
            pcms = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcms)
            
            if keyword_index >= 0:
                # print("is recording")
                write_f = open("emotion_voice.txt", "w")
                write_f.write("Start recording...")
                write_f.close()

                while True:
                    try:
                        ## หน่วงเวลา 5 วิ
                        sleep_function(5)

                        ## สั่งบันทึกเสียง 10 วิ
                        recorder.record(filename)

                        ## สั่งทำนายเสียง
                        # pred = livePredictions(path='SER_model.h5',file='voice.wav')
                        # pred.load_model() # โหลด model 
                        # pred.makepredictions() # ทำนายผล 

                        func_speech_to_text(filename)
                        func_analyze_entity_sentiment(text_content=voice_to_text_file)

                        os.remove("voice.wav") # ลบไฟล์เสียงออก
                        # print("finish predict")

                    except KeyboardInterrupt:
                        print("stop recording")
                        break 
    except:
        print("error detect!")
        if porcupine is not None:
            porcupine.delete()
            print("End")
        if audio_stream is not None:
            audio_stream.close()
            print("End")
        if pa is not None:
            pa.terminate()
            print("End")

# app_start()

## เรียกใช้งาน app เเละทำการ loop inf. ##
# action = True
# while action == True:
#     print("action..")
#     app_start()
