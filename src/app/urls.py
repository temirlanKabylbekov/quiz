from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from rest_framework import routers

from accounts.api.views import WhoAmIView
from app.views import LoginRequiredTemplateView
from questions.api.views import QuestionListViewset

router = routers.SimpleRouter()
router.register('question_list', QuestionListViewset)


api_v1 = (
    path('whoami/', WhoAmIView.as_view()),
    path('', include(router.urls)),
)

urlpatterns = [
    path('api/v1/', include((api_v1, 'api'), namespace='v1')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html')),
    re_path(r'.*', LoginRequiredTemplateView.as_view(template_name='frontend/index.html')),  # route all other stuff to the frontend
]
