import hashlib
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import MD5PasswordHasher


class BoxingMD5PasswordHasher(MD5PasswordHasher):
    algorithm = "boxing"

    def encode(self, password, salt):
        assert password is not None
        assert salt and '$' not in salt
        hash = hashlib.md5(force_bytes(f'{password}{{{salt}}}')).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)
