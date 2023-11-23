import datetime
import secrets, string


def make_bool(val):
    if str(val) == 'false' or str(val) == '0' or str(val) == 'False':
        return False
    else:
        return True


def make_next_date(day):
    now = datetime.datetime.now()
    return now + datetime.timedelta(days=day)


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist as e:
        return None


def make_password():
    letters = string.ascii_letters
    digits = string.digits
    alphabet = letters + digits
    pwd_length = 9
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))
    return pwd