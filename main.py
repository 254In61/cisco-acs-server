#!/usr/tools/pyenv/shims/python3
""" Script that calls on acsclient API for automation purposes"""
#Script to be used to decommision devices.
#https://github.com/nlgotz/acsclient
#https://github.com/nlgotz/acsclient/blob/master/acsclient/acsclient.py
from getpass import getpass
import requests,os
from acsclient.acsclient import ACSClient
from creds import *

def main():
    """Section to clean up ACS Server DB"""
    print("\n==========Clean up CIs from ACS Server DB========\n")
    for line in open("hosts","r").read().rstrip().split("\n") :
        print("\n**PROCESSING:",line.split()[1])
        ClassAcs(acs_usn,acs_pass,line.split()[1]).delete_host()

    print("\n==================================================")


class ClassAcs():
    """Class to delete objects from ACS Server"""
    def __init__(self,username,password,host):
        self.__username = username
        self.__password = password
        self.__host = host
        self.__endpoint = "10.122.102.26"

    def delete_host(self):
        instance = ACSClient(self.__endpoint,self.__username,self.__password,True)
        print("api querry output:")
        response = instance.read("NetworkDevice/Device", "name" , self.__host)
        print(response)

        """Using str() version since output is not in a format of string!!"""

        if "<Response [401]>" in (str(response)):
            print("failed login access into acs-server.Check your credentials again.")

        elif "<Response [410]>" in (str(response)):
            print("ci not found in acs-server database.")

        elif "<Response [200]>" in (str(response)):
            instance.delete("NetworkDevice/Device", "name" , self.__host)
            print("success : CI removed from ACS Server")

        else:
            print("unknown error.ci not deleted from acs-server database")


if __name__ == '__main__':
    main()
