#coding:gbk
__author__ = 'hejun 244105445@qq.com'


import os
import sys
import unittest


ROOT_DIR = 'test'

def get_test_dir():
	'''
	:return: [test_sub1,test_sub2]
	'''
	test_dir_path = os.path.join(os.getcwd(),ROOT_DIR)
	return [dir for path,dir,file in os.walk(test_dir_path)][0]

def load_modle(module_dir):
	'''
	:param module_dir: d:/test/test_sub1
	:return: [test.test_sub1.test]
	'''
	case_file_path = os.path.join(os.getcwd(),ROOT_DIR,module_dir)
	module_lst = []
	for file in os.listdir(case_file_path):
		if file.startswith('__') or file.endswith('pyc'):
			continue
		module_name = ROOT_DIR + '.' + module_dir + '.' + file.split('.')[0]
		module_lst.append(module_name)
	return module_lst

def load_test_case(module_name):
	'''
	:param module_name: test.test_sub1.test
	:return:[[obj],[]]
	'''
	__import__(module_name)
	case_lst = []#扩展使用
	for test_class in dir(sys.modules[module_name]):
		if test_class.startswith('__'):
			continue
		case_obj_lst = []
		obj = getattr(sys.modules[module_name],test_class)
		for test_case in dir(obj):
			if not test_case.startswith('test'):
				continue
			case_obj = obj(test_case)
			case_obj_lst.append(case_obj)
		case_lst.append(case_obj_lst)
	return case_lst

if __name__ == '__main__':
	case_dir_lst = get_test_dir()
	for case_dir in case_dir_lst:
		module_lst = load_modle(case_dir)
		for module in module_lst:
			case_lst = load_test_case(module)
			suite = unittest.TestSuite()
			for case in case_lst[0]:#简化逻辑控制一个测试文件只支持一个测试类
				suite.addTest(case)
			rlt = unittest.TextTestRunner().run(suite)
			print '{} test case run: {}, fail: {}.'.format(module,rlt.testsRun,len(rlt.failures))
