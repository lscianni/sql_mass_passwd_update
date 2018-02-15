#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Louis Scianni
# 2018-02-13

"""
Test timeclock passwd updating script
"""

import csv, MySQLdb as mdb
from sys import argv, getsizeof
from os import path
from getpass import getpass
from bcrypt import hashpw, gensalt

def help_info():
    return 'Usage: %s host username database file\n \
            \nUpdates user timeclock passwords from a csv file\n \
            the csv file must be in the following format\n \
            \n \
            SamAccountName,Password\n \
            username,newpassword\n \
            ......\n \
            \nex. timeclock_password_update.py sql.example.com dbadmin timelcock_db \
            newpasswords.csv\n' % argv[0]
    

    
def main():        
    table = 'atrusers'
    main.logfile = 'timeclockpasswdupdate.log'
    
    def connect_db():
        try:
            server = argv[1]#'192.173.1.11'
            username = argv[2]#'lscianni'
            print('MySQL password')
            passwd = getpass()
            database = argv[3]#'test_timeclock_passwd'

        except IndexError:
            help_info()

        try:
            connect_db.conn = mdb.connect(server, username, passwd, database)
        except mdb.Error as e:
            with open(main.logfile, 'w') as logfile:
               logfile.write('SQL Connection Error: %s\n' % e)
    
        def get_pass():
            try:
                csv_file = argv[4]
            except IndexError:
                help_info()
            pw_col = 'password'
            email_col = 'emailaddress'

            if path.exists(csv_file) == False:
                print('File Not Found (did you use the full path?)\n')
                exit()
            
            email_suffix = 'appliedtechres.com'
            
            with open(csv_file, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    get_pass.user_name = row['SamAccountName'] 
                    get_pass.passwd = bytes(row['Password'].encode('utf-8'))
                    print('hashing %s\'s password' % get_pass.user_name)
                    
                    #hashed = hashpw(get_pass.passwd.encode('utf-8'), gensalt(10))
                    get_pass.hashed = str(hashpw(get_pass.passwd, gensalt(10)), 'utf-8')

                    get_pass.email = '%s@%s' %(get_pass.user_name, email_suffix)
                    get_pass.hashstring = get_pass.hashed[1:]
                    with open(main.logfile, 'a') as logfile:
                        logfile.write('%s,%s\n' % (get_pass.email, get_pass.hashstring))

                    sql = 'UPDATE %s SET %s = "%s" WHERE %s = "%s"' % (table, pw_col, get_pass.hashed, email_col, get_pass.email)
                    
                    try:    
                        cur = connect_db.conn.cursor()
                        cur.execute(sql)
                        connect_db.conn.commit()
                        cur.close()
                        with open(main.logfile, 'a') as logfile:
                            logfile.write('success\n')
                        with open(main.logfile, 'a') as logfile:
                            logfile.write('password for %s updated\n' % get_pass.user_name)
                    except mdb.Error as e:
                        with open(main.logfile, 'a') as logfile:
                            logfile.write('MYSQL ERROR: %s\n' % e)
                            print('SQL ERROR check %s' % logfile)
                            connect_db.conn.rollback()
        
        get_pass()
           
    connect_db()
    

if __name__ == '__main__':
    main()
