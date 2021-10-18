"""execbjj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls.conf import include


from members.views import index_page, dashboard_page, account_page, membership_page, register, MembershipSelectView, webhook, newsletter, beginners_course

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name="index_page"),
    path('register/', register, name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('dashboard/', dashboard_page, name="dashboard_page"),
    path('membership/', include('members.urls')),
    path('checkin/', include('checkins.urls')),
    path('account/', account_page, name="account_page"),
    path('webhook/', webhook, name='webhook'),
    path('newsletter/', newsletter, name='newsletter'),
    path('beginners-course/', beginners_course, name="beginners_course")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
