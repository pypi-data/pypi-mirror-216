"""
This code defines a class which "unlatches" a given folder.
"""

# Standard imports.
import shutil
from pathlib import Path

# Non-standard imports.
from cryptography.fernet import Fernet, InvalidToken

# Local imports.
from .latcher import Latcher, LatcherError, make_key

##############
# MAIN CLASS #
##############

class Unlatcher(Latcher):
    """ The class in question. """
    def __init__(self, path_to_target):
        super().__init__(path_to_target)
        self.path_to_target = path_to_target
        self._path_obj_to_parent = Path(path_to_target).parent
        self._target_name = Path(path_to_target).stem
        self.path_to_decrypted = path_to_target+"_"
        self.path_to_zip = self.get_path_to_zip()
        self.path_to_salt = self.get_path_to_salt()
        self.salt = self.get_salt()

    def get_salt(self):
        """ Return the salt object. """
        if not Path(self.path_to_salt).exists():
            raise LatcherError("No salt file at: "+self.path_to_salt)
        with open(self.path_to_salt, "rb") as salt_file:
            result = salt_file.read()
        return result

    def unzip_target(self):
        """ Unzip the target directory. """
        if Path(self.path_to_decrypted).is_dir():
            raise LatcherError(
                "Folder already exists at: "+
                self.path_to_decrypted
            )
        shutil.unpack_archive(self.path_to_zip, self.path_to_decrypted)

    def get_byte_data_to_decrypt(self):
        """ Read in the zip file, and return the bytes therein. """
        if not Path(self.path_to_target).exists():
            raise LatcherError("No encrypted file at: "+self.path_to_target)
        with open(self.path_to_target, "rb") as target_file:
            result = target_file.read()
        return result

    def decrypt(self, password):
        """ Build an decrypted version of the target. """
        byte_data = self.get_byte_data_to_decrypt()
        key = make_key(self.salt, password)
        fernet_obj = Fernet(key)
        try:
            decrypted_data = fernet_obj.decrypt(byte_data)
        except InvalidToken:
            return False
        with open(self.path_to_zip, "wb") as zip_file:
            zip_file.write(decrypted_data)
        return True

    def clean(self):
        """ Remove any encrypted data, as well as any generated files. """
        files_to_remove = (self.path_to_zip, self.path_to_target)
        for file_path in files_to_remove:
            Path(file_path).unlink()

    def unlatch(self, password):
        """ (1) Decrypt. (2) Unzip. (3) Clean. """
        self.decrypt(password)
        self.unzip_target()
        self.clean()
