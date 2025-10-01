from django.http import JsonResponse, HttpRequest


def index(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok", "message": "API root"})
