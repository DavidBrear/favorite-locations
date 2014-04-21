from flask import abort

class BaseController:
    def __init__(self):
        self.name = 'BaseController'

    def call(self, request, id=None, action=None, params={}):
        method = request.method.lower()
        if action is None:
            if id is None:
                if method == 'post':
                    return self.create(request)
                return self.index()
            if method == 'post':
                return self.update(id, request)
            if id == 'new':
                return self.new()
            return self.show(id)
        if action == 'delete':
            return self.delete(id)
        try:
            return getattr(self, action)(id, request, params)
        except:
            abort(400)

