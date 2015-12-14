from django.contrib.auth.models import User

import factory


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user_%03d" % n)
    password = factory.Sequence(lambda n: "user_%03d" % n)
    email = factory.Sequence(lambda n: "user_%03d@email.com" % n)
    is_active = True
