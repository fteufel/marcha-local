from django.urls import path, include
from . import views

urlpatterns = [
        #path('polls/', include('polls.urls')),
        #path('admin/', admin.site.urls),
        

        path('<int:question_id>/', views.detail, name = 'detail'),
        path('<int:question_id>/results', views.results, name = 'results'),
        path('', views.index, name = 'index'),
        ]
