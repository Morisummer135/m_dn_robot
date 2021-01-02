#coding: utf8
import random
import os
import json
from power_up import PowerUpProcessor

def list_file_from_dir(inputs, dir_path):
	dirs = os.listdir(dir_path)
	result = []
	for f in dirs:
		res = '.dn ' + ' '.join(inputs) + ' '
		if '.png' in f:
			res += f[:-4]
		else:
			res += f
		result.append(res)
	return result

def test_pet(count):
	if count < 10 or count > 1000:
		return
	ori_count = count
	cnt = 0
	blue_hat = 0
	chicken_hat = 0
	while count >= 10:
		cnt += 1
		a = random.randint(1, 100)
		print a
		count -= 10
		if a <= 49:
			print u'友谊之心×5'
			count += 5
		elif a <= 49 + 20:
			print u'友谊之心×6'
			count += 6
		elif a <= 49 + 20 + 13:
			print u'友谊之心×7'
			count += 7
		elif a <= 49 + 20 + 13 + 7:
			print u'友谊之心×4'
			count += 4
		elif a <= 49 + 20 + 13 + 7 + 4:
			print u'蓝帽子'
			blue_hat += 1
		elif a <= 49 + 20 + 13 + 7 + 4 + 3:
			print u'友谊之心×3'
			count += 3
		elif a <= 49 + 20 + 13 + 7 + 4 + 3 + 3:
			print u'友谊之心×8'
			count += 8
		else:
			print '鸡仔帽'
			chicken_hat += 1
	return u'text:原%s个友谊之心\n共计%s次花豹分解\n蓝帽子%s个\n鸡仔帽%s个\n剩余%s个友谊之心' % (
		ori_count, cnt, blue_hat, chicken_hat, count
	)
		

def testfun(inputs):
	item = inputs[0]
	count = int(inputs[1])
	if item not in (u'宠物',):
		return
	return test_pet(count)

def dn_data_extract(group_id, text):
	ori_path = r'E:\workspace\dn_robot\images'
	inputs = text.split(' ')[1:]
	operator = text.split(' ')[0]
	if operator == '.dn':
		final_path = ori_path + '\\' + '\\'.join(inputs)
		print final_path
		if os.path.isfile(final_path + '.png'):
			return final_path + '.png'
		if os.path.isdir(final_path):
			return list_file_from_dir(inputs, final_path)
		return
	elif operator == '.ding':
		if int(group_id) == 809318266:
			return
		if len(inputs) == 0:
			return
		item_type = inputs[0]
		p = PowerUpProcessor(item_type, inputs[1:], group_id)
		return p.run()
	elif operator == '.test':
		return testfun(inputs)

if __name__ == '__main__':
	text = u'.dn'
	print dn_data_extract(text)