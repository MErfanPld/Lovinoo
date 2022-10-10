from django.shortcuts import redirect


class AdminUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return super(AdminUserMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect("/")
