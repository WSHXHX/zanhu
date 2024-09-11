from django.urls import path

from zanhu.qa import views

app_name = "qa"

urlpatterns = [
    path("", view=views.UnansweredQuestionListView.as_view(), name="unanswered_q"),
    path("answered/", view=views.AnsweredQuestionListView.as_view(), name="answered_q"),
    path("indexed/", view=views.QuestionListView.as_view(), name="all_q"),
    path("ask-question/", view=views.CreateQuestionView.as_view(), name="ask_question"),
    path("question-detail/<int:pk>/", view=views.DetailQuestionView.as_view(), name="question_detail"),
    path("propose-answer/<int:question_id>/", view=views.CreateAnswerView.as_view(), name="propose_answer"),
    path("question/vote/", view=views.question_vote, name="question_vote"),
    path("answer/vote/", view=views.answer_vote, name="answer_vote"),
    path("accept-answer/", view=views.accept_answer, name="accept_answer"),
]
