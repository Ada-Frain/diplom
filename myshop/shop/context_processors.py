from .favorites import Favorite


def favorites(request):
    ctx = dict()
    ctx['favorites'] = Favorite(request.session)
    return ctx