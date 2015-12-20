from sys import argv
import os
import getpass
import time
import re
import csv
from collections import deque

from credentials import *
from header import *
from scrapers import *

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

script, outfile = argv

delay = 10
pause = 2

def get_last_row(csv_filename):
	with open(csv_filename, 'rb') as f:
		return deque(csv.reader(f), 1)[0]

def get_continuing(outfile):
	continuing = False

	if os.stat(outfile).st_size > 0:
		with open(outfile, 'r') as data:
			data_reader = csv.reader(data, delimiter=',', quotechar='"')
			# making sure the csv isn't just a header row
			entries = 0

			for row in data:
				entries += 1
				if entries > 1:
					break

			if entries > 1:
				return True
	else:
		write_header(outfile)

def write_header(outfile):
	with open(outfile, 'a') as data:
		writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(header)

def get_subject_list(subjects, continuing, last_subject):
	subject_list = []

	for subject in subjects:
		subject_list.append(subject.get_attribute('value'))

	# gets rid of the first select value, which is an empty entry
	subject_list.pop(0)

	if continuing:
		while subject_list[0] != last_subject:
			subject_list.pop(0)

	return subject_list

def get_course_list(subject_courses, continuing, last_course):
	subject_courses_list = []
	last_row_found = False

	for subject_course in subject_courses:
		current_course = subject_course.find_element_by_css_selector('.PSEDITBOX_DISPONLY').text

		if continuing:
			if last_course == current_course:
				last_row_found = True
		if not continuing or last_row_found:
			subject_courses_list.append(subject_course.get_attribute('id'))

	return subject_courses_list

def get_ctecs_list(ctecs, continuing, last_ctec, last_term, current_subject):
	last_ctec_found = False
	ctecs_list = []

	for ctec in ctecs:
		current_term = ctec.find_elements_by_tag_name('td')[0].text
		current_ctec = ctec.find_elements_by_tag_name('td')[1].text

		if not continuing or last_ctec_found:
			if current_subject in current_ctec:
				ctecs_list.append(ctec.get_attribute('id'))

		if continuing:
			if last_ctec == current_ctec.replace(":", "") and last_term == current_term:
				last_ctec_found = True
				continuing = False

	return ctecs_list

