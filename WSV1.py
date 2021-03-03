#Import libraries
import requests
import pandas as pd
import bs4
from bs4 import BeautifulSoup

#First two components of URL String for Indeed scraping
URL_P1 = "https://www.indeed.com/jobs?q="
URL_p2 = "&l="

##This starts the program by asking the user for basic information
print("Welcome to the Indeed Job web scraper!")
USER_JOB_TITLES = input("Please enter the job title: ")
USER_JOB_CITY = input('Please enter the city you want to search: ')
print("Looking for " + USER_JOB_TITLES + " jobs in " + USER_JOB_CITY + " ...")

#Piece the URL together using user input and other Indeed URL specifics.
user_search = URL_P1 + USER_JOB_TITLES + URL_p2 + USER_JOB_CITY

#conducting a request of the stated URL above:
page = requests.get(user_search)

#specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
first_search_soup = BeautifulSoup(page.text, "html.parser")



"""Gets the job title for each posting"""
def get_job_title(theSoup):
    allJobs = []
    for div in theSoup.find_all(name = "div", attrs = {"class":"row"}):
        for a in div.find_all(name = "a", attrs = {"data-tn-element": "jobTitle"}):
            allJobs.append(a["title"])
    allJobs = allJobs[:10]
    return(allJobs)


"""Gets the company name for each posting -- some required removal of white space"""
def get_company_name(theSoup): 
    names = []
    for div in theSoup.find_all(name = "div", attrs = {"class":"row"}):
        company = div.find_all(name = "span", attrs = {"class":"company"})
        if len(company) > 0:
            for ws in company:
                names.append(ws.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in sec_try:
                names.append(span.text.strip())
    names = names[:10]
    return(names)


"""Gets the location for each posting"""
def get_job_location(theSoup): 
    geo = []
    span_tags = theSoup.findAll("span", attrs = {"class" : "location"})
    for span in span_tags:
        geo.append(span.text)
    geo = geo[:10]
    return(geo)


#This section prints the initial 10 jobs postings per the user's input.
yes_no = True
step = 0

job_PD = pd.DataFrame({'Job Title' : get_job_title(first_search_soup),
                       'City' : get_job_location(first_search_soup),
                       'Company' : get_company_name(first_search_soup)
                        })
print(job_PD)
next_input = input("Would you like to view the next page of jobs? (Y/N): ")


#Per the users second input, this section will retrieve n pages of jobs, it will continue until we run out of postings...
#or until the program encounters some sort of error.
while (next_input == 'Y'):
    step += 10
    next_search = user_search + '&start=' + str(step)
    next_page = requests.get(next_search)
    next_search_soup = BeautifulSoup(next_page.text, "html.parser")
    next_job_PD = pd.DataFrame({'Job Title' : get_job_title(next_search_soup),
                       'City' : get_job_location(next_search_soup),
                       'Company' : get_company_name(next_search_soup)
                        })
    print(next_job_PD)
    print('')
    next_input = input("Would you like to view the next page of jobs? (Y/N): ")
    print('')
print('Goodbye!')
    