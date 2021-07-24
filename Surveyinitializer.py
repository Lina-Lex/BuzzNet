from Question import Question
from Survey import Survey
import json


class SurveyInitializer():
    def __init__(self):
        with open('survey.json') as survey_file:
            survey_json_string = survey_file.read()
            self.survey = self.survey_from_json(survey_json_string)
            self.questions = self.questions_from_json(survey_json_string)

    def survey_from_json(self, survey_json_string):
        survey_dict = json.loads(survey_json_string)
        survey = Survey(title=survey_dict['title'])
        survey.questions = self.questions_from_json(survey_json_string)
        return survey

    def questions_from_json(self, survey_json_string):
        questions = []
        questions_dicts = json.loads(survey_json_string).get('questions')
        for question_dict in questions_dicts:
            id = question_dict['id']
            body = question_dict['body']
            type = question_dict['type']
            questions.append(Question(id=id, body=body, type=type))
        return questions