def main():
	timeouts = 0

	try:
		driver = webdriver.Firefox()
		driver.get('http://www.northwestern.edu/caesar/')

		wait = WebDriverWait(driver, delay)

		print "Logging into Caesar"

		# logging in to caesar
		netid_input = driver.find_element_by_css_selector('#loginInputBoxID')
		netid_input.send_keys(netid)

		password_input = driver.find_element_by_css_selector('#loginInputBoxPwd')
		password_input.send_keys(password)

		login_form = driver.find_element_by_css_selector('#login')
		login_form.submit()

		print "Navigating to CTECs"

		# clicking on "search CTECs"
		wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'EOPP_SCSECTIONCONTENTLINK')))

		search_ctecs = driver.find_element_by_css_selector('.EOPP_SCSECTIONCONTENTLINK')
		search_ctecs.click()

		# selecting the iframe with the CTEC search
		wait.until(EC.presence_of_element_located((By.ID, 'ptifrmtgtframe')))
		driver.switch_to.frame(driver.find_element_by_css_selector("#ptifrmtgtframe"))

		current_career = "UGRD"

		continuing = get_continuing(outfile)
		if continuing:
			with open(outfile, 'rb') as csv_file:
				last_row = get_last_row(outfile)
				last_career = last_row[0]
				last_subject = last_row[1]
				last_course = last_row[2]
				last_term = "{} {}".format(last_row[4], last_row[3])
				last_ctec = "{} {}-{}-{} {}".format(last_row[5], last_row[7], last_row[8], last_row[9], last_row[10]).replace(":", "")

			print "Picking up where we left off: {} {}".format(last_term, last_ctec)

			current_career = last_career
		else:
			last_row = None
			last_career = None
			last_subject = None
			last_course = None
			last_term = None
			last_ctec = None

		print "Filtering by {} courses".format(current_career)

		# selecting undergrad courses
		# for some reason sometimes it can't find the academic career dropdown
		try:
			academic_career = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_ACAD_CAREER')
		except NoSuchElementException:
			time.sleep(pause)
			academic_career = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_ACAD_CAREER')

		Select(academic_career).select_by_value(current_career)

		# locating subject selection
		wait.until(EC.presence_of_element_located((By.ID, 'NW_CT_PB_SRCH_SUBJECT')))
		time.sleep(delay)

		print "Grabbing all subject areas (this may take a few seconds)"

		academic_subjects = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_SUBJECT')
		subjects = academic_subjects.find_elements_by_tag_name('option')
		subject_list = get_subject_list(subjects, continuing, last_subject)

		current_subject = ""

		search_preferences = driver.find_element_by_css_selector("[id^='NW_CT_PB_SRCH_NW_CTEC_SRCH_CHOIC']")
		search_preferences.click()

		# this doesn't work for selecting subjects for some reason and i would like to know why
		# will select subject for a split second, then disappears
		# for subject in subject_list:
			# wait.until(EC.presence_of_element_located((By.XPATH, '//option[@value=subject]')))
			# subject_select = Select(academic_subjects)
			# subject_select.select_by_value(subject)

		for subject in subject_list:
			# a very jank way to get the driver to iterate over each subject.
			time.sleep(pause)

			academic_subjects = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_SUBJECT')
			subject_select = Select(academic_subjects)
			subject_select.select_by_value(subject)

			time.sleep(pause)

			search_button = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_SRCH_BTN')
			search_button.click()

			print "Looking at {} courses".format(subject)
			current_subject = subject

			time.sleep(pause)

			subject_courses_table = driver.find_element_by_css_selector("[id^='NW_CT_PV_DRV']")
			subject_courses = subject_courses_table.find_elements_by_css_selector('[id^="trNW_CT_PV_DRV"]')
			subject_courses_list = get_course_list(subject_courses, continuing, last_course)

			for subject_course_row in subject_courses_list:
				time.sleep(pause)

				subject_course = driver.find_element_by_id(subject_course_row)

				course_search_title = subject_course.find_element_by_css_selector('.PSEDITBOX_DISPONLY').text
				print "\t{}".format(course_search_title)

				time.sleep(pause)

				ctecs_list_link = subject_course.find_element_by_tag_name('a')
				ctecs_list_link.click()

				time.sleep(pause)

				ctecs_table = driver.find_element_by_css_selector("[id^='NW_CT_PV4_DRV']")
				ctecs = ctecs_table.find_elements_by_css_selector('[id^="trNW_CT_PV4_DRV"]')

				ctecs_list = get_ctecs_list(ctecs, continuing, last_ctec, last_term, current_subject)

				continuing = False

				for ctec_id in ctecs_list:
					while True:
						try:
							time.sleep(pause)

							# this doesn't work for some reason
							# ctec_id_xpath = '//tr[@id="{}")]'.format(ctec_id)
							# wait.until(EC.presence_of_element_located((By.XPATH, ctec_id_xpath)))

							try:
								ctec_row = driver.find_element_by_id(ctec_id)
							except NoSuchElementException:
								time.sleep(pause)
								ctec_row = driver.find_element_by_id(ctec_id)

							ctec_info = ctec_row.find_elements_by_css_selector('.PSEDITBOX_DISPONLY')
							print "\t\t{}: {}".format(ctec_info[0].text, ctec_info[1].text.encode('ascii','ignore'))

							ctec_link = ctec_row.find_element_by_tag_name('a')
							ctec_link.click()

							wait.until(EC.presence_of_element_located((By.ID, 'NW_CT_PV_NAME_RETURN_PB')))

							#
							# BEGIN ACTUAL DATA SCRAPING
							#

							search_career = current_career
							search_subject = subject
							search_course = course_search_title

							course_vitals = driver.find_elements_by_css_selector('.PSEDITBOX_DISPONLY')
							vitals_list = scrape_course_vitals(course_vitals)

							# Core Questions
							core_questions_table = driver.find_element_by_xpath('//table[contains(@id, "ACE_NW_CTEC_M_QUESTION")]')
							core_questions = core_questions_table.find_elements_by_tag_name('table')

							# initialize all responses to null in case there are no multiple choice questions
							# previously for i in range(len(core_questions) - 1)
							for i in range (0, 5):
								question_ratings = scrape_core_questions(core_questions, i)

								if i == 0:
									instruction_rating = question_ratings
								elif i == 1:
									course_rating = question_ratings
								elif i == 2:
									learned_rating = question_ratings
								elif i == 3:
									challenging_rating = question_ratings
								elif i == 4:
									stimulating_rating = question_ratings

							# Estimate the average number of hours per week you spent on this course outside of course and lab time
							try:
								time_survey_section = core_questions[5]
							except IndexError:
								time_survey_section = False

							time_rating = scrape_time_survey(time_survey_section)

							try:
								essay_section = driver.find_element_by_xpath('//table[contains(@id, "ACE_NW_CTEC_COMMENTS")]')
								essay_responses = essay_section.find_element_by_tag_name('p').text.encode('utf-8')
								essay_responses = re.search(r'(\n\n).*', essay_responses).group(0).strip().replace('"', "'")
							except NoSuchElementException:
								essay_responses = ""

							# Demographic Questions
							demographic_questions_table = driver.find_element_by_xpath('//div[contains(@id, "win0divNW_CT_PVS_DRV_DESCRLONG")]').find_element_by_tag_name('table')
							demographic_questions = demographic_questions_table.find_elements_by_tag_name('table')

							try:
								school_survey = scrape_school_survey(demographic_questions[0])
							except IndexError:
								school_survey = scrape_school_survey()

							try:
								class_survey = scrape_class_survey(demographic_questions[1])
							except IndexError:
								class_survey = scrape_class_survey()

							try:
								reason_survey = scrape_reason_survey(demographic_questions[0])
							except IndexError:
								reason_survey = scrape_reason_survey()

							try:
								interest_survey = scrape_interest_survey(demographic_questions[0])
							except IndexError:
								interest_survey = scrape_interest_survey()	

							#
							# END ACTUAL DATA SCRAPING
							#

							with open(outfile, 'a') as data:

								line = [
									search_career,
									search_subject,
									search_course
								]

								compiled_ratings = [
									vitals_list,
									instruction_rating,
									course_rating,
									learned_rating,
									challenging_rating,
									stimulating_rating,
									time_rating,
									school_survey,
									class_survey,
									reason_survey,
									interest_survey
								]

								for rating in compiled_ratings:
									for response in rating:
										line.append(response)

								line.append(essay_responses)

								writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
								writer.writerow(line)

							return_button = driver.find_element_by_css_selector('#NW_CT_PV_NAME_RETURN_PB')
							return_button.click()

							time.sleep(pause)

							academic_career = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_ACAD_CAREER')
							Select(academic_career).select_by_value(current_career)

							time.sleep(pause)

							academic_subjects = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_SUBJECT')
							subject_select = Select(academic_subjects).select_by_value(subject)

							time.sleep(pause)

							search_button = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_SRCH_BTN')
							search_button.click()

							time.sleep(pause)

							subject_course = driver.find_element_by_id(subject_course_row)

							ctecs_list_link = subject_course.find_element_by_tag_name('a')
							ctecs_list_link.click()

							break

						except TimeoutException:
							timeouts += 1

							if timeouts > 9:
								print "Hm. Something's not working. Let's try again."
								driver.quit()
								main()

							time.sleep(pause)
							print "\t\t\tOops! A little hiccup. Trying again {} more times...".format(10 - timeouts)
							pass

		print "That's all folks!"
		driver.quit()
	except NoSuchElementException:
		print "Oops! I couldn't find something. Restarting..."
		driver.quit()
		main()
	except TimeoutException:
		print "Oops! That's taking a little long to load. Restarting..."
		driver.quit()
		main()
	except StaleElementReferenceException:
		print "Oops! Something went wrong. Restarting..."
		driver.quit()
		main()


main()
