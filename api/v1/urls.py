from django.conf.urls import patterns, include, url
from rest_framework import routers

from .user import views as user_views
from .goals import views as goals_views
# obsoleted # from .transactions import views as transactions_views


router = routers.SimpleRouter()
router.register(r'goals', goals_views.GoalViewSet, base_name='goals')


urlpatterns = patterns('',
    #url(r'^$', IndexView.as_view()), # swagger doesn't get it :/

    url(r'^me/$', user_views.MeView.as_view(), name='user-me'),
    # reserved # url(r'^me/image/$', me_views.MeImageView.as_view(), name='me-image'),
    url(r'^me/accounts/$', user_views.MeAccountsView.as_view(), name='me-accounts'),
    url(r'^me/goals/$', user_views.MeGoalsView.as_view(), name='me-goals'),

    url(r'^login/$', user_views.LoginView.as_view(), name='user-login'),
    # reserved # url(r'^register/$', user_views.RegisterView.as_view(), name='user-register'),

    # reserved # url(r'^register/reset/$', user_views.ResetView.as_view(), name='user-reset'),
    # reserved # url(r'^register/send-reset-email/$', user_views.SendResetEmailView.as_view(), name='user-send-reset-email'),

    # obsoleted # url(r'^goal-types/?$', goals_views.APIGoalTypes.as_view()), # revise
    # obsoleted # url(r'^goals/?$', goals_views.APIGoal.as_view()), # revise

    # obsoleted # url(r'^transactions/deposit/?$', transactions_views.APITransactionsDeposit.as_view()),
)

urlpatterns += router.urls