from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import argparse


def parse():
	output = argparse.ArgumentParser(description="Youtube transcript downloader", formatter_class=argparse.RawTextHelpFormatter)

	output.add_argument("link", type=str, help="Full path to target, could be url or local file (urls separated by lines).\nIf url start with \"http\".")
	output.add_argument("--output", type=str, help="Output file, if none given it will be printed to standart output.", default=None)
	output.add_argument("--wait", type=int, help="Maximum waiting time in seconds in between actions.", default=5)
	output.add_argument("--language", type=str, help="Prefered caption language. If not found then get auto-generated.", default="English")
	output.add_argument("--retries", type=int, help="Number of retries if error happens.", default=3)
	output.add_argument("--quiet", help="Don't show browser window.", action="store_true", default=False)
	output.add_argument("--browser", type=int, metavar="[0-3]", choices=range(4), help="Which browser to use. 0:Firefox, 1:Chrome, 2:Ie, 3:Opera", default=0)

	return output.parse_args()

def foo(args, driver, url):
	driver.get(url)
	e = driver.find_element_by_class_name("style-scope ytd-video-primary-info-renderer")
	e.find_elements_by_tag_name("yt-icon-button")[-1].click()
	
	e1 = driver.find_element_by_class_name("style-scope ytd-menu-service-item-renderer")
	e1.find_elements_by_tag_name("yt-formatted-string")[-1].click()

	temp = driver.find_elements_by_tag_name("ytd-transcript-footer-renderer")[-1]
	temp.click()

	for t in temp.find_elements_by_tag_name("a"):
		if t.text == args.language:
			t.click()

	e2 = driver.find_element_by_tag_name("ytd-transcript-body-renderer")

	return " ".join(e2.text.split("\n")[1::2])


def handler(args, driver, url):
	num = 1

	while num < args.retries:
		try:
			res = foo(args, driver, url)
			if args.output is None:
				print(res, end=" ")
			else:
				with open(sys.output, "a+") as f:
					f.append(res)
					f.append(" ")

			break
		except:
			driver.quit()
			driver = webdriver.Firefox()	
			driver.implicitly_wait(5)		

def getPlaylist(args, driver, url):
	driver.get(url)
	l = driver.find_elements_by_tag_name("ytd-playlist-video-renderer")  # so not dereferenced

	l = [link.find_element_by_tag_name("a").get_attribute("href").split("&")[0] for link in l]

	for link in l:
		handler(args, driver, link)

if __name__ == "__main__":
	args = parse()

	main = None

	if args.quiet:
		main = webdriver.PhantomJS()
	else:
		x = {0:webdriver.Firefox, 1:webdriver.Chrome, 2:webdriver.Ie, 3:webdriver.Opera}
		main = x[args.browser]()

	main.implicitly_wait(5)

	if args.link.startswith("http"):
		if "playlist" in args.link:
			getPlaylist(args, main, args.link)
		else:
			handler(args, main, args.link)
	else:
		with open(sys.argv[1], "r") as f:
			for line in f.readlines():
				handler(args, main, line)

	main.quit()
