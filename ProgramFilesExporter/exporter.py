from json import load as loadJSON
from json import dumps as dumpsJSON
import os, re, shutil, sys, zipfile
from os import path




try: # 尝试读取排除规则列表
	with open('./exclude-list.json', encoding="utf-8") as f:
		excludeList = loadJSON(f)
except: # 若读取失败
	print('读取排除规则列表失败！')
	sys.exit(0)



files = []

try: # 尝试获取文件列表
	for name in os.listdir("../"):
		rs = []
		for i in excludeList: # 获取排除列表
			rs.append(re.search(i, name) == None) # 判断是否符合排除规则
		if False not in rs: # 获取文件列表
			files.append('../' + name)
	print(dumpsJSON(files))
except: # 若获取失败
	print('获取文件列表失败！')
	sys.exit(0)


if files == []:
	print('没有文件需要导出！')
	sys.exit(0)


try: # 尝试复制文件
	if not path.exists('../ProgramFiles/'): # 若文件夹不存在则创建
		os.mkdir('../ProgramFiles/')
	for root, dirs, subFiles in os.walk('../ProgramFiles/', topdown=False): # 清空文件夹
		for name in subFiles:
			os.remove(path.join(root, name))
		for name in dirs:
			os.rmdir(path.join(root, name))
	for name in files: # 复制文件和文件夹
		shutil.copytree(name, '../ProgramFiles/' + name[3:]) if path.isdir(name) else shutil.copy(name, '../ProgramFiles/')
	print('导出成功！')
	print('-' * 20)
	print('正在压缩中……')
	try: # 压缩
		walkResult = tuple(os.walk('../ProgramFiles/'))
		f = zipfile.ZipFile('../ProgramFiles/ProgramFiles.zip', 'w', zipfile.ZIP_DEFLATED)
		try:
			for root, dirs, subFiles in walkResult: # 压缩文件夹
				for name in subFiles:
					f.write(path.join(root, name), '%s/%s' % (root.replace('../ProgramFiles/', ''), name), compresslevel=9)
			print('压缩成功！')
		except:
			print('压缩失败！')
		finally:
			f.close()
	except:
		print('压缩失败！')
except:
	print('复制文件失败！')
	print('您可以自行复制这些文件：')
	print(dumpsJSON(files))