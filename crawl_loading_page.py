from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

prefix_url = 'https://paperswithcode.com'


def scrollDown(browser, numberOfScrollDowns):
	body = browser.find_element_by_tag_name("body")
	while numberOfScrollDowns >=0:
		body.send_keys(Keys.PAGE_DOWN)
		numberOfScrollDowns -= 1
		time.sleep(0.3)
	return browser

def crawl_url(url, run_headless=False):
	f = open('sub_task_links_details.txt', 'w')

	url = correct_url(url)
	browser = webdriver.Chrome()
	browser.get(url)
	
	content = browser.page_source
	soup = BeautifulSoup(content)
	

	all_domain = soup.findAll('div', attrs={'class':'col-md-12'})
	all_domain_links = [domain.find('a', href=True) for domain in all_domain]
	all_domain_links = [domain['href'] for domain in all_domain_links if domain != None]

	
	all_sub_task_links = []
	all_paper_links = []
	all_github_links = []
	
	for domain_link in all_domain_links:
		new_url = prefix_url + domain_link
		
		browser.get(new_url)
		
		new_content = browser.page_source
		new_soup = BeautifulSoup(new_content)
				
		displayed_task = new_soup.findAll('div', attrs={'class':"card-deck card-break infinite-item"})
		displayed_task_link = [disp_task.find("a", href=True) for disp_task in displayed_task]
		displayed_task_link = [disp_task['href'] for disp_task in displayed_task_link if disp_task != None]
		
		all_sub_task_links.extend(displayed_task_link)
		
		# Get all task link
		tasks = new_soup.findAll('div', attrs={'class':'sota-all-tasks'})
		task_links = [task.find('a', href=True) for task in tasks]
		task_links = [task['href'] for task in task_links if task != None]
		
						
		for task_url in task_links:
			task_url = prefix_url + task_url
			
			browser.get(task_url)
			task_content = browser.page_source
			task_soup = BeautifulSoup(task_content)
			
			# Get all sub task links
			sub_tasks = task_soup.findAll('div', attrs={'class':'card-deck card-break infinite-item'})
			sub_task_links = [sub_task.find('a', href=True) for sub_task in sub_tasks]
			sub_task_links = [sub_task['href'] for sub_task in sub_task_links if sub_task != None]
			
			all_sub_task_links.extend(sub_task_links)
			
			for sub_task_link in sub_task_links:
				sub_task_link = prefix_url + sub_task_link
				#print (sub_task_link)
				f.write('sub task link: '+sub_task_link+"\n")
				
				#'''
				#print (sub_task_link)
				#break
				browser.get(sub_task_link)
				browser = scrollDown(browser, 1000)
				sub_task_content = browser.page_source
				sub_task_soup = BeautifulSoup(sub_task_content)
						
				papers  = sub_task_soup.findAll('a', href=True, attrs={'class':'badge badge-light'})
				paper_links  = [paper['href'] for paper in papers if paper != None]		
				
				for paper_link in paper_links:
					paper_link = prefix_url + paper_link
					
					browser.get(paper_link)
					paper_content = browser.page_source
					paper_soup = BeautifulSoup(paper_content)
					
					source_paper = paper_soup.findAll('a', href=True, attrs={'class':'badge badge-light'})[0]['href']	
					githubs = paper_soup.findAll('a', href=True, attrs={'class':'code-table-link'})
					github_links  = [github['href'] for github in githubs if github != None]		
					
					#print (source_paper)
					#print (github_links)
					#print ('-'*30)
					f.write('\tsource paper: '+source_paper+"\n")
					f.write('\tgithub_links: '+"\n")
					[f.write('\t\t'+github_link+"\n") for github_link in github_links]
					f.write('-'*30+"\n")
					
					all_paper_links.append(source_paper)
					all_github_links.extend(github_links)
				#'''
					
		
	print ("all sub task links: ", len(all_sub_task_links))
	print ("all paper links: ", len(all_paper_links))
	print ("all github links: ", len(all_github_links))

	browser.quit()
	f.close()

if __name__=='__main__':
	url = "https://paperswithcode.com/sota"
	crawl_url(url)
	