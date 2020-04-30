#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:35:04 2020

@author: chrislovejoy
"""


import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd

def find_jobs_from(website, job_title, location, desired_characs):
    # other to include: date, output_type, listed_since
    
    
    if website == 'Indeed':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_information(job_soup, desired_characs)
    
    save_jobs_to_excel(jobs_list)
 
    print('{} new job postings retrieved. Stored in "results.xls".'.format(num_listings))
    

def load_indeed_jobs_div(job_title, location):
    getVars = {'q' : job_title, 'l' : location}
    url = ('https://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup

def extract_job_information(job_soup, desired_characs):
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

def save_jobs_to_excel(jobs_list):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel("results.xls") #TODO: allow user to specify this name


def load_CVjobs_via_selenium(job_title, location):
    return None
    # TODO
    