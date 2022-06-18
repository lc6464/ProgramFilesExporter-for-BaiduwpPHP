from json import load as loadJSON
from json import dumps as dumpsJSON
import os, re, shutil, sys, zipfile
from os import path




try: # 尝试读取排除规则列表
	with open('./exclude-list.json', encoding="utf-8") as f:
		excludeList = loadJSON(f)
except Exception as e: # 若读取失败
	print('读取排除规则列表失败！')
	print(e)
	sys.exit(0)



files = []

try: # 尝试获取文件列表
	for name in os.listdir("../"):
		for i in excludeList: # 获取排除列表
			if re.search(i, name) != None: # 若匹配到排除规则
				break
			files.append('../' + name)
except Exception as e: # 若获取失败
	print('获取文件列表失败！')
	print(e)
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
		walkResult = tuple(os.walk('../ProgramFiles/')) # 提前获取 walk 结果，防止把在压缩过程中把不完整的压缩包一并压入压缩包
		f = zipfile.ZipFile('../ProgramFiles/ProgramFiles.zip', 'w', zipfile.ZIP_DEFLATED) # 创建压缩包
		try:
			for root, dirs, subFiles in walkResult: # 压缩文件
				for name in subFiles:
					f.write(path.join(root, name), '%s/%s' % (root.replace('../ProgramFiles/', ''), name), compresslevel=9)
			print('压缩成功！')
		except Exception as e:
			print('压缩失败！')
			print(e)
		finally:
			f.close()
	except Exception as e:
		print('压缩失败！')
		print(e)
except Exception as e:
	print('复制文件失败！')
	print(e)
	print('您可以自行复制这些文件：')
	print(dumpsJSON(files))