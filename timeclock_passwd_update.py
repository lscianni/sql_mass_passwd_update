#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Louis Scianni
# 2018-02-13

"""
Test timeclock passwd updating utility
"""

import MySQLdb as mdb
from sys import argv
from getpass import getpass
from bcrypt import hashpw, gensalt
    
def connect_db():
    server = '192.173.1.11'
    username = 'lscianni'
    print('MySQL password')
    passwd = getpass()
    database = 'test_timeclock_passwd'
    
    connect_db.con = mdb.connect(server, username, passwd, database)
    
def main():        
    table = 'atrusers'
    try:
        user_name = argv[1]
    except IndexError:
        print('Pass a user name')
        exit()
        
    def get_pass():                                # Securely get the password from the user
        try:
            print('Enter atr user password')
            get_pass.passwd = getpass()
            print('Verify atr user password')
            verify_pass = getpass()
            
            if verify_pass == get_pass.passwd:
                get_pass.passwd == True
            else:
                get_pass.passwd == False
                raise ValueError('Passwords do not match')
            
            if get_pass.passwd == True:
                return get_passwd.passwd
        except ValueError as e:
            print(e)
            exit()
        
    get_pass()
    
    hashed = hashpw(get_pass.passwd.encode('utf-8'), gensalt(10))
    hashstring = str(hashed)
    hashstring = hashstring[1:]
    print(hashstring)
    
    
    connect_db()
    try:
        pw_col = 'password'
        email_col = 'emailaddress'
        sql = 'UPDATE %s SET %s = "%s" WHERE %s = "%s"' % (table, pw_col, hash, email_col, user_name) 
        cur = connect_db.con.cursor()
        cur.execute(sql)
        connect_db.con.commit()
        connect_db.con.close()
        print('password for %s updated\n' % user_name)
        
    except mdb.Error as e:
        print(e)
        connect_db.con.rollback()
        connect_db.con.close()
    
    
    

if __name__ == '__main__':
    main()