#!/usr/bin/env python3

import sys
import os
import re
import logging
import json
import parallel_ssh_lib
import penctl_lib
import ast
import dsc_oper_lib
from html_builder_lib import *


# Generate DSC Summary Page
def generate_host_dsc_summary_page( log, phdl, html_file, cert_file=None ):
   
    # Get the dsc_summary_dict
    #firmware_out_list = penctl_lib.get_penctl_cmd_out_dict( phdl, int_mnic_ip_list, 'show firmware-version' )
    dsc_dict = penctl_lib.get_dsc_dict( phdl, cert_file=cert_file )

    print(dsc_dict)
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)

    generateDscTable( html_file, 'table1', 'DSC Summary', dsc_dict )
    buildHtmlMainPageFooter(html_file)
    buildHtmlFooter(html_file)



def generate_dsc_host_port_page( log, phdl, html_file, cert_file=None ):
    port_dict = penctl_lib.get_penctl_port( phdl, cert_file=cert_file) 
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)

    generatePortTable( html_file, 'Port Info', port_dict )
    buildHtmlMainPageFooter(html_file)
    buildHtmlFooter(html_file)


def generate_dsc_temp_page( log, phdl, html_file, cert_file=None ):
    temp_dict = penctl_lib.get_penctl_temperature( phdl, cert_file=cert_file )
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)
    generateTemperatureTable( html_file, 'table1', 'Temperature Info', temp_dict )
    buildHtmlMainPageFooter(html_file)
    buildHtmlFooter(html_file)



def generate_dsc_power_page( log, phdl, html_file, cert_file=None ):
    power_dict = penctl_lib.get_penctl_power( phdl, cert_file=cert_file )
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)
    generatePowerTable( html_file, 'table1', 'Power Info', power_dict )
    buildHtmlMainPageFooter(html_file)
    buildHtmlFooter(html_file)


def generate_host_interface_stats_page( log, phdl, html_file, cert_file=None ):
    #port_dict = penctl_lib.get_penctl_port_stats( phdl, cert_file=cert_file )
    intf_dict = penctl_lib.get_linux_interface_stats( log, phdl, cert_file )
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildAmchartHeader(html_file)

    generateTopNetworkBandwidthPieChart( html_file, intf_dict, 'tx_bytes', 10, 'toptxbw' )
    generateTopNetworkBandwidthPieChart( html_file, intf_dict, 'rx_bytes', 10, 'toprxbw' )

    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)

    chart_dict = OrderedDict([('chart2', {'title': 'Top 10 OS Interface Cumulative Tx Bandwidth', 'align': 'left', 'obj': 'toptxbw', 'width': 'full'}), ('chart3', {'title': 'Top 10 OS Cumulative Interface Rx Bandwidth', 'align': 'right', 'obj': 'toprxbw', 'width': 'full'})])

    buildHtmlDashboardCharts(html_file, chart_dict)
 
    generateOsInterfaceStatsTable( html_file, 'table1', 'OS Interface Cumulative Statistics', intf_dict )
    #generatePortStatsTable( html_file, 'table1', 'Uplink Statistics', port_dict )
    buildHtmlMainPageFooter(html_file)
    buildHtmlFooter(html_file)


def generate_os_interface_stats_page( log, phdl, int_mnic_ip_list, html_file ):
    intf_dict = penctl_lib.get_linux_interface_stats( phdl )
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)
    generateOsInterfaceStatsTable( html_file, 'table1', 'OS Interface Statistics', port_dict )
    buildHtmlMainPageFooter(html_file)
    buildHtmlFooter(html_file)


def generate_host_lldp_neighor_page( log, phdl, html_file ):
    lldp_dict = penctl_lib.get_lldp_neigh_dict( phdl ) 
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)
    print(lldp_dict)
    generateLldpNeighborTable( html_file, 'table1', 'LLDP Neighbor Table', lldp_dict )
    buildHtmlMainPageFooter(html_file)
    buildHtmlFooter(html_file)




# Generate Environmentals Page

# Generate Resource View Page

# Generate Network View Page 




def generate_dscs_nw_summary_page( log, phdl, html_file, dscs_dict, cert_file=None ):
  
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)
    generateDscTableviaNetwork( html_file, 'table1', 'DSC Summary', dscs_dict )
    buildHtmlFooter(html_file)



def generate_fwlog_analysis_page( log, phdl, html_file, summary_dict, fw_ep_dict, duration, cert_file=None ): 
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)
    #generateFwlogSummaryTable( html_file, 'table1', 'Firewall Log Analysis Summary for last {} Minutes'.format(duration), summary_dict )
    addWidgetHeader( html_file )
    addWidget( html_file, 'bg-aqua', 'Flows Created', summary_dict['total_flows_created'] )
    addWidget( html_file, 'bg-yellow', 'Flows Deleted', summary_dict['total_flows_deleted'] )
    addWidget( html_file, 'bg-red', 'Flows Denied', summary_dict['total_flows_denied'] )
    addWidget( html_file, 'bg-green', 'Avg Flows/Sec', summary_dict['avg_new_flows_per_sec'] )
    addWidgetFooter( html_file )
    generateFwlogEndpointTable( html_file, 'table2', 'Firewall Log Endpoint View for last {} Minutes'.format(duration), fw_ep_dict )
    buildHtmlFooter(html_file)


