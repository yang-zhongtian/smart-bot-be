from ninja import NinjaAPI

from .exception import ServiceUnavailableError, BadRequestError

api = NinjaAPI()

api.add_router("/auth/", "bot_auth.api.router")


@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


@api.exception_handler(BadRequestError)
def bad_request(request, exc):
    return api.create_response(
        request,
        {"message": str(exc)},
        status=400,
    )
