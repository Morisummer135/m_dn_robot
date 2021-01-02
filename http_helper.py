#coding: utf8
import json
import sys
import requests
encoding = sys.getfilesystemencoding()

def pstr(s):
	print s.encode(encoding)

class HttpHelper(object):

	def __init__(self):
		self.root_url = 'http://127.0.0.1:5700/'

	def get_group_list(self):
		'''
		168850524 う幻”★"城ぃ
		585827780 大华南会长交流群
		613986919 幻城不太正经群
		655514756 机器人测试群
		584050850 战胜飓风龙杰德的
		'''
		r = requests.get(self.root_url + 'get_group_list')
		for i in r.json()['data']:
			print i['group_id'],
			pstr(i['group_name'])

	def send_group_msgs(self, group_ids, msg):
		for group_id in group_ids:
			self.send_group_msg(group_id, msg)
		return

	def send_group_msg(self, group_id, msg):
		try:
			try:
				msg = msg.decode('gbk')
			except:
				pass
			r = requests.post(
				self.root_url + 'send_group_msg',
				data=dict(
					group_id=group_id,
					message=msg,
				)
			)
		except Exception as e:
			print 'send group msg %s to %s failed: %s' % (msg, group_id, e)

	def send_group_image(self, group_id, image_path):
		try:
			r = requests.post(
				self.root_url + 'send_group_msg',
				data=dict(
					group_id=group_id,
					message='[CQ:image,file=file:///%s]' % image_path
				)
			)
			print r.content
		except Exception as e:
			print 'send group msg %s to %s failed: %s' % (msg, group_id, e)

if __name__ == '__main__':
	helper = HttpHelper()
	helper.get_group_list()
	helper.send_group_msg(655514756, '.dn \xbd\xb1\xc0\xf8\n.dn \xc7\xbf\xbb\xaf\n.dn \xca\xfd\xbe\xdd')
	#helper.send_group_image(655514756, r'E:workspace\dn_robot\1.png')