def generate_fte_cps_page( log, phdl, html_file, cps_dict, dscs_dict):
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)
    buildAmchartHeader(html_file)
    generateFteCpsChart(html_file, 'cpschart', 'Active Connections Per Second', cps_dict )
    generateFteMaxCpsChart(html_file, 'maxcpschart', 'History of Maximum Connections Per Second', cps_dict )
    chart_dict = OrderedDict([('chart2', {'title': 'Active Connections per Second', 'align': 'left', 'obj': 'cpschart', 'width': 'full'}), ('chart3', {'title': 'History of Max Connections per second', 'align': 'left', 'obj': 'maxcpschart', 'width': 'full'}) ])
    buildHtmlDashboardCharts(html_file, chart_dict)
    buildHtmlFooter(html_file)


def generate_link_utilization_page( log, phdl, html_file, stats_dict ):
    buildHtmlStart(html_file)
    buildHtmlHead(html_file)
    buildHtmlStyle(html_file)
    buildHtmlSideMenu(html_file)
    buildHtmlMainPageHeader(html_file)
    buildAmchartHeader(html_file)
    generateLinkUtilizationChart( html_file, stats_dict, 'tx', 'linkcharttx', 'Top 10 Tx Link Utilization', 10 )
    generateLinkUtilizationChart( html_file, stats_dict, 'rx', 'linkchartrx', 'Top 10 Rx Link Utilization', 10 )
    chart_dict = OrderedDict([('chart2', {'title': 'Top 10 Tx Link Utilization', 'align': 'left', 'obj': 'linkcharttx', 'width': 'full'}), ('chart3', {'title': 'Top 10 Rx Link Utilization', 'align': 'left', 'obj': 'linkchartrx', 'width': 'full'}) ])
    buildHtmlDashboardCharts(html_file, chart_dict)
    buildHtmlFooter(html_file)
  

def generate_dscs_detailed_page( log, phdl, html_dir, dscs_dict,  \
       arm_intf_dict, ep_dict, flow_dict, dscs_sessions_dict, dscs_drops_dict, \
       bw_dict, cert_file=None ):
    print('Generating DSC Detailed page')
    for dsc_ip in phdl.hosts:
        html_file = html_dir + '/' + 'dsc-db/' + 'dsc_' + dsc_ip + '.html'
        buildHtmlStart(html_file)
        buildSubPageHtmlHead(html_file)
        buildHtmlStyle(html_file)
        buildAmchartHeader(html_file)
        buildSubPageHtmlSideMenu(html_file)
        buildHtmlMainPageHeader(html_file)
        generateDscArmInterfaceTable( html_file, 'table2', 'ARM Interfaces', arm_intf_dict[dsc_ip])
        generateDscEndPointsTable( html_file, 'table3', 'WorkLoads Behind this DSC', ep_dict[dsc_ip] )
        generateDscBandwidthTable( html_file, 'table4', 'DSC Bandwidth Table', bw_dict[dsc_ip] )
        #print(flow_dict[dsc_ip])
        #print(dscs_dict[dsc_ip])
        print(dscs_dict)
        if re.search( 'ENFORCE', dscs_dict[dsc_ip]['policy-mode'], re.I ):
           generate3dDonutSessionSummaryChart( html_file, dscs_sessions_dict[dsc_ip], 'sessionschart' )
           generate3dDonutDropsChart( html_file, dscs_drops_dict[dsc_ip], 'dropschart' )
        if re.search( 'ENFORCE|FLOW', dscs_dict[dsc_ip]['policy-mode'], re.I ):
           print(flow_dict)
           generateFlowMapChart( html_file, flow_dict[dsc_ip], 'flowmap' )
        chart_dict = OrderedDict([('chart1', {'title': 'DSC Session Summary Statistics', 'align': 'left', 'obj': 'sessionschart', 'width': 'full'}),('chart2', {'title': 'DSC Drop Statistics', 'align': 'left', 'obj': 'dropschart', 'width': 'full'}),('chart3', {'title': 'DSC Flow level view', 'align': 'left', 'obj': 'flowmap', 'width': 'full'}) ])

        buildHtmlDashboardCharts(html_file, chart_dict)
        buildSubPageHtmlFooter(html_file)

         

def generate_host_dsc_port_page( log, phdl, html_file, cert_file=None ):
    port_dict = penctl_lib.get_penctl_port( phdl, cert_file=cert_file) 
    buildHtmlStart(html_file)
