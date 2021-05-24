# -*- coding: utf-8 -*-
"""
Created on Thu May 20 16:48:31 2021

@author: Nikunj Gada - https://www.linkedin.com/in/nikunj-gada
"""
#Get necessary imports
import get_jobs as jobs
import logging
import logging.config
import os

# Load log configuration
logging.config.fileConfig(fname=os.getcwd()+'/log_config.ini', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

# Location of the driver
#Change the path to where chromedriver is in your home folder.
driver = os.getcwd() +'/chromedriver'

#Adjust if your internet is slow
sleepTime = int(0)

#number of records you want to fetch
numOfRecords = int(1600)

url = 'https://www.glassdoor.com/Job/india-data-scientist-jobs-SRCH_IL.0,5_IN115_KO6,20.htm?minSalary=52000&maxSalary=1008000&includeNoSalaryJobs=false'

logger.info('Fetching data')
df = jobs.get_jobs(url, numOfRecords, False, driver, sleepTime)

logger.info('data received. Creating csv file as gs_data.csv')
df.to_csv("gs_data.csv",index=False,header=True)
