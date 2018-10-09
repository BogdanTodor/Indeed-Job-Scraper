import pandas as pd
import time
import requests
import bs4
from bs4 import BeautifulSoup

# Assign URL link
Keyword = input("Provide keyword/phrase for search: ")+"+&1="

URL = "https://au.indeed.com/jobs?q="+Keyword+"brisbane+QLD&radius=125"



# get request for link provided above
page = requests.get(URL)

#use soup and parse using html parser
pageContent = BeautifulSoup(page.text, "html.parser")

# print the html code in a more readable format
#print(pageContent.prettify())

# creates a txt file to store the html code from the webpage
WebPageFormat = open('WebPageFormat.txt','w', encoding = 'UTF-8')

# writes the formatted html code to the file created above
WebPageFormat.write(pageContent.prettify())

# Alternative would be to print it to the console for inspection, however
# due to ease of use, a separate, inspectable file seems more appropriate

def extract_job_name():
    jobs = []
    # searches for div tags with the attributes class and row
    for div_tag in pageContent.find_all(name="div", attrs={"class":"row"}):
        # searches through the selected div tags to find the a tag with attributes data-tn-element and job title
        for a_tag in div_tag.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a_tag["title"])
    print(jobs)
# extract_job_name()

def extract_company_name():
    companyName = []
    for div in pageContent.find_all(name="div", attrs={"class":"row"}):
        CoName = div.find_all(name="span", attrs={"class":"company"})
        if len(CoName) > 0:
            for i in CoName:
                companyName.append(i.text.strip())
        else:
            different_tags = div.find_all(name="span", attrs={"class":"result-link-source"})
            for j in different_tags:
                companyName.append(j.text.strip())

    print(companyName)
# extract_company_name()

# function to extract the job description of each relevant job
def extract_job_description():
    #create a list to store the description strings
    descriptions = []
    # loop through the job relevant div tags
    for div in pageContent.find_all(name="div", attrs={"class":"row"}):
        # append all job descriptions to the list 'descriptions'
        for span in div.find_all(name="span", attrs={"class":"summary"}):
            descriptions.append(span.text.strip())
    print(descriptions)

# extract_job_description()

## Create a data table and insert job information ##
columns = ["Job title", "Company", "Job description"]
job_table = pd.DataFrame(columns = columns)

for i in range(0,100, 10):
    # creates a url that changes pages based on the index variable i
    page = requests.get("https://au.indeed.com/jobs?q="+Keyword+"brisbane+QLD&radius=125"+"&start="+str(i))
    # add delay between page grabs
    time.sleep(1)
    pageContent = BeautifulSoup(page.text, 'lxml', from_encoding="UTF-8")
    for div_tag in pageContent.find_all(name="div", attrs={"class":"row"}):
        # determine size of data table
        num = (len(job_table)+1)
        job_ad = []
        # appending job name
        for a in div_tag.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            job_ad.append(a["title"])
        # appending company names
        Company_Names = div_tag.find_all(name="span", attrs={"class":"company"})
        if len(Company_Names) > 0:
            for companies in Company_Names:
                job_ad.append(companies.text.strip())
        else:
            Company_Names = div_tag.find_all(name="span", attrs={"class":"result-link-source"})
            for more_companies in Company_Names:
                job_ad.append(more_companies.text.strip())
        # appending job description
        for span in div_tag.find_all(name="span", attrs={"class":"summary"}):
            job_ad.append(span.text.strip())



        job_table.loc[num] = job_ad

print(job_table)
