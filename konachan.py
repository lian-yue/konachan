import os, urllib2, json, threading,signal, time




limit = 6

page = 1

maxPage = 0


fileDir = './File/%s.jpg'


bufferSize = 1024 * 32





print "Ctrl + C  Exit"




isExit = False

def downloadFile(url, fileName):
	output = fileDir % fileName
	if os.path.isfile(output):
		print 'Exists: ' + fileName
	else:
		try:
			response=urllib2.urlopen(url)
			file = open(output, 'wb')
			contents = response.read(bufferSize)

			print 'Download: ' + fileName
			while contents:
				file.write(contents)
				if isExit:
					file.close()
					os.remove(output)
					break
				contents = response.read(bufferSize)
			file.close()
		except urllib2.URLError,e:
			print "Error:  " + fileName + "   " + e.reason







def handler(signum, frame):
	global isExit
	isExit = True

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)



downloads = {}

isWhile = True
while (isWhile):
	print "Page: " + str(page)
	response = urllib2.urlopen('http://konachan.com/post.json?page='+ str(page) +'&limit=' + str(limit))
	contents = response.read()
	jsonContents = json.loads(contents)
	isWhile = contents and len(jsonContents) and (maxPage == 0 or page <= maxPage)

	for i in jsonContents:
		if not i['id'] in downloads:
			fileName = str(i['id']) + '_' + i['tags'].replace('/', ' ') + '_' + str(i['width']) + '_' + str(i['height']);
			downloads[fileName] = threading.Thread(target=downloadFile,args= (i['file_url'], fileName), name = 'thread-' + str(i['id']))
			downloads[fileName].start()




	while len(downloads) > (limit / 2):
		if isExit:
			break
		delID = []
		for i, el in enumerate(downloads):
			if downloads[el].isAlive():
				downloads[el].join()
			else:
				delID.append(el)

		for i in delID:
			del downloads[i]
		time.sleep(0.01)

	if isExit:
		break

	page = page + 1
	# isWhile = False
	if not isWhile:
		break




print "Complete"

