#coding: utf8
import os
import yaml
from collections import defaultdict
from randoms import get_random_choice
from http_helper import HttpHelper
hh = HttpHelper()

class PowerUpProcessor(object):

	def __init__(self, item_type, inputs, group_id):
		self.group_id = group_id
		self.item_type = item_type
		self.pdata = self.extract_power_up_data(item_type)
		self.get_error = False
		self.inputs = self.pdata["inputs"]
		self.input_item = dict()
		self.output_item = dict()
		self.relative = self.pdata['relative']
		self.summary = self.pdata['summary']
		self.table = self.pdata['table']
		self.on_max_level = self.pdata['on_max_level']
		self.item_level = int(self.pdata.get("init_level", 0))
		# 输入参数和需要参数数量不一致
		if len(inputs) != len(self.inputs):
			self.get_error = True
			return
		# 把输入的数量存起来，判断是否超过上下限
		for idx, ipt in enumerate(self.inputs):
			item_name = ipt.keys()[0]
			item_attrs = ipt.values()[0]
			if int(inputs[idx]) < item_attrs['lb'] or int(inputs[idx]) > item_attrs['ub']:
				self.get_error = True
				return
			self.input_item[item_name] = int(inputs[idx])

	def extract_power_up_data(self, ptype):
		ori_path = r'E:\workspace\dn_robot\power_ups' + '\\' + ptype + '.yml'
		if not os.path.isfile(ori_path):
			return
		yml_data = yaml.load(open(ori_path))
		return yml_data.get('data')

	def upload_summary(self, item, diff_count):
		# 单个item的累加逻辑

		item_summary = self.summary.get(item)
		# 不需要计数的材料直接跳过
		if not item_summary:
			return
		count_type = item_summary["count_type"]
		# 计数方式是累加，直接加
		if count_type == "sum":
			if not self.output_item.get(item):
				self.output_item[item] = 0
			self.output_item[item] += diff_count
		if count_type == "max":
			if not self.output_item.get(item):
				self.output_item[item] = 0
			self.output_item[item] = max(diff_count, self.output_item[item])
		# 计数方式是记分布
		if count_type == "counter":
			if not self.output_item.get(item):
				self.output_item[item] = defaultdict(int)
			display_list = item_summary["display_list"]
			if diff_count in display_list:
				self.output_item[item][diff_count] += 1

	def apply_power_up_result(self, result):
		# 强化结果收集 消耗扣除 材料数累加 强化等级变化

		for item, count in result.items():
			# 检查是否够强化费用
			if item in self.input_item:
				if self.input_item[item] + count < 0:
					return False
				self.input_item[item] += count
		for item, count in result.items():
			# 确认材料够
			if item in self.input_item:
				continue
			# 强化等级有变，可能归零
			if item == 'level':
				self.item_level += count
				self.item_level = max(0, self.item_level)
				self.upload_summary("level", self.item_level)
			# 其他只可能是消耗型材料，直接上传结果
			else:
				self.upload_summary(item, count)
		return True

	def process_unable_power_up(self, init_msg=None):
		# 材料用尽时的结果通知
		msg = [
			u"强化完成，强化材料用尽，强化结果：" if not init_msg else init_msg,
		]
		# 强化等级的分布
		for k, v in self.summary.items():
			if v["count_type"] == "counter":
				oi = self.output_item.get(k)
				if not oi:
					msg.append(u"未强化到指定等级")
				else:
					sub_msg = []
					for level, count in sorted(oi.items()):
						sub_msg.append(u"+%s：%s次" % (level, count))
					msg.append(u"；".join(sub_msg))
			if v["count_type"] == "max":
				max_level = self.output_item.get(k)
				msg.append(u"强化至+%s" % max_level)
		# 其他消耗材料的结果
		msg.append(u"消耗材料：")
		for k, v in self.summary.items():
			if v["count_type"] == "sum":
				count = self.output_item.get(k) or 0
				msg.append(u"%s：%s" % (self.relative[k], count))
		return hh.send_group_msg(self.group_id, u'\n'.join(msg))

	def send_error_message(self):
		# 提示错误输入
		msg = [
			u"输入格式："
		]
		format = u".ding %s" % self.item_type
		for ipt in self.inputs:
			ipt_code = ipt.keys()[0]
			ipt_config = ipt.values()[0]
			ipt_name = self.relative[ipt_code]
			format += u' %s数量(%s~%s)' % (ipt_name, ipt_config["lb"], ipt_config["ub"])
		msg.append(format)
		return hh.send_group_msg(self.group_id, u'\n'.join(msg))

	def process_max_level(self):
		rests = []
		for k, v in self.input_item.items():
			rests.append(u"%s: %s个" % (self.relative[k], v))
		self.process_unable_power_up(
			init_msg=u'强化完成，已到达最大等级，剩余材料：%s，强化结果：' % (" ".join(rests))
		)

	def process_power_up(self):
		# 进行一次强化

		# 已经不能再强化了
		level_table = self.table.get(self.item_level)
		if not level_table:
			return self.process_max_level()
		succ_ratio = level_table["succ_ratio"]
		broken_ratio = (1 - succ_ratio) * level_table.get("broken_ratio", 0)
		fail_ratio = 1 - succ_ratio - broken_ratio
		# 得到强化结果
		power_result = get_random_choice(
			[succ_ratio, fail_ratio, broken_ratio],
			[level_table["succ_result"], level_table.get("fail_result", dict()), level_table.get("broken_result", dict())]
		)
		# 普通强化消耗
		if not self.apply_power_up_result(level_table["all_result"]):
			return self.process_unable_power_up()
		# 强化结果额外消耗
		self.apply_power_up_result(power_result)
		return True

	def run(self):
		if self.get_error:
			return self.send_error_message()
		while True:
			can_continue = self.process_power_up()
			if not can_continue:
				break

if __name__ == '__main__':
	p = PowerUpProcessor(u'顽强', ["100"], 655514756)
	p.run()