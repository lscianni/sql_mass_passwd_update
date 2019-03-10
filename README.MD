# sql_mass_pass_update

Reads new passwords from a csv file, hashes the password using bcrypt and updates the corresponding users password in a database.

When building an executable with pyinstaller you may be required to pass the --hidden-import=_cffi_backend option.

#### Required Modules
* mysqlclient
* bcrypt
