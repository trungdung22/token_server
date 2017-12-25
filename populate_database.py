secret_key = "dc2bd2a004f7ea14c05ba8aa07345"



def populate():
    market = add_market(1, "Bittrex")

    token_type_normal = add_token_type(1, 'Normal', 100)
    token_type_trial = add_token_type(2, 'Trial', 1)
    add_user('DungDo1604', 'dungbme10@gmail.com', 'WhoDaddy1604')
    for i in range(20):
        token_key_1 = add_token_key(token_type_normal)


def add_market(pk, market_name):
    market = Market.objects.get_or_create(pk=pk, market_name=market_name)[0]
    return market


def add_token_type(pk, token_name, market_limit):
    token_type = TokenType.objects.get_or_create(pk=pk, token_name=token_name,
                                                 market_limit=market_limit)[0]
    return token_type


def add_token_key(tokey_type):
    random_hash = get_random_string(16)
    token_key = TokenKey.objects.get_or_create(token_hash=random_hash,
                                               token_type=tokey_type)[0]
    return token_key


def add_user(username, email, password):
    user = create_user(username, email, password)
    adminAccount = AdminAccount.objects.get_or_create(user=user)[0]
    return adminAccount


def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user


# Start execution here!
if __name__ == '__main__':
    import os
    print "Starting Rango population script..."
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

    from django.utils.crypto import get_random_string
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()

    from django.contrib.auth.models import User
    from token_server.models import *

    populate()
