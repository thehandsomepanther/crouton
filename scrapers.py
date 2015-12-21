import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def scrape_course_vitals(course_vitals):
	# # e.g. Fall 2010
	academic_term = course_vitals[0].text.split(' ')
	academic_quarter = academic_term[0]
	academic_year = academic_term[1]

	# # e.g. HEBREW Hebrew
	academic_subject = course_vitals[1].text
	academic_subject_code = re.match(r'\S*', academic_subject).group(0)
	academic_subject_full = re.search(r'\s.*', academic_subject).group().strip()

	# # e.g. 111-2-20 Hebrew I
	course_title = course_vitals[2].text.encode('utf-8')
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

	return [
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

def scrape_core_questions(core_questions, i):
	question_rating_response = "null"
	question_rating_average = "null"
	question_rating_of_six_by_percent = "null"
	question_rating_of_five_by_percent = "null"
	question_rating_of_four_by_percent = "null"
	question_rating_of_three_by_percent = "null"
	question_rating_of_two_by_percent = "null"
	question_rating_of_one_by_percent = "null"

	try:
		question_sections = core_questions[i].find_elements_by_tag_name('tr')
		question_rating_response_average = question_sections[0].find_elements_by_tag_name('td')

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
		pass
	except NoSuchElementException:
		pass
	except IndexError:
		pass

	return [
		question_rating_response,
		question_rating_average,
		question_rating_of_one_by_percent,
		question_rating_of_two_by_percent,
		question_rating_of_three_by_percent,
		question_rating_of_four_by_percent,
		question_rating_of_five_by_percent,
		question_rating_of_six_by_percent
	]

def scrape_time_survey(time_survey_section):
	time_rating_of_less_than_three = "null"
	time_rating_of_four_to_seven = "null"
	time_rating_of_eight_to_eleven = "null"
	time_rating_of_twelve_to_fifteen = "null"
	time_rating_of_sixteen_to_nineteen = "null"
	time_rating_of_more_than_twenty = "null"
	time_rating_response = "null"

	if time_survey_section is not False:
		try:
			time_survey = time_survey_section.find_element_by_tag_name('tr').find_elements_by_tag_name('td')
			time_survey_ratings = time_survey[0].find_elements_by_xpath('*')[1].find_elements_by_tag_name('div')
			time_rating_of_less_than_three = float(time_survey_ratings[0].text[:-1]) / 100
			time_rating_of_four_to_seven = float(time_survey_ratings[1].text[:-1]) / 100
			time_rating_of_eight_to_eleven = float(time_survey_ratings[2].text[:-1]) / 100
			time_rating_of_twelve_to_fifteen = float(time_survey_ratings[3].text[:-1]) / 100
			time_rating_of_sixteen_to_nineteen = float(time_survey_ratings[4].text[:-1]) / 100
			time_rating_of_more_than_twenty = float(time_survey_ratings[5].text[:-1]) / 100
			time_rating_response = int(re.match(r'\S*', time_survey[1].find_element_by_tag_name('font').text).group(0))
		except IndexError:
			pass

	return [
		time_rating_response,
		time_rating_of_less_than_three,
		time_rating_of_four_to_seven,
		time_rating_of_eight_to_eleven,
		time_rating_of_twelve_to_fifteen,
		time_rating_of_sixteen_to_nineteen,
		time_rating_of_more_than_twenty
	]

def scrape_school_survey(school_survey_section = False):
	school_survey_sesp = "null"
	school_survey_comm = "null"
	school_survey_grad = "null"
	school_survey_kgsm = "null"
	school_survey_mccormick = "null"
	school_survey_medill = "null"
	school_survey_music = "null"
	school_survey_summer = "null"
	school_survey_scs = "null"
	school_survey_wcas = "null"
	school_survey_response = "null"

	if school_survey_section is not False:
		survey = school_survey_section.find_elements_by_tag_name('tr')

		for i in range(1, len(survey)):
			try:
				val = int(survey[i].find_elements_by_tag_name('td')[1].text)
			except ValueError as e:
				val = float(survey[i].find_elements_by_tag_name('td')[1].text)

			school = survey[i].find_elements_by_tag_name('td')[0].text

			if "Education & SP" in school:
				school_survey_sesp = val
			elif "Communication" in school:
				school_survey_comm = val
			elif "Graduate School" in school:
				school_survey_grad = val
			elif "KGSM" in school:
				school_survey_kgsm = val
			elif "McCormick" in school:
				school_survey_mccormick = val
			elif "Medill" in school:
				school_survey_medill = val
			elif "Music" in school:
				school_survey_music = val
			elif "Summer" in school:
				school_survey_summer = val
			elif "SCS" in school:
				school_survey_scs = val
			elif "WCAS" in school:
				school_survey_wcas = val
			elif "Total Response" in school:
				school_survey_response = val

	return [
		school_survey_sesp,
		school_survey_comm,
		school_survey_grad,
		school_survey_kgsm,
		school_survey_mccormick,
		school_survey_medill,
		school_survey_music,
		school_survey_summer,
		school_survey_scs,
		school_survey_wcas,
		school_survey_response
	]

def scrape_class_survey(class_survey_section = False):
	class_survey_freshman = "null"
	class_survey_sophomore = "null"
	class_survey_junior = "null"
	class_survey_senior = "null"
	class_survey_grad = "null"
	class_survey_other = "null"
	class_survey_response = "null"

	if class_survey_section is not False:

		survey = class_survey_section.find_elements_by_tag_name('tr')

		for i in range(1, len(survey)):
			try:
				val = int(survey[i].find_elements_by_tag_name('td')[1].text)
			except ValueError as e:
				val = float(survey[i].find_elements_by_tag_name('td')[1].text)

			class_response = survey[i].find_elements_by_tag_name('td')[0].text

			if "Freshman" in class_response:
				class_survey_freshman = val
			elif "Sophomore" in class_response:
				class_survey_sophomore = val
			elif "Junior" in class_response:
				class_survey_junior = val
			elif "Senior" in class_response:
				class_survey_senior = val
			elif "Graduate" in class_response:
				class_survey_grad = val
			elif "Other" in class_response:
				class_survey_other = val
			elif "Total Response" in class_response:
				class_survey_response = val

	return [
		class_survey_freshman,
		class_survey_sophomore,
		class_survey_junior,
		class_survey_senior,
		class_survey_grad,
		class_survey_other,
		class_survey_response
	]

def scrape_reason_survey(reason_survey_section = False):
	reason_survey_distro = "null"
	reason_survey_major = "null"
	reason_survey_minor = "null"
	reason_survey_elective = "null"
	reason_survey_other = "null"
	reason_survey_none = "null"
	reason_survey_response = "null"

	if reason_survey_section is not False:

		survey = reason_survey_section.find_elements_by_tag_name('tr')

		for i in range(1, len(survey)):
			try:
				val = int(survey[i].find_elements_by_tag_name('td')[1].text)
			except ValueError as e:
				val = float(survey[i].find_elements_by_tag_name('td')[1].text)

			reason = survey[i].find_elements_by_tag_name('td')[0].text

			if "Distribution" in reason:
				reason_survey_distro = val
			elif "Major" in reason:
				reason_survey_major = val
			elif "Minor" in reason:
				reason_survey_minor = val
			elif "Elective" in reason:
				reason_survey_elective = val
			elif "Other" in reason:
				reason_survey_other = val
			elif "No" in reason:
				reason_survey_none = val
			elif "Total Response" in reason:
				reason_survey_response = val

	return [
		reason_survey_distro,
		reason_survey_major,
		reason_survey_minor,
		reason_survey_elective,
		reason_survey_other,
		reason_survey_none,
		reason_survey_response
	]

def scrape_interest_survey(interest_survey_section = False):
	interest_survey_rating_of_one = "null"
	interest_survey_rating_of_two = "null"
	interest_survey_rating_of_three = "null"
	interest_survey_rating_of_four = "null"
	interest_survey_rating_of_five = "null"
	interest_survey_rating_of_six = "null"
	interest_survey_response = "null"
	interest_survey_average = "null"

	if interest_survey_section is not False:

		survey = interest_survey_section.find_elements_by_tag_name('tr')

		for i in range(1, len(survey)):
			try:
				val = int(survey[i].find_elements_by_tag_name('td')[1].text)
			except ValueError as e:
				val = float(survey[i].find_elements_by_tag_name('td')[1].text)

			interest = survey[i].find_elements_by_tag_name('td')[0].text

			if "1" in interest:
				interest_survey_rating_of_one = val
			elif "2" in interest:
				interest_survey_rating_of_two = val
			elif "3" in interest:
				interest_survey_rating_of_three = val
			elif "4" in interest:
				interest_survey_rating_of_four = val
			elif "5" in interest:
				interest_survey_rating_of_five = val
			elif "6" in interest:
				interest_survey_rating_of_six = val
			elif "Total Response" in interest:
				interest_survey_response = val
			elif "Average Response" in interest:
				interest_survey_average = val

	return [
		interest_survey_rating_of_one,
		interest_survey_rating_of_two,
		interest_survey_rating_of_three,
		interest_survey_rating_of_four,
		interest_survey_rating_of_five,
		interest_survey_rating_of_six,
		interest_survey_response,
		interest_survey_average
	]
