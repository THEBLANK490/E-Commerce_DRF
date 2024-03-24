def get_success(code,message,data=None):
    context = {
    "code":code,
    "message":message,
    "data": data,
    "error":{}
    }
    return context

def get_error(code,message,error):
    context = {
    "code":code,
    "message":message,
    "data": {},
    "error":error,
    }
    return context