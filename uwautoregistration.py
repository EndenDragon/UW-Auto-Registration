from config import config
from selenium import webdriver
import datetime
import json
import requests
import time

_registrationURL = "https://sdb.admin.uw.edu/students/uwnetid/register.asp"
_notifyuwAPI = "https://notify.uw.edu/uiapi/channel_search/"

slnListPosition = 0 # Position in the list that the sln works

driver = webdriver.PhantomJS()

def login(url, username, password):
    global driver
    driver.get(url)
    netid_field = driver.find_element_by_id("weblogin_netid")
    password_field = driver.find_element_by_id("weblogin_password")
    netid_field.clear()
    password_field.clear()
    netid_field.send_keys(username)
    password_field.send_keys(password)
    password_field.submit()

def register():
    global driver, slnListPositon
    slnsList = config['sln-list'][slnListPosition]
    slnBoxes = driver.find_elements_by_css_selector("input[name^='sln'][type=text]")
    slnList = slnsList.keys()
    for slnBox in slnBoxes:
        if slnList:
            sln = slnList.pop()
            slnBox.send_keys(sln)
            if slnsList[sln]:
                boxNum = slnBox.get_attribute('name')[3:]
                addCodeBox = driver.find_element_by_css_selector("input[name='entcode"+boxNum+"']")
                addCodeBox.send_keys(slnsList[sln])
    submitButton = driver.find_element_by_css_selector("input[type='submit'][value*='Update']")
    submitButton.click()

def checkRegistrationStatus():
    global slnListPosition, _notifyuwAPI
    time_now = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    print "=================================="
    print "Currently: " + time_now
    for slns in config['sln-list']:
        print ""
        print "Plan number " + str(slnListPosition + 1)
        slnList = slns.keys()
        for sln in slnList:
            payload = {'sln': sln, 'year': config['quarter-year'], 'quarter': config['quarter-name']}
            notifyJSON = requests.get(_notifyuwAPI, params=payload)
            notifyJSON = json.loads(notifyJSON.text)
            course_title = notifyJSON['course_title']
            course_sln = notifyJSON['SLN']
            course_curr_enroll = notifyJSON['current_enrollment']
            course_seats = notifyJSON['total_seats']
            print "*" + course_sln + " " + course_title + " " + course_curr_enroll + "/" + course_seats
            if course_curr_enroll >= course_seats:
                print "++++++ Course is filled up!, Switching to next plan, if possible. ++++++"
                slnListPositon = slnListPositon + 1
                break;
    if (slnListPosition + 1) > len(config['sln-list']):
        print "All plans are full... but the program will still check avalibility."
        slnListPosition = 0

def run():
    submit_time = date_object = datetime.datetime.strptime(config['registration-datetime'], '%b %d %Y %I:%M%p')
    now = datetime.datetime.now()
    time_now = time.time()
    last_checked_notifyuw_time = 0
    while now < submit_time:
        now = datetime.datetime.now()
        time_now = time.time()
        if time_now - last_checked_notifyuw_time > 30: # Check notify uw every 30 secs
            #checkRegistrationStatus() - not implemented yet, needs login func
            last_checked_notifyuw_time = time.time()
    print "It's time to submit registration!! ..processing"
    login(_registrationURL, config['netid-username'], config['netid-password'])
    register()
    driver.save_screenshot('registration_result.png')

if __name__ == "__main__":
    run()
