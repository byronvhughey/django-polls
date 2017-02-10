# https://docs.djangoproject.com/en/1.10/intro/tutorial05/

import datetime
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase

from .models import Question

def create_question(question_text, days):
	"""
	Creates a question with the given 'question_text' and published the
	given number of 'days' offset to now (negative for questions published
	in the past, positive for questions that have yet to be published).
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		"""
		If no questions exist, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_a_past_question(self):
		"""
		Questions with a pub_date in the past should be displayed
		on the index page.
		"""
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_index_view_with_a_future_question(self):
		"""
		Questions with a pub_date in the future should not be 
		displayed on the index page.
		"""
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_future_question_and_past_question(self):
		"""
		Even if both past and future questions exist, only past
		questions should be displayed.
		"""
		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_index_view_with_two_past_question(self):
		"""
		The questions index page may display multiple questions.
		"""
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response - self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question 2.>', '<Question: Past question 1.>']
		)

class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
		"""
		The detail view of a question with a pub_date in the future
		should return a 404 not found.
		"""
		future_question = create_question(question_text="Future question.", days=5)
		url = reverse('polls:detail', args=(future_question.id,))
		response - self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_question(self):
		"""
		The detail view of a question with a pub-date in the past
		should display the question's text.
		"""
		past_question = create_question(question_text="Past Question.", days=-5)
		url = reverse('polls:detail', args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)

"""
We ought to add a similar get_queryset method to ResultsView and 
create a new test class for that view. It’ll be very similar to 
what we have just created; in fact there will be a lot of repetition.

We could also improve our application in other ways, adding tests 
along the way. For example, it’s silly that Questions can be 
published on the site that have no Choices. So, our views could 
check for this, and exclude such Questions. Our tests would create 
a Question without Choices and then test that it’s not published, 
as well as create a similar Question with Choices, and test that 
it is published.

Perhaps logged-in admin users should be allowed to see unpublished 
Questions, but not ordinary visitors. Again: whatever needs to be 
added to the software to accomplish this should be accompanied by 
a test, whether you write the test first and then make the code 
pass the test, or work out the logic in your code first and then 
write a test to prove it.

Good rules of thumb for tests:

- a separate TestClass for each model or view
- a separate test method (def(params)) for each set of conditions you want to test
- test method names that describe their function 
"""









