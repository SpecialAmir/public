# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# class Token(PasswordResetTokenGenerator):
#     pass


# random_token=Token()

import random

def create_new_ref_number():
      return str(random.randint(1000000000, 9999999999))

random_token=create_new_ref_number()