import re

from django.core.exceptions import ValidationError


# Validate email : example: example@example.com
def email_validation(email):
    pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.[a-z]"
    if re.search(pattern, email):
        return True
    else:
        raise ValidationError("Invalid email")


def password_validation(password):
    if not len(password) > 8 and not len(password) < 20:
        raise ValidationError("Password must be greater than 8 digits and less than 20")
    elif not any(character.islower() for character in password):
        raise ValidationError("Password should have at least one character lower case")
    elif not any(character.isupper() for character in password):
        raise ValidationError("Password should have at least one character upper case")
    elif not any(character.isdigit() for character in password):
        raise ValidationError("Password should have at least one number")
    elif not any(character in ["@", "$", "#"] for character in password):
        raise ValidationError("Password should have at least one special character [@, $, #]")
    else:
        return True
