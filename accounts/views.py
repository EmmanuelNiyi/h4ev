import traceback

from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts import exceptions, services, serializers
from accounts.serializers import UserSerializer


User = get_user_model()


class CreateUserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

    # @extend_schema(
    #     examples=[
    #         OpenApiExample(
    #             "User Registration Example",
    #             description="An example of a user registration request",
    #             value={
    #                 "username": "user@gmail.com",
    #                 "password": "string",
    #                 "first_name": "firstname",
    #                 "last_name": "lastname",
    #                 "role": 2,
    #                 "referral_code": "",
    #             },
    #             request_only=True,  # only for request
    #         ),
    #         OpenApiExample(
    #             "Successful Registration Response",
    #             description="An example of a successful user registration response",
    #             value={
    #                 "id": 1,
    #                 "username": "user@gmail.com",
    #                 "first_name": "firstname",
    #                 "last_name": "lastname",
    #                 "role": 2,
    #             },
    #             response_only=True,  # only for response
    #         ),
    #     ]
    # )
    def post(self, request, *args, **kwargs):
        # Sanitize the input data
        # unsafe_input = request.data.copy()
        # safe_input = sanitization_utils.sanitize_dictionary(unsafe_input)

        # Validate the sanitized data using the serializer
        # serializer = UserSerializer(data=safe_input)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = services.create_user_account(
                    serializer
                )

                serialized_user = UserSerializer(user)

                # Return success response
                return Response(serialized_user.data, status=status.HTTP_201_CREATED)

            except exceptions.UserAlreadyExists as e:

                return Response(
                    {"error": f"User already exists: {e}"},
                    status=status.HTTP_409_CONFLICT,
                )
            except Exception as e:
                error_details = traceback.format_exc()  # Captures full traceback
                return Response(
                    {
                        "error": f"An error occurred: {str(e)}",
                        "details": error_details,  # Provides full traceback
                    },
                    status=500,
                )
        else:
            # Return validation errors if any
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # # Retrieve and sanitize username (email) and password from request data
        unsafe_username = request.data.get("email", "")
        unsafe_password = request.data.get("password", "")
        #
        # sanitized_username = sanitization_utils.strip_xss(unsafe_username)
        # sanitized_password = sanitization_utils.strip_xss(unsafe_password)

        # Authenticate user with sanitized data
        user = authenticate(username=unsafe_username, password=unsafe_password)

        if user is not None:
            if user.is_active:
                # If user is active, serialize the user data
                user_serializer = serializers.UserReadSerializer(user)

                # Generate JWT tokens using RefreshToken
                refresh = RefreshToken.for_user(user)

                # Prepare response data with tokens
                response_data = {
                    "user": user_serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # User is not active, return an appropriate error message
                return Response(
                    {"message": "account not active."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            # Authentication failed, return error message
            return Response(
                {"message": "wrong username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class GetAllUsersView(APIView):
    """Get all users view"""

    # logger.info("Retrieving all users")

    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=200)


# class RetrieveUpdateDeleteUserView(APIView):
#     serializer_class = accounts_serializers.UserResponseSerializer
#     permission_classes = [AllowAny]  # Modify to stricter permissions if necessary
#
#     def get(self, request, user_id):
#         """Retrieve a user by ID"""
#         logger.info(f"retrieving user {user_id} details")
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": f"user {user_id} not found"}, status=404)
#
#         serializer = accounts_serializers.UserResponseSerializer(user)
#         return Response(serializer.data, status=200)
#
#     def put(self, request, user_id):
#         """Update a user by id"""
#         logger.info(f"updating user {user_id} details")
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": f"user {user_id} not found"}, status=404)
#
#         # unsafe_user_id = request.data.get("unsafe_user_id", "")
#         unsafe_first_name = request.data.get("first_name", "")
#         unsafe_last_name = request.data.get("last_name", "")
#         unsafe_role_id = request.data.get("role", "")
#
#         # Sanitize the input data
#         # sanitized_user_id = sanitization_utils.strip_xss(unsafe_user_id)
#         sanitized_first_name = sanitization_utils.strip_xss(unsafe_first_name)
#         sanitized_last_name = sanitization_utils.strip_xss(unsafe_last_name)
#         sanitized_role_id = sanitization_utils.strip_xss(unsafe_role_id)
#
#         sanitized_data = {
#             # "id": sanitized_user_id,
#             "first_name": sanitized_first_name,
#             "last_name": sanitized_last_name,
#             "role": sanitized_role_id,
#         }
#
#         serializer = accounts_serializers.UserSerializer(
#             user, data=sanitized_data, partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, user_id):
#         """Delete a user by id"""
#         logger.info(f"deleting user {user_id}")
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": f"user {user_id} not found"}, status=404)
#
#         user.delete()
#         return Response(
#             {"message": f"user with id {user_id} deleted successfully"}, status=204
#         )