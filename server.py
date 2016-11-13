# from fbrecog import recognize
# path = 'group.jpg' #Insert your image file path here
# access_token = 'EAAMZBwQ6lUVgBANVxZCcbx3HpsMszZCRBxcmt49R0jorlPeumncqI2X6kiYUopYsxTKUovPoPLgkxE7ZCivM1umsZBf3so1z15hLeQwCfbfgAmKjSyakhIEvXTbFoNGgVwtZC1SZAH5WyeTOXegt1DZCKyN9IeVSUDC0LJpAZBmdusgZDZD' #Insert your access token obtained from Graph API explorer here
# cookie = 'datr=nvD9V4KNFAkqGm7j1RYCKL4d; sb=K_L9V5XyKIEdCSShFcgYsOQl; pl=n; lu=giOm6-BIgZUHjNlQrnuHFK9Q; js_ver=2507; c_user=100000636771951; xs=31%3AQFXZYT3XxXVzvw%3A2%3A1476260395%3A7829; s=Aa6sOBZJk3MXtrEW.BYJ01T; fr=099KsM6O7krHdqPC7.AWWAjBg7-1eW-F9ahqox76ejGwE.BX_fCe.jT.AAA.0.0.BYJ-SM.AWU4RuXj; csm=2; p=-2; act=1479009737748%2F4; presence=EDvF3EtimeF1479009750EuserFA21B00636771951A2EstateFDt2F_5bDiFA2user_3a1B02089042068A2CAcDiFA2user_3a1599020823A2C_5dElm2FA2user_3a1599020823A2Euct2F1478994738301EtrFA2loadA2EtwF1155297320EatF1479009749144G479009750371CEchFDp_5f1B00636771951F5CC' #Insert your cookie string here
# fb_dtsg = 'AQHY18E6B8lB:AQEQOABx-E6_' #Insert the fb_dtsg parameter obtained from Form Data here.
# print(recognize(path,access_token,cookie,fb_dtsg))

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from fbrecog import recognize
from PIL import Image
import uuid
import json
import io

app = Flask(__name__)
socketio = SocketIO(app)

responseData = []

def recognize_image(imagepath):
	path = imagepath #Insert your image file path here
	access_token = 'EAAMZBwQ6lUVgBACdeTEhFLafFP2MZBU4CVyXedWfoADb0osQZCGx9BgqDTH2BVF1HoZCbuwT0LHKOOyZCWP8aHUxmjnirOhK6zfnGbAdUkJjsrkZCXDQkI1HkZCWiFEaAQNlHffb4UoYifVn70yz0ekUwKZAQowaKDc295SEORlItQZDZD' #Insert your access token obtained from Graph API explorer here
	cookie = 'datr=nvD9V4KNFAkqGm7j1RYCKL4d; sb=K_L9V5XyKIEdCSShFcgYsOQl; pl=n; lu=giOm6-BIgZUHjNlQrnuHFK9Q; js_ver=2507; c_user=100000636771951; xs=31%3AQFXZYT3XxXVzvw%3A2%3A1476260395%3A7829; s=Aa6sOBZJk3MXtrEW.BYJ01T; fr=099KsM6O7krHdqPC7.AWWAjBg7-1eW-F9ahqox76ejGwE.BX_fCe.jT.AAA.0.0.BYJ-SM.AWU4RuXj; csm=2; p=-2; act=1479009737748%2F4; presence=EDvF3EtimeF1479009750EuserFA21B00636771951A2EstateFDt2F_5bDiFA2user_3a1B02089042068A2CAcDiFA2user_3a1599020823A2C_5dElm2FA2user_3a1599020823A2Euct2F1478994738301EtrFA2loadA2EtwF1155297320EatF1479009749144G479009750371CEchFDp_5f1B00636771951F5CC' #Insert your cookie string here
	fb_dtsg = 'AQHY18E6B8lB:AQEQOABx-E6_' #Insert the fb_dtsg parameter obtained from Form Data here.
	responseData = recognize(path,access_token,cookie,fb_dtsg)
	if not responseData:
		socketio.emit('new_message', {'new_message': 'Sorry, I could not recognize this person.'})
	else:
		print(responseData)
		if len(responseData) == 1:
			location = ''
			if responseData[0]['x'] <= 40:
				location = 'left'
			elif responseData[0]['x'] > 40 and responseData[0]['x'] <= 60:
				location = 'center'
			else:
				location = 'right'
			name = responseData[0]['name']
			speechResponse = 'You have ' + name + ' on your ' + location
			socketio.emit('new_message', {'found': speechResponse})
		else:
			arr = []
			for i in range(0,len(responseData)):
				location = ''
				if responseData[i]['x'] <= 40:
					location = 'left'
				elif responseData[i]['x'] > 40 and responseData[i]['x'] <= 60:
					location = 'center'
				else:
					location = 'right'
				arr.append({'name': responseData[i]['name'], 'location': location })
			speechResponse = 'You have ' + arr[0]['name'] + ' on your ' + arr[0]['location'] + ' and ' + arr[1]['name'] + ' on your ' + arr[1]['location']
			socketio.emit('new_message', {'found': speechResponse})



@app.route("/")
def index():
	return render_template('index.html')

@socketio.on('send_message')
def handle_source(json_data):
    print(json_data)
    # text = json_data['message'].encode('ascii', 'ignore')
    # socketio.emit('echo', {'echo': 'test.jpg'})

@socketio.on('send_image')
def image_sent(raw):
	fileName = str(uuid.uuid4())
	enrollmentMessage = 'New image enrolled: ' + fileName
	print(enrollmentMessage)
	img = Image.open(io.BytesIO(raw))
	path = fileName+'.jpg'
	img.save(path)
	# print(path)
	recognize_image(path)


if __name__ == "__main__":
    socketio.run(app)