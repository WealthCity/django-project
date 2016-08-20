import logging

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import password_reset
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import exceptions, parsers, status
from rest_framework import views
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from client.models import Client
from support.models import SupportRequest
from user.autologout import SessionExpire
from user.models import SecurityAnswer, SecurityQuestion
from . import serializers
from ..user.serializers import ChangePasswordSerializer, \
    ResetPasswordSerializer, SecurityAnswerCheckSerializer, \
    SecurityAnswerSerializer, SecurityQuestionSerializer

logger = logging.getLogger('api.v1.user.views')
from .serializers import EmailNotificationsSerializer, \
    UserAdvisorSerializer, UserClientSerializer
from ..permissions import IsClient
from ..views import ApiViewMixin, BaseApiView



class MeView(BaseApiView):
    serializer_class = serializers.UserSerializer

    def get(self, request):
        """
        ---
        # Swagger

        response_serializer: serializers.UserSerializer
        """
        user = SupportRequest.target_user(request)
        if user.is_support_staff:
            sr = SupportRequest.get_current(self.request, as_obj=True)
            user = sr.user
        data = self.serializer_class(user).data
        if user.is_advisor:
            role = 'advisor'
            data.update(UserAdvisorSerializer(user.advisor).data)
        elif user.is_client:
            role = 'client'
            data.update(UserClientSerializer(user.client).data)
        else:
            raise PermissionDenied("User is not in the client or "
                                   "advisor groups.")
        data.update({'role': role})
        return Response(data)

    @transaction.atomic
    def post(self, request):
        """
        ---
        # Swagger

        request_serializer: serializers.UserUpdateSerializer
        response_serializer: serializers.UserSerializer
        """
        user = SupportRequest.target_user(request)
        serializer = serializers.UserUpdateSerializer(user, data=request.data,
                                                      partial=True,
                                                      context={
                                                          'request': request,
                                                      })

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        serializer = self.serializer_class(user)
        return Response(serializer.data)


class LoginView(BaseApiView):
    """
    Signin andvisors or any other type of users
    """
    authentication_classes = ()
    throttle_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSerializer
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,
    )

    def post(self, request):
        """
        ---
        # Swagger

        request_serializer: serializers.AuthSerializer
        response_serializer: serializers.UserSerializer

        responseMessages:
            - code: 400
              message: Unable to log in with provided credentials
        """
        auth_serializer = serializers.AuthSerializer(data=request.data)

        auth_serializer.is_valid(raise_exception=True)
        user = auth_serializer.validated_data['user']

        # check if user is authenticated
        if not user.is_authenticated():
            raise exceptions.NotAuthenticated()

        # initiate internal routine to login this user
        login(request, user)

        serializer = self.serializer_class(user)
        return Response(serializer.data)


class RegisterView(BaseApiView):
    pass


