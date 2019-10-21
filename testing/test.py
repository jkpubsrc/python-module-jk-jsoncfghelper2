#!/usr/bin/python3


import os

import jk_testing
import jk_json

import jk_jsoncfghelper2




DATA_DIR_PATH = "data"





class TestSetup(object):

	def __init__(self, name:str, dirPath:str):
		self.__testData = jk_json.loadFromFile(dirPath + "/testData.jsonc")
		self.__expectedOutput = jk_json.loadFromFile(dirPath + "/expectedOutput.jsonc")
		self.__scmgr = jk_jsoncfghelper2.loadFromXMLFile(dirPath + "/definition.xml")
		self.__checker = self.__scmgr.get("main")
		assert self.__checker is not None
		self.__name = name
	#

	def name(self):
		return self.__name
	#

	@jk_testing.TestCase()
	def __call__(self, ctx):
		ret =list(self.__checker.check(self.__scmgr, self.__testData))

		bError = False
		if len(self.__expectedOutput) != len(ret):
			bError = True
		else:
			for l1, l2 in zip(ret, self.__expectedOutput):
				if (l1[0] != l2[0]) or (l1[1] != l2[1]):
					bError = True
					break
		
		if bError:
			ctx.log.error("Expected output did not match output encountered!")

			lines = jk_json.dumps(self.__testData, indent="\t", sort_keys=True, cls=jk_json.ObjectEncoder).split("\n")
			log2 = ctx.log.descend("Data:")
			for line in lines:
				log2.warn(line)

			log2 = ctx.log.descend("Output encountered:")
			if len(ret) > 0:
				for p, errMsg in ret:
					log2.warn(p + " => " + errMsg)
			else:
				log2.warn("(none)")

			log2 = ctx.log.descend("Output expected:")
			if len(self.__expectedOutput) > 0:
				for p, errMsg in self.__expectedOutput:
					log2.warn(p + " => " + errMsg)
			else:
				log2.warn("(none)")

			raise Exception()

		#i = 0
		#for path, errMsg in ret:
	#

#





testDriver = jk_testing.TestDriver()
#testDriver.data["abc"] = "abc"

tests = []
for dirEntry in os.scandir(DATA_DIR_PATH):
	if dirEntry.is_dir():
		tests.append(
			(TestSetup(dirEntry.name, DATA_DIR_PATH + "/" + dirEntry.name), True)
		)

results = testDriver.runTests(tests)

#reporter = jk_testing.TestReporterHTML()
#reporter.report(results, showInWebBrowser=True)









