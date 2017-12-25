from django.conf.urls import url
from token_server import views

urlpatterns = [
    url(r'^login/$', views.auth_and_login, name='auth_and_login'),
    url(r'^logout/$', views.auth_and_login, name='auth_and_login'),
    url(r'^index/$', views.index_view, name='index_view,'),
    url(r'^token_detail/(?P<pk>\d+)/$', views.token_detail, name='token_detail'),
    url(r'^token/add/(?P<pk_type>\d+)/$', views.token_add, name='token_add'),
    url(r'^api/token/binding/$', views.token_binding, name='token_binding'),
    url(r'^api/token/validate/$', views.token_validation, name='token_validation')
]