class ResetView(BaseApiView):
    def post(self, request):
        serializer = serializers.ResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # set password
        user.set_password(serializer.validated_data['password'])
        user.save()

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetEmailView(BaseApiView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.ResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_active:
            # send password
            pass
            return Response(status=status.HTTP_200_OK)
        return Response('User is blocked', status=status.HTTP_403_FORBIDDEN)


class KeepAliveView(BaseApiView):
    def get(self, request):
        SessionExpire(request).keep_alive()
        return Response('ok', status=status.HTTP_200_OK)


class EmailNotificationsView(ApiViewMixin, RetrieveUpdateAPIView):
    permission_classes = IsClient,
    serializer_class = EmailNotificationsSerializer

    def get_object(self):
        return Client.objects.get(user=self.request.user).notification_prefs


class PasswordResetView(ApiViewMixin, views.APIView):
    """
    accepts post with email field
    resets password and then
    sends reset password email to matching user account
    """
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer
    post_reset_redirect = '/password/reset/done/'

    # eventually just remove this
    def get(self, request):
        return password_reset(request,
                              self.post_reset_redirect,
                              template_name='registration/password_reset.html')

    def post(self, request):
        serializer = serializers.ResetPasswordSerializer(data=request.data)
        protocol = 'https' if request.is_secure else 'http'
        if serializer.is_valid():
            logger.info('Resetting password for user %s' % serializer.validated_data['email'])
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            for user in serializer.get_users(serializer.validated_data['email']):
                ctx = {
                    'email': user.email,
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': protocol,
                }
                serializer.send_mail(
                    subject_template_name='registration/password_reset_subject.txt',
                    email_template_name='registration/password_reset_email.html',
                    from_email=settings.SUPPORT_EMAIL,
                    to_email=user.email,
                    context=ctx,
                )
            return Response('ok', status=status.HTTP_200_OK)

        logger.error('Unauthorized login attempt using email %s' % serializer.data['email'])
        return Response('unauthorized', status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(ApiViewMixin, views.APIView):
    """
    allows logged in users to change their password
    receives old password, new password, and security question answer
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        # camelCase to snake_case
        if 'oldPassword' in request.data:
            request.data['old_password'] = request.data['oldPassword']
            request.data.pop('oldPassword', None)
        if 'newPassword' in request.data:
            request.data['new_password'] = request.data['newPassword']
            request.data.pop('newPassword', None)

        serializer = serializers.ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            logger.info('Changing password for user %s' % request.user.email)
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response('ok', status=status.HTTP_200_OK)
        logger.error('Unauthorized change password attempt from user %s' % request.user.email)
        return Response('unauthorized', status=status.HTTP_401_UNAUTHORIZED)


class SecurityQuestionListView(ApiViewMixin, ListAPIView):
    """
    A read only list view.  Receives get request, returns
    a list of the canned security questions.  Allows anyone
    access.
    """
    queryset = SecurityQuestion.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SecurityQuestionSerializer

    def get(self, request):
        # return set of canned security questions
        queryset = self.get_queryset()
        serializer = serializers.SecurityQuestionSerializer(queryset, many=True)
        return Response(serializer.data)


class SecurityQuestionAnswerView(ApiViewMixin, views.APIView):
    """
    allows a logged in user to set a new security question and answer
    and allow a logged user to retriev their current security question
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SecurityAnswerSerializer

    def get(self, request):
        # get the user's current security question
        try:
            sa = SecurityAnswer.objects.get(user=request.user)
        except:
            logger.error('Security question not found for %s' % request.user.email)
            return Response('Not found', status=status.HTTP_404_NOT_FOUND)
        data = {
            'question': sa.question
        }
        serializer = serializers.SecurityUserQuestionSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            logger.info('Valid request to retrieve current security question for %s' % request.user.email)
            return Response(serializer.validated_data)
        logger.error('Unauthorized request to retrieve security question for %s' % request.user.email)
        return Response('unauthorized', status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        # set new security question and answer combination
        serializer = serializers.SecurityAnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            logger.info('Valid request to set new security question and answer for %s' % request.user.email)
            sa, created = SecurityAnswer.objects.get_or_create(user=request.user)
            sa.question = serializer.validated_data['question']
            sa.set_answer(serializer.validated_data['answer'])
            sa.save()
            return Response('ok', status=status.HTTP_200_OK)
        logger.error('Unauthorized attempt to set new security question and answer for %s' % request.user.email)
        return Response('unauthorized', status=status.HTTP_401_UNAUTHORIZED)


class SecurityAnswerCheckView(ApiViewMixin, views.APIView):
    """
    allows authenticated request to check an answer is correct
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SecurityAnswerCheckSerializer

    def post(self, request):
        serializer = serializers.SecurityAnswerCheckSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            logger.info('Valid request to set check security answer for %s' % request.user.email)
            return Response('ok', status=status.HTTP_200_OK)
        logger.error('Unauthorized attempt to check answer for %s' % request.user.email)
        return Response('unauthorized', status=status.HTTP_401_UNAUTHORIZED)
