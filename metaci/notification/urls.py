from django.conf.urls import url

from metaci.notification import views


urlpatterns = [
    url(
        r'^$',
        views.my_notifications,
        name='my_notifications',
    ),
    url(
        r'^add/repository',
        views.AddRepositoryNotification.as_view(),
        name='add_repository_notification',
    ),
    url(
        r'^add/branch',
        views.AddBranchNotification.as_view(),
        name='add_branch_notification',
    ),
    url(
        r'^add/planrepository',
        views.AddPlanRepositoryNotification.as_view(),
        name='add_planrepository_notification',
    ),
    url(
        r'^add/plan',
        views.AddPlanNotification.as_view(),
        name='add_plan_notification',
    ),
    url(
        r'^delete/branch/(?P<pk>\d+)$',
        views.delete_branch_notification,
        name='delete_branch_notification',
    ),
    url(
        r'^delete/plan/(?P<pk>\d+)$',
        views.delete_plan_notification,
        name='delete_plan_notification',
    ),
    url(
        r'^delete/planrepository/(?P<pk>\d+)$',
        views.delete_planrepository_notification,
        name='delete_planrepository_notification',
    ),
    url(
        r'^delete/repository/(?P<pk>\d+)$',
        views.delete_repository_notification,
        name='delete_repository_notification',
    ),
]
