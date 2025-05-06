from django.core.cache import cache
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from accounts.services import LoggingAPIView, generate_cache_key
from onadata.services import get_form_submissions, get_user_forms


class GetFormsByUsernameView(LoggingAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):

        # Parameters to be considered for cache busting
        url_params = request.GET.dict()
        time_window = 60  # Cache busts every minute

        # Generate a dynamic cache key based on username, user, and request params
        cache_key = generate_cache_key(
            user=request.user,
            url_params=url_params,
            time_window=time_window
        )
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            data, status_code = get_user_forms(username)

            if status_code == 200:
                if len(data) == 0:
                    return Response(f"error: no forms found for user {username}")
                cache.set(cache_key, data, timeout=300)
                return Response(data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching forms: {e}")
            return Response(
                {"error": "Failed to fetch forms"},
                status=status.HTTP_502_BAD_GATEWAY
            )


class GetFormSubmissionsView(LoggingAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, form_id):

        # Parameters to be considered for cache busting
        url_params = request.GET.dict()
        time_window = 60  # Cache busts every minute

        # Generate a dynamic cache key based on username, user, and request params
        cache_key = generate_cache_key(
            user=request.user,
            url_params=url_params,
            time_window=time_window
        )
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            data = get_form_submissions(form_id)

            if not data:
                return Response(
                    {"error": f"No submissions found for form {form_id}"},
                    status=status.HTTP_404_NOT_FOUND
                )

            cache.set(cache_key, data, timeout=300) # clear redis in 5 minutes
            return Response(data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching form submissions: {e}")
            return Response(
                {
                    "error": "Failed to fetch form submissions",
                    "error_description": f"External API returned {str(e)}"
                },
                status=status.HTTP_502_BAD_GATEWAY
            )
