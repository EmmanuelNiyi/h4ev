from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from onadata.services import get_form_submissions, get_user_forms


class GetFormsByUsernameView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):

        try:
            data, status_code = get_user_forms(username)

            if status_code == 200:
                if len(data) == 0:
                    return Response(f"error: no forms found for user {username}")
                return Response(data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching forms: {e}")
            return Response(
                {"error": "Failed to fetch forms"},
                status=status.HTTP_502_BAD_GATEWAY
            )


class GetFormSubmissionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, form_id):
        try:
            data = get_form_submissions(form_id)

            if not data:
                return Response(
                    {"error": f"No submissions found for form {form_id}"},
                    status=status.HTTP_404_NOT_FOUND
                )

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
