from requests import get, post

class SetClines:
	web = {
		"app_name": "Main",
		"app_version": "4.3.3",
		"platform": "Web",
		"package": "web.rubika.ir",
		"lang_code": "fa"
	}

	android = {
	    "app_name":"Main",
		"app_version":"3.3.2",
		"platform":"Android",
		"package":"app.rbmain.a",
		"lang_code":"fa"
	}


class Server:
	matnadress = []
	m = get("https://getdcmess.iranlms.ir/").json()["data"]["API"]
	for k,v in m.items(): 
	      matnadress.append(v)
	      
	      


	
	filesadress = []
	m = get("https://getdcmess.iranlms.ir/").json()["data"]["API"]
	for k,v in m.items():
	      filesadress.append(v)
	      
	socket = []
	sock = get("https://getdcmess.iranlms.ir/").json()["data"]["socket"]
	
	for k,v in sock.items():
	      socket.append(v)
	      
	      
	      


