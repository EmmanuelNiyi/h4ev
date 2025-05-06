import json
import os
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework.views import APIView

from h4ev import settings

User = get_user_model()


def create_user_account(serializer):
    """Handles the core logic of user creation"""
    validated_data = serializer.validated_data

    password = validated_data.get("password")
    validated_data["password"] = make_password(password)  # Hash the password

    try:
        user = User.objects.create(**validated_data)

        return user
    except Exception as e:
        raise ValidationError(e)


class LoggingAPIView(APIView):
    """
    Extends DRF’s APIView to log, per authenticated user:
      - request method, path, headers, body
      - response status, body
      - timing: start, end, duration_ms
    Logs are appended as JSON lines in settings.LOG_DIR/user_<id>.jsonl.
    """

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if not getattr(request, 'user', None) or not request.user.is_authenticated:
            return

        # record start
        request._start_time = datetime.utcnow()

        # minimal request info
        request._log_data = {
            "user_id": request.user.id,
            "username": request.user.get_username(),
            "timestamp_start": request._start_time.isoformat() + "Z",
            "request": {
                "method": request.method,
                "path": request.get_full_path(),
            },
        }

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        if not hasattr(request, "_start_time"):
            return response

        end_time = datetime.utcnow()
        duration_ms = (end_time - request._start_time).total_seconds() * 1000

        # complete the log entry with only status_code
        log_entry = request._log_data
        log_entry.update({
            "timestamp_end": end_time.isoformat() + "Z",
            "duration_ms": round(duration_ms, 2),
            "response": {
                "status_code": response.status_code,
            }
        })

        # ensure log dir exists
        os.makedirs(settings.LOG_DIR, exist_ok=True)
        logfile = os.path.join(settings.LOG_DIR, f"user_{request.user.id}.jsonl")

        with open(logfile, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return response
