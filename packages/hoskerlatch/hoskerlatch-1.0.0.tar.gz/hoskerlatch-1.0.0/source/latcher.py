"""
This code defines a class which "latches" a given folder.
"""

# Standard imports.
import base64
import random
import secrets
import shutil
import string
from pathlib import Path

# Non-standard imports.
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# Local constants.
ARCHIVE_FORMAT = "zip"
ARCHIVE_SUFFIX = ".zip"
BLOCK_SIZE = 8
FILENAME_LENGTH = 9
KEY_LENGTH = 32
MEMORY_COST = 2**14
PUBLIC_KEY_LENGTH = 2048
PUBLIC_KEY_FILENAME = "latch.pem"
PUBLIC_KEY_FILE_MODE = "PEM"
SALT_FILENAME = ".latch.salt"
SALT_LENGTH = 16

##############
# MAIN CLASS #
##############

class Latcher:
    """ The class in question. """
    def __init__(self, path_to_target, resalt=False):
        self.path_to_target = path_to_target
        self.resalt = resalt
        self._path_obj_to_parent = Path(path_to_target).parent
        self._target_name = Path(path_to_target).stem
        self.path_to_encrypted = self.get_path_to_encrypted()
        self.path_to_zip = self.get_path_to_zip()
        self.path_to_salt = self.get_path_to_salt()
        self.salt = self.get_salt()

    def get_path_to_encrypted(self):
        """ Ronseal. """
        path_obj = self._path_obj_to_parent/make_random_string()
        result = str(path_obj.resolve())
        return result

    def get_path_to_zip(self):
        """ Ronseal. """
        path_obj = self._path_obj_to_parent/(self._target_name+ARCHIVE_SUFFIX)
        result = str(path_obj.resolve())
        return result

    def get_path_to_salt(self):
        """ Ronseal. """
        path_obj = self._path_obj_to_parent/SALT_FILENAME
        result = str(path_obj.resolve())
        return result

    def get_salt(self):
        """ Return the salt object, generating it as necessary. """
        if Path(self.path_to_salt).exists() and not self.resalt:
            with open(self.path_to_salt, "rb") as salt_file:
                result = salt_file.read()
        else:
            result = secrets.token_bytes(SALT_LENGTH)
            with open(self.path_to_salt, "wb") as salt_file:
                salt_file.write(result)
        return result

    def zip_target(self):
        """ Zip the target directory. """
        if Path(self.path_to_zip).exists():
            raise LatcherError(
                "Zip file at already exists at: "+
                self.path_to_zip
            )
        if not Path(self.path_to_target).is_dir():
            raise LatcherError(
                "Target is not a folder: "+
                self.path_to_target
            )
        path_obj_to_zip = Path(self.path_to_zip)
        archive_command_path = \
            str(path_obj_to_zip.parent/path_obj_to_zip.stem)
        shutil.make_archive(
            archive_command_path,
            ARCHIVE_FORMAT,
            self.path_to_target
        )
        return True

    def get_byte_data_to_encrypt(self):
        """ Read in the zip file, and return the bytes therein. """
        if not Path(self.path_to_zip).exists():
            raise LatcherError("No zip file to read in at: "+self.path_to_zip)
        with open(self.path_to_zip, "rb") as zip_file:
            result = zip_file.read()
        return result

    def encrypt(self, password):
        """ Build an encrypted version of the zipped target. """
        byte_data = self.get_byte_data_to_encrypt()
        key = make_key(self.salt, password)
        fernet_obj = Fernet(key)
        encrypted_data = fernet_obj.encrypt(byte_data)
        if Path(self.path_to_encrypted).exists():
            raise LatcherError(
                "Encrypted file at "+
                self.path_to_encrypted+
                " already exists."
            )
        with open(self.path_to_encrypted, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

    def clean(self):
        """ Remove any unencrypted data, as well as any generated files. """
        files_to_remove = (self.path_to_zip,)
        folders_to_remove = (self.path_to_target,)
        for file_path in files_to_remove:
            Path(file_path).unlink()
        for folder_path in folders_to_remove:
            shutil.rmtree(folder_path)

    def latch(self, password):
        """ (1) Zip. (2) Encrypt. (3) Clean. """
        self.zip_target()
        self.encrypt(password)
        self.clean()

################################
# HELPER FUNCTIONS AND CLASSES #
################################

class LatcherError(Exception):
    """ A custom exception. """

def make_random_string():
    """ Construct a string of random characters. """
    result = \
        "".join(
            random.choice(string.ascii_lowercase+string.digits)
            for _ in range(FILENAME_LENGTH)
        )
    return result

def make_key(salt, password):
    """Derive the key from the password using the passed salt. """
    parallelisation_parameter = 1
    key_derivation_function = \
        Scrypt(
            salt,
            KEY_LENGTH,
            MEMORY_COST,
            BLOCK_SIZE,
            parallelisation_parameter
        )
    derived_key = key_derivation_function.derive(password.encode())
    result = base64.urlsafe_b64encode(derived_key)
    return result
