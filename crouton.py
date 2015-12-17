from sys import argv
import os
import getpass
import time
import re
import csv
from collections import deque

from credentials import *

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

script, outfile = argv

delay = 10
pause = 1

def get_last_row(csv_filename):
    with open(csv_filename, 'rb') as f:
        return deque(csv.reader(f), 1)[0]

def main():
	driver = webdriver.Firefox()
	driver.get('http://www.northwestern.edu/caesar/')
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

	wait = WebDriverWait(driver, delay)

	current_career = "UGRD"

 	continuing = False

	if os.stat(outfile).st_size > 0:
		continuing = True

		with open(outfile, 'rb') as csv_file:
			last_row = get_last_row(outfile)
			last_career = last_row[0]
			last_subject = last_row[1]
			last_course = last_row[2]
			last_term = "{} {}".format(last_row[4], last_row[3])
			last_ctec = "{} {}-{}-{} {}".format(last_row[5], last_row[7], last_row[8], last_row[9], last_row[10])

		print "Picking up where we left off: {} {}".format(last_term, last_ctec)

	if not continuing:
		with open(outfile, 'a') as data:
			writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(
				[
					"search_career",
					"search_subject",
					"search_course",
					"academic_quarter",
					"academic_year",
					"academic_subject_code",
					"academic_subject_full",
					"course_number",
					"course_subnum",
					"course_section",
					"course_name",
					"instructor",
					"enrollment_count",
					"response_count",
					"instruction_rating_response",
					"instruction_rating_average",
					"instruction_rating_of_one_by_percent",
					"instruction_rating_of_two_by_percent",
					"instruction_rating_of_three_by_percent",
					"instruction_rating_of_four_by_percent",
					"instruction_rating_of_five_by_percent",
					"instruction_rating_of_six_by_percent",
					"course_rating_response",
					"course_rating_average",
					"course_rating_of_one_by_percent",
					"course_rating_of_two_by_percent",
					"course_rating_of_three_by_percent",
					"course_rating_of_four_by_percent",
					"course_rating_of_five_by_percent",
					"course_rating_of_six_by_percent",
					"learned_rating_response",
					"learned_rating_average",
					"learned_rating_of_one_by_percent",
					"learned_rating_of_two_by_percent",
					"learned_rating_of_three_by_percent",
					"learned_rating_of_four_by_percent",
					"learned_rating_of_five_by_percent",
					"learned_rating_of_six_by_percent",
					"challenging_rating_response",
					"challenging_rating_average",
					"challenging_rating_of_one_by_percent",
					"challenging_rating_of_two_by_percent",
					"challenging_rating_of_three_by_percent",
					"challenging_rating_of_four_by_percent",
					"challenging_rating_of_five_by_percent",
					"challenging_rating_of_six_by_percent",
					"stimulating_rating_response",
					"stimulating_rating_average",
					"stimulating_rating_of_one_by_percent",
					"stimulating_rating_of_two_by_percent",
					"stimulating_rating_of_three_by_percent",
					"stimulating_rating_of_four_by_percent",
					"stimulating_rating_of_five_by_percent",
					"stimulating_rating_of_six_by_percent",
					"time_rating_response",
					"time_rating_of_less_than_three",
					"time_rating_of_four_to_seven",
					"time_rating_of_eight_to_eleven",
					"time_rating_of_twelve_to_fifteen",
					"time_rating_of_sixteen_to_nineteen",
					"time_rating_of_more_than_twenty",
					"school_survey_sesp",
					"school_survey_comm",
					"school_survey_grad",
					"school_survey_kgsm",
					"school_survey_mccormick",
					"school_survey_medill",
					"school_survey_music",
					"school_survey_summer",
					"school_survey_scs",
					"school_survey_wcas",
					"school_survey_response",
					"class_survey_freshman",
					"class_survey_sophomore",
					"class_survey_junior",
					"class_survey_senior",
					"class_survey_grad",
					"class_survey_other",
					"class_survey_response",
					"reason_survey_distro",
					"reason_survey_major",
					"reason_survey_minor",
					"reason_survey_elective",
					"reason_survey_other",
					"reason_survey_none",
					"reason_survey_response",
					"interest_survey_rating_of_one",
					"interest_survey_rating_of_two",
					"interest_survey_rating_of_three",
					"interest_survey_rating_of_four",
					"interest_survey_rating_of_five",
					"interest_survey_rating_of_six",
					"interest_survey_rating_of_one",
					"interest_survey_response",
					"interest_survey_average",
					"essay_responses"
				]
			)


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

	if continuing:
		current_career = last_career

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

	subject_list = []

	for subject in subjects:
		subject_list.append(subject.get_attribute('value'))
		# print subject.get_attribute('value')

	# gets rid of the first select value, which is an empty entry
	subject_list.pop(0)

	if continuing:
		while subject_list[0] != last_subject:
			subject_list.pop(0)

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

		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')

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

		subject_courses_list = []

		last_row_found = False

		for subject_course in subject_courses:
			current_course = subject_course.find_element_by_css_selector('.PSEDITBOX_DISPONLY').text

			if continuing:
				if last_course == current_course:
					last_row_found = True
			if not continuing or last_row_found:
				subject_courses_list.append(subject_course.get_attribute('id'))

		for subject_course_row in subject_courses_list:
			time.sleep(pause)

			subject_course = driver.find_element_by_id(subject_course_row)

			course_search_title = subject_course.find_element_by_css_selector('.PSEDITBOX_DISPONLY').text
			print "\t{}".format(course_search_title)

			time.sleep(pause)

			ctecs_list_link = subject_course.find_element_by_tag_name('a')
			ctecs_list_link.click()

			time.sleep(pause)

			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			ctecs_table = driver.find_element_by_css_selector("[id^='NW_CT_PV4_DRV']")
			ctecs = ctecs_table.find_elements_by_css_selector('[id^="trNW_CT_PV4_DRV"]')

			ctecs_list = []

			last_ctec_found = False

			for ctec in ctecs:
				current_term = ctec.find_elements_by_tag_name('td')[0].text
				current_ctec = ctec.find_elements_by_tag_name('td')[1].text

				if not continuing or last_ctec_found:
					ctecs_list.append(ctec.get_attribute('id'))

				if continuing:
					if last_ctec == current_ctec and last_term == current_term:
						last_ctec_found = True
						continuing = False

			for ctec_id in ctecs_list:
				while True:
					try:
						time.sleep(pause)

						# this doesn't work for some reason
						# ctec_id_xpath = '//tr[@id="{}")]'.format(ctec_id)
						# wait.until(EC.presence_of_element_located((By.XPATH, ctec_id_xpath)))

						ctec_row = driver.find_element_by_id(ctec_id)

						ctec_term = ctec_row.find_elements_by_css_selector('.PSEDITBOX_DISPONLY')
						print "\t\t{}: {}".format(ctec_term[0].text, ctec_term[1].text)

						ctec_link = ctec_row.find_element_by_tag_name('a')
						ctec_link.click()

						wait.until(EC.presence_of_element_located((By.ID, 'NW_CT_PV_NAME_RETURN_PB')))

						#
						# BEGIN ACTUAL DATA SCRAPING
						#

						# will change this to include all careers
						search_career = "UGRD"
						search_subject = subject
						search_course = course_search_title

						course_vitals = driver.find_elements_by_css_selector('.PSEDITBOX_DISPONLY')

						# # e.g. Fall 2010
						academic_term = course_vitals[0].text
						academic_quarter = academic_term.split(' ')[0]
						academic_year = academic_term.split(' ')[1]

						# # e.g. HEBREW Hebrew
						academic_subject = course_vitals[1].text
						academic_subject_code = re.match(r'\S*', academic_subject).group(0)
						academic_subject_full = re.search(r'\s.*', academic_subject).group().strip()

						# # e.g. 111-2-20 Hebrew I
						course_title = course_vitals[2].text
						course_full_number = re.match(r'\S*', course_title).group(0).split('-')
						course_number = course_full_number[0]
						course_subnum = course_full_number[1]
						course_section = course_full_number[2]
						course_name = re.search(r'\s(.*)', course_title).group().strip()

						# e.g. Sarah Silverman
						instructor = course_vitals[3].text

						# number of peple who took the course
						enrollment_count = int(course_vitals[4].text)

						# number of people who filled out the CTEC
						response_count = int(course_vitals[5].text)

						# Core Questions
						core_questions_table = driver.find_element_by_xpath('//table[contains(@id, "ACE_NW_CTEC_M_QUESTION")]')
						core_questions = core_questions_table.find_elements_by_tag_name('table')

						for i in range(len(core_questions) - 1):
							question_sections = core_questions[i].find_elements_by_tag_name('tr')

							question_rating_response_average = question_sections[0].find_elements_by_tag_name('td')

							try:
								question_rating_response = int(re.match(r'\S*', question_rating_response_average[1].find_element_by_tag_name('font').text).group(0))
								question_rating_average = float(re.search(r'\s(\d*\.?\d*)$', question_rating_response_average[1].find_element_by_tag_name('font').text).group(0).strip())

								question_rating_numbers_section = question_sections[1].find_element_by_tag_name('td')
								question_rating_numbers = question_rating_numbers_section.find_elements_by_xpath('*')[1].find_elements_by_tag_name('div')

								question_rating_of_six_by_percent = float(question_rating_numbers[0].text[:-1]) / 100
								question_rating_of_five_by_percent = float(question_rating_numbers[1].text[:-1]) / 100
								question_rating_of_four_by_percent = float(question_rating_numbers[2].text[:-1]) / 100
								question_rating_of_three_by_percent = float(question_rating_numbers[3].text[:-1]) / 100
								question_rating_of_two_by_percent = float(question_rating_numbers[4].text[:-1]) / 100
								question_rating_of_one_by_percent = float(question_rating_numbers[5].text[:-1]) / 100
							except ValueError:
								# no response
								question_rating_of_six_by_percent = "null"
								question_rating_of_five_by_percent = "null"
								question_rating_of_four_by_percent = "null"
								question_rating_of_three_by_percent = "null"
								question_rating_of_two_by_percent = "null"
								question_rating_of_one_by_percent = "null"

							question_ratings = [
								question_rating_response,
								question_rating_average,
								question_rating_of_one_by_percent,
								question_rating_of_two_by_percent,
								question_rating_of_three_by_percent,
								question_rating_of_four_by_percent,
								question_rating_of_five_by_percent,
								question_rating_of_six_by_percent
							]

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
						time_survey = core_questions[5].find_element_by_tag_name('tr').find_elements_by_tag_name('td')
						time_survey_ratings = time_survey[0].find_elements_by_xpath('*')[1].find_elements_by_tag_name('div')
						time_rating_of_less_than_three = float(time_survey_ratings[0].text[:-1]) / 100
						time_rating_of_four_to_seven = float(time_survey_ratings[1].text[:-1]) / 100
						time_rating_of_eight_to_eleven = float(time_survey_ratings[2].text[:-1]) / 100
						time_rating_of_twelve_to_fifteen = float(time_survey_ratings[3].text[:-1]) / 100
						time_rating_of_sixteen_to_nineteen = float(time_survey_ratings[4].text[:-1]) / 100
						time_rating_of_more_than_twenty = float(time_survey_ratings[5].text[:-1]) / 100
						time_rating_response = int(re.match(r'\S*', time_survey[1].find_element_by_tag_name('font').text).group(0))

						time_rating = [
							time_rating_response,
							time_rating_of_less_than_three,
							time_rating_of_four_to_seven,
							time_rating_of_eight_to_eleven,
							time_rating_of_twelve_to_fifteen,
							time_rating_of_sixteen_to_nineteen,
							time_rating_of_more_than_twenty
						]

						essay_section = driver.find_element_by_xpath('//table[contains(@id, "ACE_NW_CTEC_COMMENTS")]')
						essay_responses = essay_section.find_element_by_tag_name('p').text.encode('utf-8')

						# Demographic Questions
						demographic_questions_table = driver.find_element_by_xpath('//div[contains(@id, "win0divNW_CT_PVS_DRV_DESCRLONG")]').find_element_by_tag_name('table')
						demographic_questions = demographic_questions_table.find_elements_by_css_selector('div > div > table > tbody > tr > td')

						for i in range(len(demographic_questions)):
							survey = demographic_questions[i].find_elements_by_tag_name('tr')
							demographic_responses = []

							for j in range(1, len(survey)):
								try:
									val = int(survey[j].find_elements_by_tag_name('td')[1].text)
								except ValueError as e:
									val = float(survey[j].find_elements_by_tag_name('td')[1].text)

								demographic_responses.append(val)

							if i == 0:
								school_survey = demographic_responses
							elif i == 1:
								class_survey = demographic_responses
							elif i == 2:
								reason_survey = demographic_responses
							elif i == 3:
								interest_survey = demographic_responses

						#
						# END ACTUAL DATA SCRAPING
						#

						with open(outfile, 'a') as data:

							compiled_ratings = [
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

							line = [
								search_career,
								search_subject,
								search_course,
								academic_quarter,
								academic_year,
								academic_subject_code,
								academic_subject_full,
								course_number,
								course_subnum,
								course_section,
								course_name,
								instructor,
								enrollment_count,
								response_count
							]

							for rating in compiled_ratings:
								for response in rating:
									line.append(response)

							line.append(re.search(r'(\n\n).*', essay_responses).group(0).strip().replace('"', "'"))

							writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							writer.writerow(line)

						return_button = driver.find_element_by_css_selector('#NW_CT_PV_NAME_RETURN_PB')
						return_button.click()

						time.sleep(pause)

						academic_subjects = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_SUBJECT')

						subject_select = Select(academic_subjects)
						subject_select.select_by_value(subject)

						time.sleep(pause)

						search_button = driver.find_element_by_css_selector('#NW_CT_PB_SRCH_SRCH_BTN')
						search_button.click()

						time.sleep(pause)

						subject_course = driver.find_element_by_id(subject_course_row)

						ctecs_list_link = subject_course.find_element_by_tag_name('a')
						ctecs_list_link.click()

						break

					except TimeoutException:
						time.sleep(pause)
						print "\t\t\tOops! A little hiccup"
						pass

	driver.quit()

main()
