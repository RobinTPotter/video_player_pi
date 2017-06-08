from subprocess import Popen, PIPE, STDOUT
from config import *
from flask import Flask, render_template, redirect, url_for
import os
import threading

p=None
app = Flask(__name__)
files = []
commands = [
	{'letter': 'q', 'name': 'quit'},
	{'letter': 'space', 'name': 'pause', 'alt':' ' },
	{'letter': '+', 'name': 'vol up' },
	{'letter': '-', 'name': 'vol down' },
	{'letter': 'o', 'name': 'on 10 mins' },
	{'letter': 'i', 'name': 'back 10 mins' },
	{'letter': 'right', 'name': 'on 30 secs' , 'alt':'\027[C'},
	{'letter': 'left', 'name': 'back 30 secs' , 'alt':'\027[D'},
	{'letter': 'kill', 'name': 'killall' },
]

@app.route('/command/<command>')
def send_command(command):
	showMenu = False
	if command in [x['letter'] for x in commands]: 
		commando = [c for c in commands if c['letter']==command][0]
		if 'alt' in commando.keys(): command = commando['alt']
		try:
			#print('sending >'+ command +'<')
			#stdo, stde = p.communicate(command+'\0')
			#print('stdo: '+str(stdo))
			#print('stde: '+str(stde))
			print('why dyour force it')
			if not command=='kill': p.stdin.write(command)
			else:
				getproc = Popen('pgrep omxplayer'.split(),stdin=PIPE,stdout=PIPE)
				processes = ' '.join(getproc.communicate()[0].split('\n')).rstrip()
 				Popen(('kill -9 '+processes).split(' '), stdout=PIPE, stdin=PIPE, stderr=STDOUT).communiate()

			if command=='q' or command=='kill': showMenu = True
		except Exception as e:
			showMenu = True
			print('communicate exception in command {0}\n{1}'.format(str(command),e))
	
	if showMenu==True:
		return redirect(url_for('hello'))
	else:
		return render_template('commands.html', commands=commands)


@app.route('/commands')
def commands_route():
	return render_template('commands.html', commands=commands)

@app.route('/play/<int:thing>')
def play(thing):
 	file = [f['directory']+'/'+f['file'] for f in files if f['number']==thing][0]
	global p
 	p = Popen(['omxplayer', '-b',file], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
	print(p)
	print(dir(p))
	return render_template('commands.html', commands=commands)


@app.route('/')
def hello():
	global files
	files = []
	num = 0
	for d in DIR:
		try:
			for e in EXT:
				lfiles=[(d,z) for z in  os.listdir(d) if z.endswith(e)]
				files = files + lfiles
		except:
			print('maybe error reading folder')

	out='<ul>'
	files = zip(files,range(0,len(files)))
	files = [{'directory': a[0], 'file':a[1], 'number': b} for a,b in files]
	files.sort(key=lambda x: x['file'])
	#print(files)
	#for d,f,n in files:
	#	print((d,f,n))		
	#	out += '<li><a href="play/'+str(n)+'">'+f+'</a></li>'
	#out += '</ul>'
	#return out
	return render_template('index.html', files=files)

