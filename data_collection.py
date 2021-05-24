# -*- coding: utf-8 -*-
"""
Created on Thu May 20 16:48:31 2021

@author: Nikunj Gada - https://www.linkedin.com/in/nikunj-gada
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
import logging

# # Get the logger specified in the file
logger = logging.getLogger(__name__)

def get_jobs(url, num_jobs, verbose, driverPath, sleepTime):
    try : 
        '''Gathers jobs as a dataframe, scraped from Glassdoor'''
        start = round(time.time())
        
        logger.info("Inside get_jobs method")
        #Initializing the webdriver
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path=driverPath, options=options)
        driver.set_window_size(1120, 1000)
    
        #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + keyword + '&locT=N&locId=115&llocName=India&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
        #url = 'https://www.glassdoor.com/Job/india-data-scientist-jobs-SRCH_IL.0,5_IN115_KO6,20.htm?minSalary=52000&includeNoSalaryJobs=false&maxSalary=1008000'
        driver.get(url)
        
        #Initialize empty list of jobs
        jobs = []
    
        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(sleepTime)
    
        # Once the website is loaded it is clicked anywhere to get started
        try:
            driver.find_element_by_css_selector('[class="react-job-listing css-7x0jr eigr9kq3"').click()
            time.sleep(0.5)
            logger.debug('Website open and Ready for scrapping')
    
        except ElementClickInterceptedException:
            logger.exception('ElementClickInterceptedException - Failed to get website ready for scraping')
            logger.info('Time taken for method get_jobs() is ',(time.time() - start))
            return pd.DataFrame(jobs)
        except NoSuchElementException:
            logger.exception('ElementClickInterceptedException - Failed to get website ready for scraping')
            logger.info('Time taken for method get_jobs() is ',(time.time() - start))
            return pd.DataFrame(jobs)
        except Exception:
            logger.debug("Failure in first click, retrying 1 time ")
            try :
                driver.find_element_by_css_selector('[class="react-job-listing css-7x0jr eigr9kq3"').click()
                time.sleep(0.5)
            except :
                logger.exception("Retry Failed for clicking anywhere on the website")
                logger.info('Time taken for method get_jobs() is ',(time.time() - start))
                return pd.DataFrame(jobs)
    
        time.sleep(.1)
        
        #Test for the "Sign Up" prompt and get rid of it.
        try:
            #clicking to the X.
            driver.find_element_by_css_selector('[alt="Close"').click()
            time.sleep(0.5)
            logger.info('X clicked - Sign-in skipped')
        except NoSuchElementException:
            logger.exception('Failed to click on X and skip sign-in')
            logger.info('Time taken for method get_jobs() is ',(time.time() - start))
            return pd.DataFrame(jobs)
    
        while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
    
            #A click on the right grid
            # When the page changes it is necessary we click on the grid
            try: 
                driver.find_element_by_css_selector('[class="react-job-listing css-7x0jr eigr9kq3"').click()
                time.sleep(0.5)
            except NoSuchElementException :
                pass
            except Exception:
                logger.debug("Failure in first click, retrying 1 time ")
                try :
                    driver.find_element_by_css_selector('[class="react-job-listing css-7x0jr eigr9kq3"').click()
                    time.sleep(0.5)
                except :
                    logger.exception("Retry Failed for clicking anywhere on the website")
                    logger.info('Time taken for method get_jobs() is ',(time.time() - start))
                    return pd.DataFrame(jobs)
            
            #Going through each job in this page
            #job_buttons = driver.find_elements_by_class_name("jobLink")        #jl for Job Listing. These are the buttons we're going to click.
            job_buttons = [el for el in driver.find_elements_by_xpath('.//ul[@data-test="jlGrid"]/li')]
                            
            #print("job_buttons : ",job_buttons)
            for job_button in job_buttons:
                
                #initilize variables to NA
                #You need to set a "not found value. It's important."
                salary_estimate = -1
                rating = -1
                founded = -1
                size = -1
                industry = -1
                type_of_ownership = -1
                sector = -1
                revenue = -1
                url = -1
                
                company_name = -1
                location = -1
                job_title = -1
                job_description = -1
                job_type = -1
                competitors = -1
                headquarters = -1
                recommendJob = -1
    
                logger.info("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
                if len(jobs) >= num_jobs:
                    break
                
                #Clicking on JobList
                try:
                    job_button.click()
                except Exception:
                    logger.debug('Job Click Failed, Retrying 1 time : ')
                    try :
                        job_button.click()
                    except Exception :
                        logger.exception('Retry failed : Job ClicK ')
                        pass
                    logger.debug('Retry success : Job Click')
                    pass
                
                collected_successfully = False
                           
                company_name, location, job_title, job_description, job_type, salary_estimate, rating = fetchData(driver, collected_successfully, company_name, location, job_title, job_description, job_type, salary_estimate, rating)
                                    
                #Printing for debugging
                if verbose:
                    print("Job Title: {}".format(job_title))
                    print("Job Type: {}".format(job_type))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))
    
                #Going to the Company tab...
                #clicking on this:
                #<div class="tab" data-tab-type="overview"><span>Company</span></div>
                try:
                    #Clicking on Company Tab
                    #driver.find_element_by_xpath('.//div[@data-item="tab" and @data-tab-type="overview"]').click()
                    try:
                        driver.find_element_by_xpath('.//div[@data-tab-type="overview"]').click()
                        time.sleep(0.5)
                    except Exception :
                        logger.debug('Company Click Failed, retry 1 time')
                        try :
                            driver.find_element_by_xpath('.//div[@data-tab-type="overview"]').click()
                            time.sleep(0.5)
                        except Exception :
                            logger.debug('Retry failed : 1 : Company ClicKed Failed, Retry 2 initiated')
                            try :
                                driver.find_element_by_xpath('.//div[@data-tab-type="overview"]').click()
                                time.sleep(0.5)
                            except Exception :
                                logger.exception('Retry failed : 2 : Company ClicKed Failed')
                                pass
                            pass
                        logger.debug('Retry success : Company Click')
                        pass
                                                      
                    # Grid for all info of the company
                    tableRange = len(driver.find_elements_by_xpath('.//div[@id="EmpBasicInfo"]/div[1]/div/div'))
                    company_url = (driver.find_elements_by_xpath('//*[@id="EmpBasicInfo"]/div[2]/div/a')[0]).get_attribute('href')                
                except Exception as e:
                        logger.error('Failed to fetch company url or table Range : ',e)
                        pass
                    
                for i in range(1,tableRange+1):
                    query = './/div[@id="EmpBasicInfo"]/div[1]/div/div[' + str(i) + ']/span'
                    overview = driver.find_elements_by_xpath(query)
                                    
                    if len(overview) == 0:
                        pass
                        #print("Do Nothing")
                    else :
                        try:                       
                            if((overview[0].text).lower() == 'size'):
                                size = overview[1].text
                            elif((overview[0].text).lower() == 'revenue'):
                                revenue = overview[1].text
                            elif((overview[0].text).lower() == 'founded'):
                                founded = overview[1].text
                            elif((overview[0].text).lower() == 'industry'):
                                industry = overview[1].text
                            elif((overview[0].text).lower() == 'type'):
                                type_of_ownership = overview[1].text
                            elif((overview[0].text).lower() == 'sector'):
                                sector = overview[1].text
                            elif((overview[0].text).lower() == 'revenue'):
                                revenue = overview[1].text
                                                        
                        except Exception as e:
                            logger.error('Error in If block : ',e)
                            pass
                                   
                    #Rarely, some job postings do not have the tab.
                    try:
                        #<div class="infoEntity">
                        #    <label>Headquarters</label>
                        #    <span class="value">San Francisco, CA</span>
                        #</div>
                        headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                        competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                    
                    except Exception :
                        #print('NoSuchElementException : ',e)
                        pass
                # Fetching Company overall Ratings  
                try:
                    driver.find_element_by_xpath('.//div[@data-tab-type="rating"]').click()
                    time.sleep(0.5)
                    recommendJob = (driver.find_elements_by_xpath('.//div[@id="employerStats"]/div[2]/div[1]/div[1]')[0]).text
                except Exception :
                    logger.debug('Rating click Failed, retry 1 time')
                    try :
                        driver.find_element_by_xpath('.//div[@data-tab-type="rating"]').click()
                        time.sleep(0.5)
                        recommendJob = (driver.find_elements_by_xpath('.//div[@id="employerStats"]/div[2]/div[1]/div[1]')[0]).text
                    except Exception :
                        logger.debug('Retry fail : Rating ClicKed Failed : ')
                        pass
                    pass
                    
                if verbose:
                    logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    logger.info("Company: {}".format(company_name))
                    logger.info("Headquarters: {}".format(headquarters))
                    logger.info("Size: {}".format(size))
                    logger.info("Founded: {}".format(founded))
                    logger.info("Type of Ownership: {}".format(type_of_ownership))
                    logger.info("Industry: {}".format(industry))
                    logger.info("Sector: {}".format(sector))
                    logger.info("Revenue: {}".format(revenue))
                    logger.info("Competitors: {}".format(competitors))
                    logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    
                jobs.append({"Job Title" : job_title,
                "Job Type" : job_type,
                "Salary Estimate" : salary_estimate,
                "Job Description" : job_description,
                "Rating" : rating,
                "Company Name" : company_name,
                "Location" : location,
                "Headquarters" : headquarters,
                "Size" : size,
                "Founded" : founded,
                "Type of ownership" : type_of_ownership,
                "Industry" : industry,
                "Sector" : sector,
                "Revenue" : revenue,
                "Company URL" : company_url,
                "Recommend Job" : recommendJob})
                #add job to jobs
    
            #Clicking on the "next page" button
            try:
                #pagination-next
                driver.find_element_by_xpath('//li/a[contains(@data-test,"pagination-next")]').click()
                time.sleep(.1)
            except Exception :
                logger.exception("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
                break
    
        logger.info('Time taken for method get_jobs() is ',(time.time() - start))
        return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
    except : 
        logger.info('Time taken for method get_jobs() is ',(time.time() - start))
        return pd.DataFrame(jobs)

def fetchData(driver, collected_successfully, company_name, location, job_title, job_description, job_type, salary_estimate, rating):
     while not collected_successfully:
        try:
            # company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
            # location = driver.find_element_by_xpath('.//div[@class="location"]').text
            # job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
            # job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
            # collected_successfully = True
            
            #Collectig all information
            company_name = driver.find_element_by_xpath('.//div[contains(@class , "css-87uc0g e1tk4kwz1")]').text
            location = driver.find_element_by_xpath('.//div[contains(@class , "css-56kyx5 e1tk4kwz5")]').text
            job_title = driver.find_element_by_xpath('.//div[contains(@class , "css-1vg6q84 e1tk4kwz4")]').text
            job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
            job_type = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[3]/div[2]/div[1]').text
            salary_estimate = driver.find_element_by_xpath('.//span[contains(@class,"css-56kyx5 css-16kxj2j e1wijj242")]').text
            rating = driver.find_element_by_xpath('.//span[@data-test="detailRating"]').text
            
            collected_successfully = True
            
        except Exception :
            logger.debug('Cannot find xPath, Retry agin')
            try:              
                try:
                    company_name = driver.find_element_by_xpath('.//div[contains(@class , "css-87uc0g e1tk4kwz1")]').text                
                except Exception :
                    logger.debug('Cannot find xPath for company_name')
                    try:
                        company_name = driver.find_element_by_xpath('.//div[contains(@class , "css-87uc0g e1tk4kwz1")]').text
                    except :
                        logger.debug('Cannot find xPath for company_name after retry')
                        #marking that read was successful to avoid infinite loop
                        collected_successfully = True
                        pass
                    pass
                
                try:
                    location = driver.find_element_by_xpath('.//div[contains(@class , "css-56kyx5 e1tk4kwz5")]').text
                except Exception :
                    logger.debug('Cannot find xPath for location')
                    try: 
                        location = driver.find_element_by_xpath('.//div[contains(@class , "css-56kyx5 e1tk4kwz5")]').text
                    except :
                        logger.debug('Cannot find xPath for location after retry')
                        collected_successfully = True
                        pass
                    pass
                
                try :
                    job_title = driver.find_element_by_xpath('.//div[contains(@class , "css-1vg6q84 e1tk4kwz4")]').text
                except Exception :
                    logger.debug('Cannot find xPath for job_title')
                    try: 
                        job_title = driver.find_element_by_xpath('.//div[contains(@class , "css-1vg6q84 e1tk4kwz4")]').text
                    except :
                        logger.debug('Cannot find xPath for job_title after retry')
                        collected_successfully = True
                        pass
                    pass
                
                try :
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                except Exception :
                    logger.debug('Cannot find xPath for job_description')
                    try: 
                        job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    except :
                        logger.debug('Cannot find xPath for job_description after retry')
                        collected_successfully = True
                        pass
                    pass
                
                try :
                    salary_estimate = driver.find_element_by_xpath('.//span[contains(@class,"css-56kyx5 css-16kxj2j e1wijj242")]').text
                except Exception :
                    logger.debug('Cannot find xPath for salary_estimate')
                    try: 
                        salary_estimate = driver.find_element_by_xpath('.//span[contains(@class,"css-56kyx5 css-16kxj2j e1wijj242")]').text
                    except :
                        logger.debug('Cannot find xPath for salary_estimate after retry')
                        collected_successfully = True
                        pass
                    pass
                
                try :
                    rating = driver.find_element_by_xpath('.//span[@data-test="detailRating"]').text
                except Exception :
                    logger.debug('Cannot find xPath for rating')
                    try: 
                        rating = driver.find_element_by_xpath('.//span[@data-test="detailRating"]').text
                    except :
                        logger.debug('Cannot find xPath for rating after retry')
                        collected_successfully = True
                        pass
                    pass
                
                try :
                    job_type = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[3]/div[2]/div[1]').text
                except Exception :
                    logger.debug('Cannot find xPath for job_type')
                    try: 
                        job_type = driver.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[3]/div[2]/div[1]').text
                    except :
                        logger.debug('Cannot find xPath for job_type after retry')
                        collected_successfully = True
                        pass
                    pass
            except :
                collected_successfully = True
                pass
        return company_name, location, job_title, job_description, job_type, salary_estimate, rating