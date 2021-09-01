from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chacu.py', views.about, name='about'),
    path('nosotros', views.us, name='us'),
    path('ranking', views.ranking, name='ranking'),
    path('contacto', views.contact, name='contact'),
    path('charts', views.chart_report, name='charts'),
    path('data', views.pivot_data, name='pivot_data'),
    path('panel', views.admin_panel, name='panel'),
    path('panel/trivia/configuracion', views.trivia_config, name='trivia_config'),
    path('panel/trivia/preguntas', views.trivia_questions, name='trivia_questions'),
    path(
        'panel/trivia/preguntas/<int:question_id>',
        views.trivia_question_edit,
        name='trivia_questions_edit'
    ),
    path('panel/trivia/opciones', views.trivia_options, name='trivia_options'),
    path(
        'panel/trivia/opciones/<int:option_id>',
        views.trivia_option_edit,
        name='trivia_options_edit'
    ),
]
