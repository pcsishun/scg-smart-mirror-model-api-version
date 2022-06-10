def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    import os
    import json

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vision-api-key.json"
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', '0', '1', '2',
                       '3', '4')
    print('Faces')

    for face in faces:

        if(likelihood_name[face.anger_likelihood] == '0' and likelihood_name[face.joy_likelihood] == '0' and likelihood_name[face.surprise_likelihood] == '0' and likelihood_name[face.sorrow_likelihood] == '0'):

            set_video_emotion = {
                "anger": likelihood_name[face.anger_likelihood],
                "joy":likelihood_name[face.joy_likelihood],
                "surprise": likelihood_name[face.surprise_likelihood],
                "sorrow": likelihood_name[face.sorrow_likelihood],
                "highest_emotion":"normal"
            }
            
            # print(set_video_emotion)

            with open("video_emotion.json", "w") as outfile:
                        json.dump(set_video_emotion, outfile)
        else:

            set_video_emotion_find_max_mood = {
                "anger": likelihood_name[face.anger_likelihood],
                "joy":likelihood_name[face.joy_likelihood],
                "surprise": likelihood_name[face.surprise_likelihood],
                "sorrow": likelihood_name[face.sorrow_likelihood]
            }

            set_video_emotion = {
                "anger": likelihood_name[face.anger_likelihood],
                "joy":likelihood_name[face.joy_likelihood],
                "surprise": likelihood_name[face.surprise_likelihood],
                "sorrow": likelihood_name[face.sorrow_likelihood],
                "highest_emotion":max(set_video_emotion_find_max_mood, key=lambda key: set_video_emotion_find_max_mood[key])
            }

            with open("video_emotion.json", "w") as outfile:
                        json.dump(set_video_emotion, outfile)


        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


detect_faces("./test.png")
