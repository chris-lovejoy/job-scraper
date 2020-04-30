#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:35:04 2020

@author: chrislovejoy
"""


import urllib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os


def find_jobs_from(website, job_title, location, desired_characs):
    # other to include: date, output_type, listed_since
    # add in whether Chrome driver or otherwise
    
    
    if website == 'Indeed':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_information_indeed(job_soup, desired_characs)
    
    if website == 'CWjobs':
        location_of_driver = os.getcwd()
        driver = initiate_driver(location_of_driver, browser='chrome')
        job_soup = make_job_search(job_title, location, driver)
        jobs_list, num_listings = extract_job_information_cwjobs(job_soup, desired_characs)
    
    save_jobs_to_excel(jobs_list)
 
    print('{} new job postings retrieved. Stored in "results.xls".'.format(num_listings))
    

## ======================= GENERIC FUNCTIONS ======================= ##

def save_jobs_to_excel(jobs_list):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel("results.xls") #TODO: allow user to specify this name



## ================== FUNCTIONS FOR INDEED.CO.UK =================== ##

def load_indeed_jobs_div(job_title, location):
    getVars = {'q' : job_title, 'l' : location}
    url = ('https://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup

def extract_job_information_indeed(job_soup, desired_characs):
    job_elems = job_soup.find_all('div', class_='jobsearch-SerpJobCard')
     
    cols = []
    extracted_info = []
    
    
    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(titles)                    
    
    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_indeed(job_elem))
        extracted_info.append(companies)
    
    if 'links' in desired_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)
    
    jobs_list = {}
    
    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]
    
    num_listings = len(extracted_info[0])
    
    return jobs_list, num_listings


def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', class_='title')
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='company')
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_elem):
    link = job_elem.find('a')['href']
    # TO DO: modify, so that relevant Indeed.co.uk domain is included within the link
    return link



## ================== FUNCTIONS FOR CWJOBS.CO.UK =================== ##
    

def initiate_driver(location_of_driver, browser):
    if browser == 'chrome':
        driver = webdriver.Chrome(executable_path=(location_of_driver + "/chromedriver"))
#    elif browser == 'firefox':
#        driver = webdriver.Firefox(executable_path=location_of_driver)
#    elif browser == 'safari':
#        driver = webdriver.Safari(executable_path=location_of_driver)
#    elif browser == '
#        driver = webdriver.Edge(executable_path=location_of_driver)
    return driver

def make_job_search(job_title, location, driver):
    driver.get('https://www.cwjobs.co.uk/')
    
    # Select the job box
    job_title_box = driver.find_element_by_name('Keywords')

    # Send job information
    job_title_box.send_keys(job_title)

    # Selection location box
    location_box = driver.find_element_by_id('location')
    
    # Send location information
    location_box.send_keys(location)
    
    # Find Search button
    search_button = driver.find_element_by_id('search-button')
    search_button.click()

    driver.implicitly_wait(5)

    page_source = driver.page_source
    
    job_soup = BeautifulSoup(page_source, "html.parser")
    
    return job_soup


def extract_job_information_cwjobs(job_soup, desired_characs):
    
    job_elems = job_soup.find_all('div', class_="job")
     
    cols = []
    extracted_info = []
    
    if 'titles' in desired_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_cwjobs(job_elem))
        extracted_info.append(titles) 
                           
    
    if 'companies' in desired_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_cwjobs(job_elem))
        extracted_info.append(companies)
    
    # TO DO: links
    
    
    jobs_list = {}
    
    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]
    
    num_listings = len(extracted_info[0])
    
    return jobs_list, num_listings


def extract_job_title_cwjobs(job_elem):
    title_elem = job_elem.find('h2')
    title = title_elem.text.strip()
    return title

 
def extract_company_cwjobs(job_elem):
    company_elem = job_elem.find('h3')
    company = company_elem.text.strip()
    return company