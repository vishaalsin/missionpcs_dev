from django.conf.urls import url
from letsprepare import views
from yaksh.views import select_exam, initiate_dashboard
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^show_modules/$', views.show_all_modules, name="home"),
    url(r'^exam/$', views.show_all_quizzes, name='quizzes'),
    url(r'^results/$', views.show_results, name='results'),
    url(r'^buy/$', views.show_all_on_sale, name='buy'),
    url(r'^assign_quizzes/$', views.assign_quizzes, name='assign_quizzes'),
    url(r'^report_error/$', views.report_error, name='report_error'),
    url(r'^send_otp/$', views.send_otp, name='report_error'),
    url(r'^verify_payment/$', views.verify_payment, name='get_payment'),
    url(r'^test-series/$', TemplateView.as_view(template_name='portal_pages/test-series.html')),
    url(r'^tests/$', TemplateView.as_view(template_name='portal_pages/tests.html')),
    url(r'^select-exams/$', select_exam, name='select-exam'),
    url(r'^prev-tests/$', TemplateView.as_view(template_name='portal_pages/prev-tests.html')),
    url(r'^detailed-news/$', TemplateView.as_view(template_name='portal_pages/detailed-news.html')),
    url(r'^current-affairs/$', TemplateView.as_view(template_name='portal_pages/current-affairs.html')),
    url(r'^home/$', initiate_dashboard, name="Home"),
    url(r'^buy2/$', TemplateView.as_view(template_name='buy/all_on_sale.html')),
]