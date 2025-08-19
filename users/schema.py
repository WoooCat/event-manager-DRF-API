from drf_spectacular.extensions import OpenApiAuthenticationExtension


class SessionBoundJWTExtension(OpenApiAuthenticationExtension):
    target_class = 'users.auth.SessionBoundJWTAuthentication'
    name = 'SessionBoundJWTAuth'
    match_subclasses = True

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
