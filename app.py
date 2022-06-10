# from distutils.log import debug
# from flask import Flask
# from flask_cors import CORS, cross_origin
# from videotester import sendData
# import sys
# import pickle

# app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route('/')
# def index():
#     file = open('emotional.txt', 'rb')
#     emotion = pickle.load(file)
#     file.close()
#     print("face emotion =>",emotion)
#     return emotion

# @app.route('/voice')
# def voice_detect():
#     file = open("")
#     emotion = pickle.load(file)
#     file.close()
#     print("voice emotion =>",emotion)
#     return emotion



# if (__name__) == "__main__":
#     app.run(debug=True)