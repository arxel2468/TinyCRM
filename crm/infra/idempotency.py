import hashlib
from django.core.cache import cache
from rest_framework.response import Response


def idempotent_post(ttl=60 * 60 * 24):
    def outer(view_method):
        def inner(self, request, *args, **kwargs):
            key = request.headers.get("Idempotency-Key")
            if not key:
                return view_method(self, request, *args, **kwargs)
            scope = (
                f"idemp:{request.user.id}:{hashlib.sha256(key.encode()).hexdigest()}"
            )
            cached = cache.get(scope)
            if cached:
                return Response(cached["body"], status=cached["status"])
            resp = view_method(self, request, *args, **kwargs)
            if 200 <= resp.status_code < 300:
                cache.set(scope, {"status": resp.status_code, "body": resp.data}, ttl)
            return resp

        return inner

    return outer
