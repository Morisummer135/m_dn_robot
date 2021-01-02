#coding: utf8
import json

from wsgiref.simple_server import make_server
from dn_data_extractor import dn_data_extract
from http_helper import HttpHelper
hh = HttpHelper()

def process_dn_data_message(msg, text):
	image_path = dn_data_extract(msg["group_id"], text)
	if not image_path:
		print 'get image path failed msg = %s' % text
	elif isinstance(image_path, list):
		hh.send_group_msg(msg['group_id'], '\n'.join(image_path))
	elif image_path.startswith('text:'):
		hh.send_group_msg(msg['group_id'], image_path[5:])
	else:
		hh.send_group_image(msg['group_id'], image_path)
	return 'success'

def application(environ, start_response):
	print 'get'
	start_response('200 OK', [('Content-Type', 'text/html')])
	request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	msg = json.loads(environ['wsgi.input'].read(request_body_size))
	if "message" not in msg:
		return "success"
	text = msg['message']
	if text.startswith('.dn') or text.startswith('.test') or text.startswith(".ding"):
		return process_dn_data_message(msg, text)
	#hh.send_group_msg(655514756, msg['sender']['nickname'] + ': ' + msg['message'])
	return 'success'

if __name__ == '__main__':
	httpd = make_server('', 9998, application)
	httpd.serve_forever()