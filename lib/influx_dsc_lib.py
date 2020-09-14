#!/usr/bin/env python3

import argparse

from influxdb import InfluxDBClient
import sys
import os
import re
import logging
import json
import parallel_ssh_lib
import penctl_lib
import ast
import time
from datetime import datetime
import dsc_oper_lib


logging.basicConfig( level=logging.INFO, filename="/tmp/venk_script.log", filemode='w')
logging.root.setLevel(logging.INFO)
log = logging.getLogger("hostmgmt")




def create_influx_session( host, port=8086, username='root', password='XXXXX' ):
    client = InfluxDBClient( host=host, port=port, username=username, password=password )
    return client


# Influx client handle attributes - 
# ['_InfluxDBClient__baseurl', '_InfluxDBClient__host', '_InfluxDBClient__path', '_InfluxDBClient__port', '_InfluxDBClient__udp_port', '_InfluxDBClient__use_udp', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_baseurl', '_batches', '_database', '_gzip', '_headers', '_host', '_password', '_path', '_port', '_proxies', '_read_chunked_response', '_retries', '_scheme', '_session', '_timeout', '_udp_port', '_use_udp', '_username', '_verify_ssl', '_write_points', 'alter_retention_policy', 'close', 'create_continuous_query', 'create_database', 'create_retention_policy', 'create_user', 'delete_series', 'drop_continuous_query', 'drop_database', 'drop_measurement', 'drop_retention_policy', 'drop_user', 'from_dsn', 'get_list_continuous_queries', 'get_list_database', 'get_list_measurements', 'get_list_privileges', 'get_list_retention_policies', 'get_list_series', 'get_list_users', 'grant_admin_privileges', 'grant_privilege', 'ping', 'query', 'request', 'revoke_admin_privileges', 'revoke_privilege', 'send_packet', 'set_user_password', 'switch_database', 'switch_user', 'write', 'write_points']


def create_db( client, dbname, retention_duration, replication ):
    client.create_database(dbname)
    retention_policy_name = dbname + "_retention_policy"
    client.create_retention_policy( retention_policy_name, database=dbname, duration=retention_duration, replication=replication )
    db_list = client.get_list_database()
    if dbname not in db_list:
       print('Error !! Creating Database {} failed'.format(dbname))



def switch_db( client, dbname ):
    client.switch_database(dbname)




def write_dsc_cps_measurement( log, client, phdl, dscs_dict, measurement_name='cps' ):
    dscs_cps_dict = dsc_oper_lib.get_dscs_drop_metrics( log, phdl )
    for dsc_ip in dscs_cps_dict.keys():
        dsc_id = dscs_dict[dsc_ip]['dsc-id']
        if re.search( 'TRANSPARENT|INSERT', dscs_dict[dsc_ip]['fwd-mode'] ):
           connections_per_second = dscs_cps_dict[dsc_ip]['FteCPSMetrics']['connections_per_second']
           max_packets_per_second = dscs_cps_dict[dsc_ip]['FteCPSMetrics']['max_packets_per_second']
           current_time = datetime.strftime(time_obj, '%Y-%m-%dT%H:%M:%S.%fZ')
           json_body_str = '''[
           {
               "measurement": "''' + str(measurement_name) + '''",
               "tags": {
                     "dsc-id": "''' + str(dsc_id) + '''",
                     "dsc-ip": "''' + str(dsc_ip) + '''"
                 },
                 "time": "''' + str(current_time) + '''",
                 "fields": {
                     "connections_per_second": ''' + str(connections_per_second) + ''',
                     "max_packets_per_second": ''' + str(max_packets_per_second) + '''
                 }
               }
            ]'''
            json_body = eval(json_body_str)
            print('Writing CPS Measurement Points: {0}'.format(json_body))
            client.write_points(json_body)




def write_intf_statistics( client, phdl, measurement_name='interface_stats'):
    intf_dict = penctl_lib.get_linux_interface_stats( phdl )
    for host in intf_dict.keys():
        for intf in intf_dict[host]['interface_list']:
            time_obj = datetime.now()
            i_dict = intf_dict[host]['interface_stats'][intf]
            current_time = datetime.strftime(time_obj, '%Y-%m-%dT%H:%M:%S.%fZ')
            json_body_str = '''[
              {
                 "measurement": "''' + str(measurement_name) + '''",
                 "tags": {
                     "host": "''' + str(host) + '''",
                     "interface": "''' + str(intf) + '''"
                 },
                 "time": "''' + str(current_time) + '''",
                 "fields": {
                 "TxPackets": ''' + str(i_dict['tx_pkts']) + ''',
                 "RxPackets": ''' + str(i_dict['rx_pkts']) + ''',
                 "TxBytes": ''' + str(i_dict['tx_bytes']) + ''',
                 "RxBytes": ''' + str(i_dict['rx_bytes']) + '''
                 }
               }
            ]'''
            json_body = eval(json_body_str)
            print('Writing Points: {0}'.format(json_body))
            client.write_points(json_body)
            



def write_dsc_temperature( client, phdl, measurement_name='dsc_temperature'):
    temp_dict = penctl_lib.get_penctl_temperature( phdl, int_mnic_ip_list )
    for host in temp_dict.keys():
        for int_mnic_ip in temp_dict[host].keys():
            time_obj = datetime.now()
            current_time = datetime.strftime(time_obj, '%Y-%m-%dT%H:%M:%S.%fZ')
            json_body_str = '''[
              {
                 "measurement": "''' + str(measurement_name) + '''",
                 "tags": {
                     "host": "''' + str(host) + '''",
                     "int_mnic": "''' + str(int_mnic_ip) + '''"
                 },
                 "time": "''' + str(current_time) + '''",
                 "fields": {
                 "LocalTemperature": ''' + str(temp_dict[host][int_mnic_ip][0]['LocalTemperature']) + ''',
                 "DieTemperature": ''' + str(temp_dict[host][int_mnic_ip][0]['DieTemperature']) + ''',
                 "HbmTemperature": ''' + str(temp_dict[host][int_mnic_ip][0]['HbmTemperature']) + '''
                 }
               }
            ]'''
            json_body = eval(json_body_str)
            print('Writing Points: {0}'.format(json_body))
            client.write_points(json_body)



#create_db( db_name, host, port=8086, user='root', password='root', retention_duration='14d' )

influx_host = '10.30.5.9'
influx_port = 8086
user = 'root'
password = 'root'

phdl = parallel_ssh_lib.ParallelSessions( log, host_config )

client = InfluxDBClient( host=influx_host, port=influx_port, username=user, password=password, database='dsc_metrics' )
#client.drop_database('dsc_metrics')

#create_db( client, 'dsc_metrics' )

query = 'select DieTemperature from dsc_temperature;'
result = client.query(query)
print(result)
#sys.exit(1)

while True:
   write_dsc_temperature( client, phdl, measurement_name='dsc_temperature')
   write_intf_statistics( client, phdl, measurement_name='interface_stats')
   time.sleep(300)
