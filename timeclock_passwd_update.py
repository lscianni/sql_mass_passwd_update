#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Louis Scianni
# 2018-02-13

"""
Test timeclock passwd updating script

Updates the timeclock passwords stored in mysql as bcrypt hashes.
Reads usernames and passwords from a csv file.
If the hashes don't match its printed to a log file. 
"""

import csv, MySQLdb as mdb
from sys import argv, getsizeof
from os import path
from getpass import getpass
from bcrypt import hashpw, gensalt
    
def main():        
    table = 'atrusers' # change this to the real table name
    main.logfile = 'timeclockpasswdupdate.log'
    
    def help_info():
        return 'Usage: %s host username database file\n \
            \nUpdates user timeclock passwords from a csv file\n \
            the csv file must be in the following format\n \
            \n \
            SamAccountName,Password\n \
            username,newpassword\n \
            ...\n \
            \nex. timeclock_password_update.py sql.example.com dbadmin timelcock_db \
            newpasswords.csv\n' % argv[0]
    
    def get_args():
        # Get arguments form commandline
        try:
            get_args.server = argv[1]
            get_args.username = argv[2]
            print('MySQL password')
            get_args.passwd = getpass()
            get_args.database = argv[3]
            get_args.csv_file = argv[4]

        except IndexError:
            help_info()
   
    
    def connect_db():
        get_args()

        try:
            connect_db.conn = mdb.connect(get_args.server, get_args.username, get_args.passwd, get_args.database)

        except AttributeError:
            help_info()
             
        except mdb.Error as e:
            with open(main.logfile, 'w') as logfile: # write to log; maybe make this a function
               logfile.write('SQL Connection Error: %s\n' % e)
               print('%s\n' % e)
    
        def get_pass():

            pw_col = 'password'
            email_col = 'emailaddress'

            if path.exists(get_args.csv_file) == False:
                print('File Not Found (did you use the full path?)\n')
                help_info()
            
            else:
                email_suffix = 'appliedtechres.com'
            
                with open(get_args.csv_file, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        get_pass.user_name = row['SamAccountName'] 
                        get_pass.passwd = row['Password'].encode('utf-8')
                        print('hashing %s\'s password' % get_pass.user_name)
                        salt = gensalt(10, prefix=b"2a")
                        get_pass.hashed = hashpw(get_pass.passwd, salt)
                        # check if the hash is valid
                        if hashpw(get_pass.passwd, get_pass.hashed) != get_pass.hashed:
                            print('Hash mix-match')
                            with open(main.logfile, 'a') as logfile:
                                logfile.write('Hash:%s did not match')
                        else:
                            # convert the hash form binary to a string    
                            get_pass.hashed = str(get_pass.hashed)[1:]

                            get_pass.email = '%s@%s' %(get_pass.user_name, email_suffix)
                            #get_pass.hashstring = get_pass.hashed[1:]
                            with open(main.logfile, 'a') as logfile:
                                logfile.write('%s,%s\n' % (get_pass.email, get_pass.hashed))
                            # sql update statement
                            sql = 'UPDATE %s SET %s = "%s" WHERE %s = "%s"' % (table, pw_col, get_pass.hashed, email_col, get_pass.email)
                    
                            try:    
                                cur = connect_db.conn.cursor()
                                cur.execute(sql)                  # execute sql
                                connect_db.conn.commit()
                                cur.close()
                                with open(main.logfile, 'a') as logfile:
                                    logfile.write('success\n')
                                with open(main.logfile, 'a') as logfile:
                                    logfile.write('password for %s updated\r\n\n' % get_pass.user_name)
                            except mdb.Error as e:
                                with open(main.logfile, 'a') as logfile:
                                    logfile.write('MYSQL ERROR: %s\n' % e)
                                    print('SQL ERROR check %s' % logfile)
                                    connect_db.conn.rollback() # rollback if there is an error
        
        get_pass()
    connect_db()
    
if __name__ == '__main__':
    main()
