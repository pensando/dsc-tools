#!/usr/bin/env python3

from __future__ import print_function
from pssh.clients import ParallelSSHClient

import sys
import os
import re
import ast
import json

# Following used only for scp of file
import paramiko
from paramiko import SSHClient
from scp import SCPClient

class ParallelSessions():
    """
    ParallelSessions - Uses the pssh library that is based of Paramiko, that lets you take
    multiple parallel ssh sessions to hosts and execute commands. This library will be
    used for the Naples Host Managed solution ..

    """

    def __init__(self, log, host_config, penctl='/root/penctl.linux' ):

        self.log            = log
        self.host_config    = host_config
        self.hosts          = host_config.keys()
        self.penctl         = penctl

        self.client         = ParallelSSHClient( self.hosts, host_config=self.host_config)


    def exec(self, cmd ):
        """
        Returns a dictionary of host as key and command output as values
        """
        cmd_output = {}
        output = self.client.run_command(cmd )
        for host, host_output in output.items():
            cmd_out_str = ''
            for line in host_output.stdout:
                cmd_out_str = cmd_out_str + line.replace( '\t', '   ')
                cmd_out_str = cmd_out_str + '\n'
            cmd_output[host] = cmd_out_str
        return cmd_output


    def scp_file(self, local_file, remote_file, recurse=False ):
        print('About to copy local file {} to remote {} on all Hosts'.format(local_file, remote_file))
        cmds = self.client.copy_file( local_file, remote_file, recurse=recurse )
        self.client.pool.join()
        for cmd in cmds:
            try:
               cmd.get()
            except IOError:
               raise Exception("Expected IOError exception, got none")
        return

 

    def penctl_exec(self, cmd, pen_agent='/root/penagent_linux.py', penctl='/root/penctl.linux', output_type='json', cert_file=None ):
        """
        Returns a dictionary of host, dscs as keys and command output as values
        """
        cmd_output = {}
        penctl_cmd = '{} --cmd "{}" --penctl_path {} --output_type {} --cert_file {}'.format(pen_agent, cmd, penctl, output_type, cert_file )
        print(penctl_cmd)
        output_dict = {}
        output = self.client.run_command( penctl_cmd, )
        for host, host_output in output.items():
            print(host)
            cmd_out_str = ''
            for line in host_output.stdout:
                cmd_out_str = cmd_out_str + line.replace( '\t', '   ')
                if not re.search( 'json',  output_type, re.I ):
                   cmd_out_str = cmd_out_str + '\n'
            if re.search( 'json',  output_type, re.I ):
               #print(cmd_out_str)
               #print(type(cmd_out_str))
               output_dict[host] = ast.literal_eval(cmd_out_str.replace( "'", '"' ))
            else:
               output_dict[host] = ast.literal_eval(cmd_out_str)
        print('%%%%%%%%')
        print(output_dict)
        print('%%%%%%%%')
        return output_dict

    def reboot_connections(self ):
        print('Rebooting Connections')
        self.client.run_command( 'reboot -f' ) 

    def destroy_clients(self ):
        print('Destroying Current phdl connections ..')
        del self.client



def scp( src, dst, srcusername, srcpassword, dstusername = None, dstpassword = None):
    """
       This method gets/puts files from one server to another
       :param arg: These are sub arguments for scp command
       :return: None
       :examples:
           To get remote file '/tmp/x' from 1.1.1.1 to local server '/home/user/x'
           scp('1.1.1.1:/tmp/x', '/home/user/x', 'root', 'XXXXX')
           To put local file  '/home/user/x to remote server-B's /tmp/x'
           scp('/home/user/x', '1.1.1.1:/tmp/x', 'root', 'XXXXX')
           To copy remote file '/tmp/x' from 1.1.1.1 to remote server 1.1.1.2 '/home/user/x'
           scp('1.1.1.1:/tmp/x','1.1.1.2:/home/user/x','root','XXXXX','root','XXXXX')
    """

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    srclist = src.split(":")
    dstlist = dst.split(":")
    # 0 means get, 1 means put, 2 means server A to server B
    get_put = 1
    srcip   = None
    dstip   = None

    if len(srclist) == 2:
        srcip = srclist[0]
        srcfile = srclist[1]
        ssh.connect(srcip, username=srcusername, password=srcpassword)
        get_put = 0
    else:
        srcfile = srclist[0]

    if len(dstlist) == 2:
        dstip = dstlist[0]
        dstfile = dstlist[1]
        if get_put == 0:
            get_put = 2
        else:
            get_put = 1
            ssh.connect(dstip, username=srcusername, password=srcpassword)
    else:
        dstfile = dstlist[0]
    if get_put < 2:
       scp = SCPClient(ssh.get_transport())
       if not get_put:
           scp.get(srcfile,dstfile)
       else:
           scp.put(srcfile,dstfile)
       scp.close()
    else:
        if dstusername is None:
            dstusername = srcusername
        if dstpassword is None:
            dstpassword = srcpassword
        # This is to handle if ssh keys in the known_hosts is empty or incorrect
        # Need better way to handle in the future
        output = ssh.exec_command('ssh-keygen -R %s'%(dstip))
        # print('ssh-keygen output is {0}'.format(output))
        time.sleep(1)
        output = ssh.exec_command('ssh-keyscan %s >> ~/.ssh/known_hosts'%(dstip))
        # print('ssh-keyscan output is {0}'.format(output))
        time.sleep(1)
        output = ssh.exec_command('sshpass -p %s scp %s %s@%s:%s'%(dstpassword, srcfile, dstusername, dstip, dstfile))
