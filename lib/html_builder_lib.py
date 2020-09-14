#!/usr/bin/env python3

import logging
import sys
import os
import re
import datetime
import glob
import operator

from collections import OrderedDict
import json
from heapq import nlargest

def buildHtmlStart(filename):
    fw = open( filename, 'w' )
    html_lines="""
    <!DOCTYPE html>
    <html>
    """
    fw.write(html_lines)
    fw.close()




def buildSubPageHtmlHead(filename):

    # Add Html Header to Page ..
    fw = open( filename, 'w' )
    html_lines="""
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Systest | Systest</title>
    <!-- Tell the browser to be responsive to screen width -->
    <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
    <!-- Bootstrap 3.3.7 -->
    <link rel="stylesheet" href="../bower_components/bootstrap/dist/css/bootstrap.min.css">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="../bower_components/font-awesome/css/font-awesome.min.css">
    <!-- Ionicons -->
    <link rel="stylesheet" href="../bower_components/Ionicons/css/ionicons.min.css">
    <link rel="stylesheet" href="../bower_components/datatables.net-bs/css/dataTables.bootstrap.min.css">
    <!-- Theme style -->
    <link rel="stylesheet" href="../dist/css/AdminLTE.min.css">
    <!-- AdminLTE Skins. Choose a skin from the css/skins
       folder instead of downloading all of them to reduce the load. -->
    <link rel="stylesheet" href="../dist/css/skins/_all-skins.min.css">
    <!-- Morris chart -->
    <link rel="stylesheet" href="../bower_components/morris.js/morris.css">
    <!-- jvectormap -->
    <link rel="stylesheet" href="../bower_components/jvectormap/jquery-jvectormap.css">
    <!-- Date Picker -->
    <link rel="stylesheet" href="../bower_components/bootstrap-datepicker/dist/css/bootstrap-datepicker.min.css">
    <!-- Daterange picker -->
    <link rel="stylesheet" href="../bower_components/bootstrap-daterangepicker/daterangepicker.css">
    <!-- bootstrap wysihtml5 - text editor -->
    <link rel="stylesheet" href="../plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.min.css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <!-- Google Font -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700,300italic,400italic,600italic">
    </head>"""
    fw.write(html_lines)
    fw.close()






def buildHtmlHead(filename):

    # Add Html Header to Page ..
    fw = open( filename, 'w' )
    html_lines="""
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Systest | Systest</title>
    <!-- Tell the browser to be responsive to screen width -->
    <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
    <!-- Bootstrap 3.3.7 -->
    <link rel="stylesheet" href="bower_components/bootstrap/dist/css/bootstrap.min.css">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="bower_components/font-awesome/css/font-awesome.min.css">
    <!-- Ionicons -->
    <link rel="stylesheet" href="bower_components/Ionicons/css/ionicons.min.css">
    <link rel="stylesheet" href="bower_components/datatables.net-bs/css/dataTables.bootstrap.min.css">
    <!-- Theme style -->
    <link rel="stylesheet" href="dist/css/AdminLTE.min.css">
    <!-- AdminLTE Skins. Choose a skin from the css/skins
       folder instead of downloading all of them to reduce the load. -->
    <link rel="stylesheet" href="dist/css/skins/_all-skins.min.css">
    <!-- Morris chart -->
    <link rel="stylesheet" href="bower_components/morris.js/morris.css">
    <!-- jvectormap -->
    <link rel="stylesheet" href="bower_components/jvectormap/jquery-jvectormap.css">
    <!-- Date Picker -->
    <link rel="stylesheet" href="bower_components/bootstrap-datepicker/dist/css/bootstrap-datepicker.min.css">
    <!-- Daterange picker -->
    <link rel="stylesheet" href="bower_components/bootstrap-daterangepicker/daterangepicker.css">
    <!-- bootstrap wysihtml5 - text editor -->
    <link rel="stylesheet" href="plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.min.css">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <!-- Google Font -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700,300italic,400italic,600italic">
    </head>"""
    fw.write(html_lines)
    fw.close()







def buildSubPageSideBarTreeMenu( filename ):

    fw = open( filename, 'a+')
    html_lines = """
        <li class="treeview">
           <a href="#">
            <i class="fa fa-laptop"></i> <span>Host Managed</span>
            <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
           </a>

              <ul class="treeview-menu">
              <li class="active"><a href="../host_dsc_summary.html"><i class="fa fa-circle-o"></i> <span>DSC Summary</span></a></li>
              <li class="treeview">
                  <a href="#"><i class="fa fa-bullseye"></i> Environmentals <span class="pull-right-container">
                  <i class="fa fa-angle-left pull-right"></i>
                  </span>
                  </a>
                  <ul class="treeview-menu">
                     <li><a href="../host_mgm_temperature.html"><i class="fa fa-circle-o"></i> Temperature</a></li>
                     <li><a href="../host_mgm_power.html"><i class="fa fa-circle-o"></i> Power</a></li>
                     <li><a href="http://10.30.5.9:3000/dashboard/db/dietemperature-host.html"><i class="fa fa-circle-o"></i> Thermal Time Series</a></li>
                  </ul>
              </li>
              <li class="treeview">
              <a href="#"><i class="fa fa-bullseye"></i> Use Cases <span class="pull-right-container">
                  <i class="fa fa-angle-left pull-right"></i>
                  </span>
                  </a>
                  <ul class="treeview-menu">
                     <li><a href="../host_lldp_summary.html"><i class="fa fa-circle-o"></i> LLDP DB</a></li>
                     <li><a href="../host_interface_stats_summary.html"><i class="fa fa-circle-o"></i> Traffic Stats</a></li>
                     <li><a href="http://10.30.5.9:3000/dashboard/db/interface_stats"><i class="fa fa-circle-o"></i> Time Series Stats</a></li>
              </ul>


             </ul>

            </li>

         </li>


        <li class="treeview">
           <a href="#">
            <i class="fa fa-laptop"></i> <span>NW Managed</span>
            <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
           </a>

              <ul class="treeview-menu">

              <li class="active"><a href="../dscs_nw_summary.html"><i class="fa fa-circle-o"></i> DSCs Summary</a></li>

              <li class="treeview">
                  <a href="#"><i class="fa fa-bullseye"></i> Top N Cases <span class="pull-right-container">
                  <i class="fa fa-angle-left pull-right"></i>
                  </span>
                  </a>
                  <ul class="treeview-menu">
                     <li><a href="../link_utilization.html"><i class="fa fa-circle-o"></i> Link Utilization</a></li>
                     <li><a href="../dscs_cps.html"><i class="fa fa-circle-o"></i> Connections/sec</a></li>
                  </ul>
              </li>


             </ul>

         </li>
        <li class="treeview">
           <a href="#">
            <i class="fa fa-laptop"></i> <span>NW Managed - PSM</span>
            <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
           </a>

              <ul class="treeview-menu">

              <li class="active"><a href="../fw_log_analysis.html"><i class="fa fa-circle-o"></i> FW Log Analysis</a></li>
              </ul>
         </li>





"""

    fw.write(html_lines)
    fw.close()









def buildSideBarTreeMenu( filename ):

    fw = open( filename, 'a+')
    html_lines = """
        <li class="treeview">
           <a href="#">
            <i class="fa fa-laptop"></i> <span>Host Managed</span>
            <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
           </a>

              <ul class="treeview-menu">

              <li class="active"><a href="host_dsc_summary.html"><i class="fa fa-circle-o"></i> <span>DSC Summary</span></a></li>

              <li class="treeview">
                  <a href="#"><i class="fa fa-bullseye"></i> Environmentals <span class="pull-right-container">
                  <i class="fa fa-angle-left pull-right"></i>
                  </span>
                  </a>
                  <ul class="treeview-menu">
                     <li><a href="host_temperature.html"><i class="fa fa-circle-o"></i> Temperature</a></li>
                     <li><a href="host_power.html"><i class="fa fa-circle-o"></i> Power</a></li>
                     <li><a href="http://10.30.5.9:3000/dashboard/db/dietemperature-host.html"><i class="fa fa-circle-o"></i> Thermal Time Series</a></li>
                  </ul>
              </li>

              <li class="treeview">
              <a href="#"><i class="fa fa-bullseye"></i> Use Cases <span class="pull-right-container">
                  <i class="fa fa-angle-left pull-right"></i>
                  </span>
                  </a>
                  <ul class="treeview-menu">
                     <li><a href="host_lldp_summary.html"><i class="fa fa-circle-o"></i> LLDP DB</a></li>
                     <li><a href="host_interface_stats_summary.html"><i class="fa fa-circle-o"></i> Traffic Stats</a></li>
                     <li><a href="http://10.30.5.9:3000/dashboard/db/interface_stats"><i class="fa fa-circle-o"></i> Time Series Stats</a></li>
              </ul>


             </ul>

            </li>

         </li>


        <li class="treeview">
           <a href="#">
            <i class="fa fa-laptop"></i> <span>NW Managed</span>
            <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
           </a>

              <ul class="treeview-menu">

              <li class="active"><a href="dscs_nw_summary.html"><i class="fa fa-circle-o"></i> DSCs Summary</a></li>

              <li class="treeview">
                  <a href="#"><i class="fa fa-bullseye"></i> Top N Cases <span class="pull-right-container">
                  <i class="fa fa-angle-left pull-right"></i>
                  </span>
                  </a>
                  <ul class="treeview-menu">
                     <li><a href="link_utilization.html"><i class="fa fa-circle-o"></i> Link Utilization</a></li>
                     <li><a href="dscs_cps.html"><i class="fa fa-circle-o"></i> Connections/sec</a></li>
                  </ul>
              </li>


             </ul>

            </li>

        <li class="treeview">
           <a href="#">
            <i class="fa fa-laptop"></i> <span>NW Managed - PSM</span>
            <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
           </a>

              <ul class="treeview-menu">

              <li class="active"><a href="fw_log_analysis.html"><i class="fa fa-circle-o"></i> FW Log Analysis</a></li>
              </ul>
         </li>




    """

    fw.write(html_lines)
    fw.close()







def buildSubPageHtmlSideMenu(filename):

    fw = open( filename, 'a+')
    html_lines = """
    <body class="hold-transition skin-blue sidebar-mini">
    <div class="wrapper">

    <header class="main-header">
    <!-- Logo -->
    <a href="index2.html" class="logo">
      <!-- mini logo for sidebar mini 50x50 pixels -->
      <span class="logo-mini"><b>E</b>W</span>
      <!-- logo for regular state and mobile devices -->
      <span class="logo-lg"><b>Pen</b>Apps</span>
    </a>
    <!-- Header Navbar: style can be found in header.less -->
    <nav class="navbar navbar-static-top">
      <!-- Sidebar toggle button-->
      <a href="#" class="sidebar-toggle" data-toggle="push-menu" role="button">
        <span class="sr-only">Toggle navigation</span>
      </a>
    """
    fw.write(html_lines)

    html_lines = '''

     <div class="navbar-custom-menu">
         <div>
           <img src="../bower_components/Ionicons/png/512/Pensando_light_logo.png" alt="*" height="50" width="120">
         </div>
     </div>
    </nav>
  </header>
  <!-- Left side column. contains the logo and sidebar -->
  <!-- Left side column. contains the logo and sidebar -->

  <aside class="main-sidebar">
    <!-- sidebar: style can be found in sidebar.less -->
    <section class="sidebar">
      <!-- Sidebar user panel -->
      <!-- search form -->
      <form action="#" method="get" class="sidebar-form">
        <div class="input-group">
          <input type="text" name="q" class="form-control" placeholder="Search...">
          <span class="input-group-btn">
                <button type="submit" name="search" id="search-btn" class="btn btn-flat"><i class="fa fa-search"></i>
                </button>
              </span>
        </div>
      </form>
      <!-- /.search form -->
      <!-- sidebar menu: : style can be found in sidebar.less -->
      <ul class="sidebar-menu" data-widget="tree">
        <li class="header">MAIN NAVIGATION</li>

    '''
    fw.write(html_lines)
    fw.close()


    buildSubPageSideBarTreeMenu( filename )


    fw = open( filename, 'a+')
    html_lines = """
    </li>
    </section>
    <!-- /.sidebar -->
    </aside>
    """
    fw.write(html_lines)
    fw.close()




def buildHtmlSideMenu(filename):

    fw = open( filename, 'a+')
    html_lines = """
    <body class="hold-transition skin-blue sidebar-mini">
    <div class="wrapper">

    <header class="main-header">
    <!-- Logo -->
    <a href="index2.html" class="logo">
      <!-- mini logo for sidebar mini 50x50 pixels -->
      <span class="logo-mini"><b>E</b>W</span>
      <!-- logo for regular state and mobile devices -->
      <span class="logo-lg"><b>Pen</b>Apps</span>
    </a>
    <!-- Header Navbar: style can be found in header.less -->
    <nav class="navbar navbar-static-top">
      <!-- Sidebar toggle button-->
      <a href="#" class="sidebar-toggle" data-toggle="push-menu" role="button">
        <span class="sr-only">Toggle navigation</span>
      </a>
    """
    fw.write(html_lines)


    html_lines = '''
     <div class="navbar-custom-menu">
         <div>
           <img src="./bower_components/Ionicons/png/512/Pensando_light_logo.png" alt="*" height="50" width="120">
         </div>
     </div>
    </nav>
  </header>
  <!-- Left side column. contains the logo and sidebar -->
  <!-- Left side column. contains the logo and sidebar -->

  <aside class="main-sidebar">
    <!-- sidebar: style can be found in sidebar.less -->
    <section class="sidebar">
      <!-- Sidebar user panel -->
      <!-- search form -->
      <form action="#" method="get" class="sidebar-form">
        <div class="input-group">
          <input type="text" name="q" class="form-control" placeholder="Search...">
          <span class="input-group-btn">
                <button type="submit" name="search" id="search-btn" class="btn btn-flat"><i class="fa fa-search"></i>
                </button>
              </span>
        </div>
      </form>
      <!-- /.search form -->
      <!-- sidebar menu: : style can be found in sidebar.less -->
      <ul class="sidebar-menu" data-widget="tree">
        <li class="header">MAIN NAVIGATION</li>
    '''
    fw.write(html_lines)
    fw.close()


    buildSideBarTreeMenu( filename )


    fw = open( filename, 'a+')
    html_lines = """
    </li>
    </section>
    <!-- /.sidebar -->
    </aside>
    """
    fw.write(html_lines)
    fw.close()




# bg-green, bg-yellow, bg-red
def addWidget( filename, bg_type, widget_text, widget_value,  ):
    fw = open( filename, 'a+' )
    html_lines = '''
        <!-- Beginning of Widget -->
        <div class="col-lg-3 col-xs-3">
          <!-- small box -->
          <div class="small-box ''' + bg_type + '''">
            <div class="inner">
              <h3>''' + str(widget_value) + '''</h3>
             <p>''' + str(widget_text) + '''</p>
            </div>
          </div>
        <!-- End of Widget -->
        </div> '''
    fw.write(html_lines)
    fw.close()




def addWidgetHeader( filename ):
    fw = open( filename, 'a+' )
    html_lines = """
    <!-- row Begninning -->
    <div class="row">
    """
    fw.write(html_lines)
    fw.close()

def addWidgetFooter( filename ):
    fw = open( filename, 'a+' )
    html_lines="""
    <!-- row end -->
     </div>
    """
    fw.write(html_lines)
    fw.close()




def buildSubPageHtmlFooter( filename ):
    # Add Html Footer to Page ..
    fw = open( filename, 'a+' )
    html_lines = """

    <!-- jQuery 3 -->
<script src="../bower_components/jquery/dist/jquery.min.js"></script>
<!-- jQuery UI 1.11.4 -->
<script src="../bower_components/jquery-ui/jquery-ui.min.js"></script>
<!-- Resolve conflict in jQuery UI tooltip with Bootstrap tooltip -->
<script>
  $.widget.bridge('uibutton', $.ui.button);
</script>
<!-- Bootstrap 3.3.7 -->
<script src="../bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
<!-- DataTables -->
<script src="../bower_components/datatables.net/js/jquery.dataTables.min.js"></script>
<script src="../bower_components/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>

<!-- Morris.js charts -->
<script src="../bower_components/raphael/raphael.min.js"></script>
<!-- Sparkline -->
<script src="../bower_components/jquery-sparkline/dist/jquery.sparkline.min.js"></script>
<!-- jvectormap -->
<script src="../plugins/jvectormap/jquery-jvectormap-1.2.2.min.js"></script>
<script src="../plugins/jvectormap/jquery-jvectormap-world-mill-en.js"></script>
<!-- jQuery Knob Chart -->
<script src="../bower_components/jquery-knob/dist/jquery.knob.min.js"></script>
<!-- daterangepicker -->
<script src="../bower_components/moment/min/moment.min.js"></script>
<script src="../bower_components/bootstrap-daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="../bower_components/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js"></script>
<!-- Bootstrap WYSIHTML5 -->
<script src="../plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.all.min.js"></script>
<!-- Slimscroll -->
<script src="../bower_components/jquery-slimscroll/jquery.slimscroll.min.js"></script>
<!-- FastClick -->
<script src="../bower_components/fastclick/lib/fastclick.js"></script>
<!-- AdminLTE App -->
<script src="../dist/js/adminlte.min.js"></script>
<!-- AdminLTE dashboard demo (This is only for demo purposes) -->
<script src="../dist/js/pages/dashboard.js"></script>
<!-- AdminLTE for demo purposes -->
<script src="../dist/js/demo.js"></script>
<script>
  $(function () {
    $('#table1').DataTable({
     "pageLength": 25,
     "scrollX": true,
     "autoWidth": true
    })
    $('#table2').DataTable({
     "pageLength": 25,
     "scrollX": true,
     "autoWidth": true
    })
    $('#table3').DataTable({
     "pageLength": 25,
     "scrollX": true,
     "autoWidth": true
    })
    $('#table4').DataTable()
    $('#table5').DataTable()
    $('#table50').DataTable({
     "pageLength": 50,
     "scrollX": true,
     "autoWidth": true
    })
    $('#table100').DataTable({
     "pageLength": 100,
     "scrollX": true,
     "autoWidth": true
    })
  })
</script>

    </body>
    </html>
    """
    fw.write(html_lines)
    fw.close()






def buildHtmlFooter( filename ):
    # Add Html Footer to Page ..
    fw = open( filename, 'a+' )
    html_lines = """

    <!-- jQuery 3 -->
<script src="bower_components/jquery/dist/jquery.min.js"></script>
<!-- jQuery UI 1.11.4 -->
<script src="bower_components/jquery-ui/jquery-ui.min.js"></script>
<!-- Resolve conflict in jQuery UI tooltip with Bootstrap tooltip -->
<script>
  $.widget.bridge('uibutton', $.ui.button);
</script>
<!-- Bootstrap 3.3.7 -->
<script src="bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
<!-- DataTables -->
<script src="bower_components/datatables.net/js/jquery.dataTables.min.js"></script>
<script src="bower_components/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>

<!-- Morris.js charts -->
<script src="bower_components/raphael/raphael.min.js"></script>
<!-- Sparkline -->
<script src="bower_components/jquery-sparkline/dist/jquery.sparkline.min.js"></script>
<!-- jvectormap -->
<script src="plugins/jvectormap/jquery-jvectormap-1.2.2.min.js"></script>
<script src="plugins/jvectormap/jquery-jvectormap-world-mill-en.js"></script>
<!-- jQuery Knob Chart -->
<script src="bower_components/jquery-knob/dist/jquery.knob.min.js"></script>
<!-- daterangepicker -->
<script src="bower_components/moment/min/moment.min.js"></script>
<script src="bower_components/bootstrap-daterangepicker/daterangepicker.js"></script>
<!-- datepicker -->
<script src="bower_components/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js"></script>
<!-- Bootstrap WYSIHTML5 -->
<script src="plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.all.min.js"></script>
<!-- Slimscroll -->
<script src="bower_components/jquery-slimscroll/jquery.slimscroll.min.js"></script>
<!-- FastClick -->
<script src="bower_components/fastclick/lib/fastclick.js"></script>
<!-- AdminLTE App -->
<script src="dist/js/adminlte.min.js"></script>
<!-- AdminLTE dashboard demo (This is only for demo purposes) -->
<script src="dist/js/pages/dashboard.js"></script>
<!-- AdminLTE for demo purposes -->
<script src="dist/js/demo.js"></script>
<script>
  $(function () {
    $('#table1').DataTable({
     "pageLength": 25,
     "scrollX": true,
     "autoWidth": true
    })
    $('#table2').DataTable({
     "pageLength": 25,
     "scrollX": true,
     "autoWidth": true
    })
    $('#table3').DataTable({
     "pageLength": 25,
     "scrollX": true,
     "autoWidth": true
    })
    $('#table4').DataTable()
    $('#table5').DataTable()
    $('#table50').DataTable({
     "pageLength": 50,
     "scrollX": true,
     "autoWidth": true
    })
    $('#table100').DataTable({
     "pageLength": 100,
     "scrollX": true,
     "autoWidth": true
    })
  })
</script>

    </body>
    </html>
    """
    fw.write(html_lines)
    fw.close()





def buildHtmlStyle(filename):
    fw = open(filename, 'a+')
    html_lines = """
    <style>
       pre {
       font-size: inherit;
       color: inherit;
       border: initial;
       padding: initial;
       white-space: pre;
       font-family: inherit;
    }
    th, td {
       padding: 3px;
       font-size: 10pt;
    }
    </style>
    """
    fw.write(html_lines)
    fw.close()


def buildHtmlMainPageHeader(filename):
    fw = open( filename, 'a+' )
    html_lines = '''
      <div class="content-wrapper">
      <!-- Main content -->
      <section class="content">'''
    fw.write(html_lines)
    fw.close()


def buildHtmlMainPageFooter(filename):
    fw = open( filename, 'a+' )
    html_lines = '''
      </section>
      <!-- /.content -->
      </div>'''
    fw.write(html_lines)
    fw.close()



def buildAmchartHeader(filename):
    fw = open(filename, 'a+')
    html_lines = """
      <!-- Resources -->
      <script src="https://www.amcharts.com/lib/3/amcharts.js"></script>
      <script src="https://www.amcharts.com/lib/3/pie.js"></script>
      <script src="https://www.amcharts.com/lib/3/plugins/export/export.min.js"></script>
      <script src="https://www.amcharts.com/lib/4/core.js"></script>
      <script src="https://www.amcharts.com/lib/4/charts.js"></script>
      <script src="https://www.amcharts.com/lib/4/plugins/timeline.js"></script>
      <script src="https://www.amcharts.com/lib/4/plugins/bullets.js"></script>
      <script src="https://www.amcharts.com/lib/4/themes/animated.js"></script>

      <link rel="stylesheet" href="https://www.amcharts.com/lib/3/plugins/export/export.css" type="text/css" media="all" />
      <script src="https://www.amcharts.com/lib/3/themes/light.js"></script>
      <!-- Chart code -->
    """
    fw.write(html_lines)
    fw.close()








def generateDscEndPointsTable( filename, table_id, table_title, ep_dict ):

    fw = open(filename, 'a+')
    html_lines = '''
    <!-- /.row -->
    <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">''' + table_title + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Enic Interface</th>
                  <th>Workload MAC</th>
                  <th>Enic Hdl</th>
                  <th>L2seg Hdl</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)
    for ep_mac in ep_dict.keys():
        html_lines = '''
              <tr>
                 <td>''' + str(ep_dict[ep_mac]['enic-intf']) + '''</td>
                 <td>''' + str(ep_mac) + '''</td>
                 <td>''' + str(ep_dict[ep_mac]['enic-hdl']) + '''</td>
                 <td>''' + str(ep_dict[ep_mac]['l2seg']) + '''</td>
              </tr>'''
        fw.write(html_lines)

    html_lines = '''
             </tbody>
             </table>
            </div>
          <!-- /.box-body -->
          </div>
          <!-- /.box -->
    '''
    fw.write(html_lines)
    fw.close()




def generateVeniceApiPerfTable( filename, table_id, table_title, perf_dict ):

    fw = open(filename, 'a+')
    html_lines = '''
    <!-- /.row -->
    <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">''' + table_title + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Object</th>
                  <th>Resource URI</th>
                  <th>Requests per Sec</th>
                  <th>Time per Request</th>
                  <th>Concurrent Requests</th>
                  <th>Failed Requests</th>
                  <th>Total Time</th>
                  <th>Longest Request</th>
                  <th>Transfer Rate</th>
                  <th>Total Transferred</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)
    for obj in perf_dict.keys():
        html_lines = '''
              <tr>
                 <td>''' + str(obj) + '''</td>
                 <td>''' + str(perf_dict[obj]['document-path']) + '''</td>
                 <td>''' + str(perf_dict[obj]['requests-per-sec']) + '''</td>
                 <td>''' + str(perf_dict[obj]['time-per-request']) + '''</td>
                 <td>''' + str(perf_dict[obj]['concurrent-requests']) + '''</td>
                 <td>''' + str(perf_dict[obj]['failed-requests']) + '''</td>
                 <td>''' + str(perf_dict[obj]['total-time']) + '''</td>
                 <td>''' + str(perf_dict[obj]['longest-request']) + '''</td>
                 <td>''' + str(perf_dict[obj]['transfer-rate']) + '''</td>
                 <td>''' + str(perf_dict[obj]['total-transferred']) + '''</td>
              </tr>'''
        fw.write(html_lines)

    html_lines = '''
             </tbody>
             </table>
            </div>
          <!-- /.box-body -->
          </div>
          <!-- /.box -->
    '''
    fw.write(html_lines)
    fw.close()








def generateDscBandwidthTable( filename, table_id, table_title, bw_dict ):

    fw = open(filename, 'a+')
    html_lines = '''
    <!-- /.row -->
    <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">''' + table_title + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Interface</th>
                  <th>Tx PPS</th>
                  <th>Tx BPS</th>
                  <th>Rx PPS</th>
                  <th>Rx BPS</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)
    for intf in bw_dict.keys():
        html_lines = '''
              <tr>
                 <td>''' + str(intf) + '''</td>
                 <td>''' + str(bw_dict[intf]['tx_pps']) + '''</td>
                 <td>''' + str(bw_dict[intf]['tx_bps']) + '''</td>
                 <td>''' + str(bw_dict[intf]['rx_pps']) + '''</td>
                 <td>''' + str(bw_dict[intf]['rx_bps']) + '''</td>
              </tr>'''
        fw.write(html_lines)

    html_lines = '''
             </tbody>
             </table>
            </div>
          <!-- /.box-body -->
          </div>
          <!-- /.box -->
    '''
    fw.write(html_lines)
    fw.close()







def generateDscArmInterfaceTable( filename, table_id, table_title, arm_intf_dict ):

    fw = open(filename, 'a+')
    html_lines = '''
    <!-- /.row -->
    <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">''' + table_title + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Interface</th>
                  <th>Mac Addr</th>
                  <th>IP Addr</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)
    for intf in arm_intf_dict.keys():
        html_lines = '''
              <tr>
                 <td>''' + str(intf) + '''</td>
                 <td>''' + str(arm_intf_dict[intf]['mac_addr']) + '''</td>
                 <td>''' + str(arm_intf_dict[intf]['ip_addr']) + '''</td>
              </tr>'''
        fw.write(html_lines)

    html_lines = '''
             </tbody>
             </table>
            </div>
          <!-- /.box-body -->
          </div>
          <!-- /.box -->
    '''
    fw.write(html_lines)
    fw.close()






def generateFwlogSummaryTable( filename, table_id, table_title, summary_dict ):
    fw = open(filename, 'a+')
    html_lines = '''
    <!-- /.row -->
    <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">''' + table_title + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Total Log Records</th>
                  <th>Flows Created</th>
                  <th>Flows Deleted</th>
                  <th>Flows Denied</th>
                  <th>New Flows per sec</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)

    print(summary_dict)
    html_lines = '''
                <tr>
                <td>''' + str(summary_dict['total_fw_records']) + '''</a></td>
                <td>''' + str(summary_dict['total_flows_created']) + '''</a></td>
                <td>''' + str(summary_dict['total_flows_deleted']) + '''</a></td>
                <td>''' + str(summary_dict['total_flows_denied']) + '''</a></td>
                <td>''' + str(summary_dict['avg_new_flows_per_sec']) + '''</a></td>
                </tr>
                </table>
             </div>
          <!-- /.box-body -->
          </div>
          <!-- /.box -->
    '''
    fw.write(html_lines)
    fw.close()


def generateFwlogEndpointTable( filename, table_id, table_title, ep_dict ):
    fw = open(filename, 'a+')
    html_lines = '''
    <!-- /.row -->
    <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">''' + table_title + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>EndPoint IP</th>
                  <th>Flows Created</th>
                  <th>Flows Deleted</th>
                  <th>Flows Allowed</th>
                  <th>Flows Denied/Rejected</th>
                  <th>No Policy Enforced</th>
                  <th>Peer Endpoints</th>
                  <th>Protocol-Ports</th>
                  <th>Policy Rule Hash</th>
                  <th>Bytes</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)

    for ep_ip in ep_dict.keys():
        policy_rules_list = []
        html_lines = '''
              <tr>
                 <td>''' + str(ep_ip) + '''</a></td>
                 <td>''' + str(ep_dict[ep_ip]['flows_created']) + '''</td>
                 <td>''' + str(ep_dict[ep_ip]['flows_deleted']) + '''</td>
                 <td>''' + str(int(ep_dict[ep_ip]['action_allowed']/2)) + '''</td>
                 <td>''' + str(int(ep_dict[ep_ip]['action_denied'] + ep_dict[ep_ip]['action_rejected'])) + '''</td>
                 <td>''' + str(ep_dict[ep_ip]['action_none']) + '''</td>
                 <td>''' + str(ep_dict[ep_ip]['peer-endpoint-list']) + '''</td>
                 <td>''' + str(ep_dict[ep_ip]['protocol-dict']) + '''</td>
                 <td>''' + str(ep_dict[ep_ip]['rule-list']) + '''</td>
                 <td>''' + str('0') + '''</td>
              </tr>'''
        fw.write(html_lines)
    html_lines = '''
             </tbody>
             <tfoot>
             <tr>
                  <th>EndPoint IP</th>
                  <th>DSC Id</th>
                  <th>Session Count</th>
                  <th>Peer Endpoints</th>
                  <th>Protocol-Ports</th>
                  <th>Bytes</th>
                  <th>Policy Rules</th>
              </tr>
             </tfoot>
              </table>
            </div>
          <!-- /.box-body -->
          </div>
          <!-- /.box -->
    '''
    fw.write(html_lines)
    fw.close()

 



def generateDscTableviaNetwork( filename, table_id, table_title, dsc_dict ):
    fw = open(filename, 'a+')
    html_lines = '''
    <!-- /.row -->
    <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">''' + table_title + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>IP Addr</th>
                  <th>DSC ID</th>
                  <th>MAC</th>
                  <th>Product Name</th>
                  <th>Part No.</th>
                  <th>Serial No.</th>
                  <th>Mgmt IP</th>
                  <th>FW Version</th>
                  <th>FWD Mode</th>
                  <th>Policy Mode</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)

    for dsc_ip in dsc_dict.keys():
        html_lines = '''
              <tr>
                 <td><a href="./dsc-db/dsc_''' + dsc_ip + '''.html">''' + str(dsc_ip) + '''</a></td>
                 <td>''' + str(dsc_dict[dsc_ip]['dsc-id']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_ip]['mac-address']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_ip]['product-name']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_ip]['part-number']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_ip]['serial-number']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_ip]['mgmt-ip']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_ip]['fw-version']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_ip]['fwd-mode']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_ip]['policy-mode']) + '''</td>
              </tr>'''
        fw.write(html_lines)

    html_lines = '''
             </tbody>
             <tfoot>
             <tr>
                  <th>IP Addr</th>
                  <th>DSC ID</th>
                  <th>MAC</th>
                  <th>Product Name</th>
                  <th>Part No.</th>
                  <th>Serial No.</th>
                  <th>Mgmt IP</th>
                  <th>FW Version</th>
                  <th>FWD Mode</th>
                  <th>Policy Mode</th>
                </tr>
             </tfoot>
              </table>
            </div>
          <!-- /.box-body -->
          </div>
          <!-- /.box -->
    '''
    fw.write(html_lines)
    fw.close()

 



def generateDscTable( filename, table_id, table_title, dsc_dict ):
    fw = open(filename, 'a+')
    html_lines = '''
    <!-- /.row -->
    <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">''' + table_title + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>DSC-Name</th>
                  <th>Primary MAC</th>
                  <th>Host IP</th>
                  <th>Product Name</th>
                  <th>Part No</th>
                  <th>Managed Mode</th>
                  <th>FW Version</th>
                  <th>Uboot Version</th>
                  <th>Serial No</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)

    for dsc_id in dsc_dict.keys():
        html_lines = '''
              <tr>
                 <td>''' + str(dsc_dict[dsc_id]['dsc_name']) + '''</td>
                 <td>''' + str(dsc_id) + '''</td>
                 <td>''' + str(dsc_dict[dsc_id]['host_name']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_id]['product_name']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_id]['part_no']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_id]['managed_mode']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_id]['fw_version']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_id]['uboot_version']) + '''</td>
                 <td>''' + str(dsc_dict[dsc_id]['serial_no']) + '''</td>
              </tr>'''
        fw.write(html_lines)

    html_lines = '''
             </tbody>
             <tfoot>
             <tr>
                  <th>DSC-Name</th>
                  <th>Primary MAC</th>
                  <th>Host IP</th>
                  <th>Product Name</th>
                  <th>Part No</th>
                  <th>Serial No</th>
                  <th>Managed Mode</th>
                  <th>Device Profile</th>
              </tr>
             </tfoot>
              </table>
            </div>
          <!-- /.box-body -->
          </div>
          <!-- /.box -->
    '''
    fw.write(html_lines)
    fw.close()

 


def generatePortTable( filename, table_title, port_dict  ):
    fw = open(filename, 'a+')

    for host in port_dict.keys():
        html_lines = '''
            <!-- /.row -->
            <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">Port Info for Host ''' + host + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="''' + host + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Int Mnic</th>
                  <th>Port</th>
                  <th>Speed</th>
                  <th>FEC cfg</th>
                  <th>FEC Oper</th>
                  <th>AutoNeg Cfg</th>
                  <th>AutoNeg Oper</th>
                  <th>MTU</th>
                  <th>Admin Status</th>
                  <th>Oper Status</th>
                  <th>Transceiver</th>
                  <th>Tx Pause</th>
                  <th>Rx Pause</th>
                </tr>
                </thead>
                <tbody>
        '''
        fw.write(html_lines)

        for dsc_ip in port_dict[host].keys():
            for port in port_dict[host][dsc_ip].keys():
                html_lines = '''
                   <tr>
                   <td>''' + str(dsc_ip) + '''</td>
                   <td>''' + str(port) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['speed']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['fec_cfg']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['fec_oper']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['auto_cfg']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['auto_oper']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['mtu']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['admin_status']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['oper_status']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['transceiver']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['tx_pause']) + '''</td>
                   <td>''' + str(port_dict[host][dsc_ip][port]['rx_pause']) + '''</td>
                   </tr>'''
                fw.write(html_lines)

        html_lines = '''
             </tbody>
             </table>
             </div>
             <!-- /.box-body -->
             </div>
             <!-- /.box -->'''
        fw.write(html_lines)
    fw.close()





def generatePowerTable( filename, table_id, table_title, power_dict  ):
    fw = open(filename, 'a+')

    html_lines = '''
            <!-- /.row -->
            <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">Power Info''' + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
            <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Host</th>
                  <th>Int Mnic</th>
                  <th>Power In - Watts</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)


    for host in power_dict.keys():
        for dsc_ip in power_dict[host].keys():
            t_dict = power_dict[host][dsc_ip][0]
            html_lines = '''
                <tr>
                <td>''' + str(host) + '''</td>
                <td>''' + str(dsc_ip) + '''</td>
		<td>''' + str(float(t_dict['Pin']/1000)) + '''</td>
                </tr>'''
            fw.write(html_lines)

    html_lines = '''
           </tbody>
           </table>
           </div>
           <!-- /.box-body -->
           </div>
           <!-- /.box -->'''
    fw.write(html_lines)
    fw.close()

 


def generateTemperatureTable( filename, table_id, table_title, temp_dict  ):
    fw = open(filename, 'a+')

    html_lines = '''
            <!-- /.row -->
            <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">Temperature Info''' + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
            <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Host</th>
                  <th>Int Mnic</th>
                  <th>Local Temp - Celcius</th>
                  <th>Die Temp - Celcius</th>
                  <th>HBM Temp - Celcius</th>
                  <th>Qsfp Port1 Temp</th>
                  <th>Qsfp Port2 Temp</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)


    for host in temp_dict.keys():
        for dsc_ip in temp_dict[host].keys():
            t_dict = temp_dict[host][dsc_ip][0]
            html_lines = '''
                <tr>
                <td>''' + str(host) + '''</td>
                <td>''' + str(dsc_ip) + '''</td>
		<td>''' + str(t_dict['LocalTemperature']) + '''</td>
                <td>''' + str(t_dict['DieTemperature']) + '''</td>
                <td>''' + str(t_dict['HbmTemperature']) + '''</td>
                <td>''' + str(t_dict['QsfpPort1Temperature']) + '''</td>
                <td>''' + str(t_dict['QsfpPort2Temperature']) + '''</td>
                </tr>'''
            fw.write(html_lines)

    html_lines = '''
           </tbody>
           </table>
           </div>
           <!-- /.box-body -->
           </div>
           <!-- /.box -->'''
    fw.write(html_lines)
    fw.close()

 



def generatePortStatsTable( filename, table_id, table_title, port_dict  ):
    fw = open(filename, 'a+')

    html_lines = '''
            <!-- /.row -->
            <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">Uplink Statistics''' + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
            <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Host</th>
                  <th>Int Mnic</th>
                  <th>Port</th>
                  <th>TX ALL</th>
                  <th>RX ALL</th>
                  <th>TX OK</th>
                  <th>RX OK</th>
                  <th>TX BAD</th>
                  <th>RX BAD</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)


    for host in port_dict.keys():
        for dsc_ip in port_dict[host].keys():
            for port in port_dict[host][dsc_ip].keys():
                p_dict = port_dict[host][dsc_ip][port]
                html_lines = '''
                   <tr>
                   <td>''' + str(host) + '''</td>
                   <td>''' + str(dsc_ip) + '''</td>
                   <td>''' + str(port) + '''</td>
		   <td>''' + str(p_dict['tx_all']) + '''</td>
		   <td>''' + str(p_dict['rx_all']) + '''</td>
		   <td>''' + str(p_dict['tx_ok']) + '''</td>
		   <td>''' + str(p_dict['rx_ok']) + '''</td>
		   <td>''' + str(p_dict['tx_bad']) + '''</td>
		   <td>''' + str(p_dict['rx_bad_all']) + '''</td>
                   </tr>'''
                fw.write(html_lines)

    html_lines = '''
           </tbody>
           </table>
           </div>
           <!-- /.box-body -->
           </div>
           <!-- /.box -->'''
    fw.write(html_lines)
    fw.close()




def generateLldpNeighborTable( filename, table_id, table_title, lldp_dict ):
    fw = open(filename, 'a+')

    html_lines = '''
            <!-- /.row -->
            <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">LLDP Neighbors''' + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
            <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Host</th>
                  <th>Host Interface</th>
                  <th>Peer Name</th>
                  <th>Peer Interface</th>
                  <th>Peer Mgmt IP</th>
                  <th>Peer Description</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)
    for host in lldp_dict.keys():
      for intf in lldp_dict[host].keys():
          html_lines = '''
           <tr>
           <td>''' + str(host) + '''</td>
           <td>''' + str(intf) + '''</td>
           <td>''' + str(lldp_dict[host][intf]['peer_name']) + '''</td>
           <td>''' + str(lldp_dict[host][intf]['peer_intf']) + '''</td>
           <td>''' + str(lldp_dict[host][intf]['peer_mgmt_ip']) + '''</td>
           <td>''' + str(lldp_dict[host][intf]['peer_desc']) + '''</td>
           </tr>'''
          fw.write(html_lines)

    html_lines = '''
           </tbody>
           </table>
           </div>
           <!-- /.box-body -->
           </div>
           <!-- /.box -->'''
    fw.write(html_lines)
    fw.close()






def generateOsInterfaceStatsTable( filename, table_id, table_title, port_dict  ):
    fw = open(filename, 'a+')

    html_lines = '''
            <!-- /.row -->
            <div class="box">
            <div class="box-header">
            <h3 class="box-title"><a name="''' + '''">OS Interface Statistics''' + '''</a></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
            <table id="''' + table_id + '''" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Host</th>
                  <th>Interface</th>
                  <th>TX Pkts</th>
                  <th>RX Pkts</th>
                  <th>TX Bytes</th>
                  <th>RX Bytes</th>
                  <th>TX Errors</th>
                  <th>RX Errors</th>
                  <th>TX Dropped</th>
                  <th>RX Dropped</th>
                </tr>
                </thead>
                <tbody>
    '''
    fw.write(html_lines)


    for host in port_dict.keys():
        for port in port_dict[host].keys():
                p_dict = port_dict[host][port]
                html_lines = '''
                   <tr>
                   <td>''' + str(host) + '''</td>
                   <td>''' + str(port) + '''</td>
		   <td>''' + str(p_dict['tx_pkts']) + '''</td>
		   <td>''' + str(p_dict['rx_pkts']) + '''</td>
		   <td>''' + str(p_dict['tx_bytes']) + '''</td>
		   <td>''' + str(p_dict['rx_bytes']) + '''</td>
		   <td>''' + str(p_dict['tx_errors']) + '''</td>
		   <td>''' + str(p_dict['rx_errors']) + '''</td>
		   <td>''' + str(p_dict['tx_dropped']) + '''</td>
		   <td>''' + str(p_dict['rx_dropped']) + '''</td>
                   </tr>'''
                fw.write(html_lines)

    html_lines = '''
           </tbody>
           </table>
           </div>
           <!-- /.box-body -->
           </div>
           <!-- /.box -->'''
    fw.write(html_lines)
    fw.close()




def generateFteMaxCpsChart( filename, chart_name, chart_title, cps_dict ):
    fw = open( filename, 'a+' )
    html_lines='''
<!-- Styles -->
<style>
#''' + chart_name + ''' {
  width: 100%;
  height: 500px;
}

</style>


<!-- Chart code -->
<script>
am4core.ready(function() {

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

var chart = am4core.create("''' + chart_name + '''", am4charts.XYChart);
chart.padding(40, 40, 40, 40);

var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.dataFields.category = "dsc";
categoryAxis.renderer.minGridDistance = 1;
categoryAxis.renderer.inversed = true;
categoryAxis.renderer.grid.template.disabled = true;

var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
valueAxis.min = 0;

var series = chart.series.push(new am4charts.ColumnSeries());
series.dataFields.categoryY = "dsc";
series.dataFields.valueX = "maxcps";
series.tooltipText = "{valueX.value}"
series.columns.template.strokeOpacity = 0;
series.columns.template.column.cornerRadiusBottomRight = 5;
series.columns.template.column.cornerRadiusTopRight = 5;

var labelBullet = series.bullets.push(new am4charts.LabelBullet())
labelBullet.label.horizontalCenter = "left";
labelBullet.label.dx = 10;
labelBullet.label.text = "{values.valueX.workingValue.formatNumber('#.0as')}";
labelBullet.locationX = 1;

// as by default columns of the same series are of the same color, we add adapter which takes colors from chart.colors color set
series.columns.template.adapter.add("fill", function(fill, target){
  return chart.colors.getIndex(target.dataItem.index);
});

categoryAxis.sortBySeries = series;
chart.data = ['''
    fw.write(html_lines)

    cps_per_sec_dict = {}
    for dsc_ip in cps_dict.keys():
        cps_per_sec_dict[dsc_ip] = cps_dict[dsc_ip]['FteCPSMetrics']['max_connections_per_second']
    sorted_cps_per_sec_dict = dict(sorted(cps_per_sec_dict.items(), key=operator.itemgetter(1),reverse=True))
    for dsc_ip in sorted_cps_per_sec_dict.keys():
        if sorted_cps_per_sec_dict[dsc_ip] != 0:
           html_lines = '''
           {
            "dsc": "''' + dsc_ip + '''",
            "maxcps": "''' + str(sorted_cps_per_sec_dict[dsc_ip]) + '''"
           },
           '''
           fw.write(html_lines)
    html_lines='''
    ]



    }); // end am4core.ready()
    </script>
    '''
    fw.write(html_lines)
    fw.close()





def generateFteCpsChart( filename, chart_name, chart_title, cps_dict ):
    fw = open( filename, 'a+' )
    html_lines='''
<!-- Styles -->
<style>
#''' + chart_name + ''' {
  width: 100%;
  height: 500px;
}

</style>


<!-- Chart code -->
<script>
am4core.ready(function() {

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

var chart = am4core.create("''' + chart_name + '''", am4charts.XYChart);
chart.padding(40, 40, 40, 40);

var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.dataFields.category = "dsc";
categoryAxis.renderer.minGridDistance = 1;
categoryAxis.renderer.inversed = true;
categoryAxis.renderer.grid.template.disabled = true;

var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
valueAxis.min = 0;

var series = chart.series.push(new am4charts.ColumnSeries());
series.dataFields.categoryY = "dsc";
series.dataFields.valueX = "cps";
series.tooltipText = "{valueX.value}"
series.columns.template.strokeOpacity = 0;
series.columns.template.column.cornerRadiusBottomRight = 5;
series.columns.template.column.cornerRadiusTopRight = 5;

var labelBullet = series.bullets.push(new am4charts.LabelBullet())
labelBullet.label.horizontalCenter = "left";
labelBullet.label.dx = 10;
labelBullet.label.text = "{values.valueX.workingValue.formatNumber('#.0as')}";
labelBullet.locationX = 1;

// as by default columns of the same series are of the same color, we add adapter which takes colors from chart.colors color set
series.columns.template.adapter.add("fill", function(fill, target){
  return chart.colors.getIndex(target.dataItem.index);
});

categoryAxis.sortBySeries = series;
chart.data = ['''
    fw.write(html_lines)

    cps_per_sec_dict = {}
    print(cps_dict)
    for dsc_ip in cps_dict.keys():
        cps_per_sec_dict[dsc_ip] = cps_dict[dsc_ip]['FteCPSMetrics']['connections_per_second']
    sorted_cps_per_sec_dict = dict(sorted(cps_per_sec_dict.items(), key=operator.itemgetter(1),reverse=True))
    for dsc_ip in sorted_cps_per_sec_dict.keys():
        if sorted_cps_per_sec_dict[dsc_ip] > 0:
           html_lines = '''
           {
            "dsc": "''' + dsc_ip + '''",
            "cps": "''' + str(sorted_cps_per_sec_dict[dsc_ip]) + '''"
           },
           '''
           fw.write(html_lines)
    html_lines='''
    ]



    }); // end am4core.ready()
    </script>
    '''
    fw.write(html_lines)
    fw.close()







def generateLinkUtilizationChart( filename, stats_dict, direction, chart_name, chart_title, top_n=10):
    fw = open( filename, 'a+')
    html_lines='''
    <style>
    #''' + chart_name + ''' {
      width: 100%;
      height: 450px;
    }
    </style>
    <script>
    am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create("''' + chart_name + '''", am4charts.XYChart3D);

    chart.titles.create().text = "''' + chart_title + '''";

    // Add data
    chart.data = [
    '''
    fw.write(html_lines)

    # Add logic to limit to top 10 Interfaces ..
    all_list = []
    for dsc_ip in stats_dict.keys():
        for intf in stats_dict[dsc_ip].keys():
            speed = stats_dict[dsc_ip][intf]['speed']
            intf_id =  dsc_ip + '_' + intf
            print(intf_id)
            if re.search( 'tx|Tx|TX', direction, re.I ):
               gbps = float(stats_dict[dsc_ip][intf]['txgbps'])
            elif re.search( 'rx|Rx|RX', direction, re.I ):
               gbps = float(stats_dict[dsc_ip][intf]['rxgbps'])
            util_percent = (gbps*100)/speed
            dict_item = { 'intf_id': intf_id, 'gbps': gbps, 'speed': speed, 'util_percent': util_percent }
            all_list.append(dict_item)

    print(all_list)
    top_n_list = nlargest( top_n, all_list, key=lambda item: item["util_percent"] )
    print(top_n_list)           

    for item_dict in top_n_list:
        html_lines = '''{
           "interface": "''' + str(item_dict['intf_id']) +  '''",
           "util_percent": ''' + str(item_dict['util_percent']) + ''',
           "bandwidth": ''' + str(item_dict['gbps']) + ''',
           "speed": ''' + str(item_dict['speed']) + '''
        },'''
        fw.write(html_lines)


    html_lines='''
    ];

    // Create axes
    let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "interface";
    categoryAxis.renderer.labels.template.rotation = 270;
    categoryAxis.renderer.labels.template.hideOversized = false;
    categoryAxis.renderer.minGridDistance = 20;
    categoryAxis.renderer.labels.template.horizontalCenter = "right";
    categoryAxis.renderer.labels.template.verticalCenter = "middle";
    categoryAxis.tooltip.label.rotation = 270;
    categoryAxis.tooltip.label.horizontalCenter = "right";
    categoryAxis.tooltip.label.verticalCenter = "middle";

let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.title.text = "Link Utilization %";
valueAxis.title.fontWeight = "bold";
valueAxis.min = 0;
valueAxis.max = 100;
// Create series
var series = chart.series.push(new am4charts.ConeSeries());
series.dataFields.valueY = "util_percent";
series.dataFields.valueY2 = "speed";
series.dataFields.valueY3 = "bandwidth";
series.dataFields.categoryX = "interface";
series.name = "LinkUtil";
//series.tooltipText = "{categoryX}: [bold]{valueY}[/]";
series.tooltipText = "{valueY}% of {valueY2}G: [bold]{valueY3}Gbps[/]";
series.columns.template.fillOpacity = .8;

var columnTemplate = series.columns.template;
columnTemplate.strokeWidth = 2;
columnTemplate.strokeOpacity = 1;
//columnTemplate.stroke = am4core.color("#FFFFFF");
columnTemplate.stroke = am4core.color("#8FFF");

chart.cursor = new am4charts.XYCursor();
chart.cursor.lineX.strokeOpacity = 0;
chart.cursor.lineY.strokeOpacity = 0;

}); // end am4core.ready()
</script>''' 
    fw.write(html_lines)
    fw.close()




def generate3dDonutSessionsChart( filename, data_dict, chart_name ):

    fw = open( filename, 'a+')
    html_lines='''
    <style>
    #''' + chart_name + ''' {
      width: 100%;
      height: 400px;
    }
    </style>
    <!-- Chart code -->
    <script>
    am4core.ready(function() {
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("''' + chart_name + '''", am4charts.PieChart3D);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

    chart.legend = new am4charts.Legend();

    chart.data = ['''
    fw.write(html_lines)

    for key_name in data_dict.keys():
        if key_name != "Key" or key_name != "total_active_sessions" or key_name != "num_aged_sessions":
           html_lines = '''{
            session: "''' + str(key_name) + '''",
            count: "''' + str(data_dict[key_name]) + '''"
           },'''
           if int(data_dict[key_name]) != 0:
              if not re.search( 'half_open_sessions', key_name, re.I ):
                 fw.write(html_lines)

    html_lines=''' 
    ];

    chart.innerRadius = 100;

    var series = chart.series.push(new am4charts.PieSeries3D());
    series.dataFields.value = "count";
    series.dataFields.category = "session";

    }); // end am4core.ready()
    </script>
    '''
    fw.write(html_lines)




def generate3dDonutSessionSummaryChart( filename, data_dict, chart_name ):
    
    fw = open( filename, 'a+')
    html_lines='''
    <style>
    #''' + chart_name + ''' {
      width: 100%;
      height: 500px;
    }
    </style>
    <!-- Chart code -->
    <script>
    am4core.ready(function() {
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("''' + chart_name + '''", am4charts.PieChart3D);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

    chart.legend = new am4charts.Legend();

    chart.data = ['''
    fw.write(html_lines)

    for key_name in data_dict.keys():
        html_lines = '''{
            session: "''' + str(key_name) + '''",
            count: "''' + str(data_dict[key_name]) + '''"
        },'''
        if int(data_dict[key_name]) != 0:
           fw.write(html_lines)

    html_lines=''' 
    ];

    chart.innerRadius = 100;

    var series = chart.series.push(new am4charts.PieSeries3D());
    series.dataFields.value = "count";
    series.dataFields.category = "session";

    }); // end am4core.ready()
    </script>
    '''
    fw.write(html_lines)
    fw.close()


def generate3dDonutDropsChart( filename, data_dict, chart_name ):
    
    fw = open( filename, 'a+')
    html_lines='''
    <style>
    #''' + chart_name + ''' {
      width: 100%;
      height: 500px;
    }
    </style>
    <!-- Chart code -->
    <script>
    am4core.ready(function() {
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create("''' + chart_name + '''", am4charts.PieChart3D);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

    chart.legend = new am4charts.Legend();

    chart.data = ['''
    fw.write(html_lines)

    for key_name in data_dict['DropMetrics'].keys():
        html_lines = '''{
            drop: "''' + str(key_name) + '''",
            count: "''' + str(data_dict['DropMetrics'][key_name]) + '''"
        },'''
        if int(data_dict['DropMetrics'][key_name]) != 0:
           fw.write(html_lines)

    html_lines=''' 
    ];

    chart.innerRadius = 100;

    var series = chart.series.push(new am4charts.PieSeries3D());
    series.dataFields.value = "count";
    series.dataFields.category = "drop";

    }); // end am4core.ready()
    </script>
    '''
    fw.write(html_lines)
    fw.close()





def generateFlowMapChart( filename, flow_dict, chart_name ):
    fw = open( filename, 'a+')
    html_lines='''
    <style>
    #flowmap {
      width: 100%;
      height: 750px;
    }
    </style>
    <script>
    var time = Date.now();
    am4core.useTheme(am4themes_animated);
    var chart = am4core.create("flowmap", am4charts.ChordDiagram);

    // colors of main characters
    chart.colors.saturation = 0.45;
    chart.colors.step = 3;
    var colors = {
    }
    chart.data = [
    '''
    fw.write(html_lines)

    print('%%%%%%%%%%%%%%%%%%%%%%')
    print(flow_dict)
    print('%%%%%%%%%%%%%%%%%%%%%%')
    for key in flow_dict.keys():
        src, dst, protocol = key.split("_")
        data = '''{"from":"''' + src + '-' + protocol + '''","to":"''' + dst + \
           '-' + protocol + \
           '''","value":''' + str(flow_dict[key]) + '''},\n'''
        fw.write(data)

    html_lines=''']

    chart.dataFields.fromName = "from";
    chart.dataFields.toName = "to";
    chart.dataFields.value = "value";


    chart.nodePadding = 0.5;
    chart.minNodeSize = 0.01;
    chart.startAngle = 80;
    chart.endAngle = chart.startAngle + 360;
    chart.sortBy = "value";

    var nodeTemplate = chart.nodes.template;
    nodeTemplate.readerTitle = "Click to show/hide or drag to rearrange";
    nodeTemplate.showSystemTooltip = true;
    nodeTemplate.propertyFields.fill = "color";
    nodeTemplate.tooltipText = "{name}'s flows: {total}";
    // when rolled over the node, make all the links rolled-over
    nodeTemplate.events.on("over", function (event) {    
    var node = event.target;
    node.outgoingDataItems.each(function (dataItem) {
        if(dataItem.toNode){
            dataItem.link.isHover = true;
            dataItem.toNode.label.isHover = true;
        }
    })
    node.incomingDataItems.each(function (dataItem) {
        if(dataItem.fromNode){
            dataItem.link.isHover = true;
            dataItem.fromNode.label.isHover = true;
        }
    }) 

    node.label.isHover = true;   
    })


    // when rolled out from the node, make all the links rolled-out
    nodeTemplate.events.on("out", function (event) {
    var node = event.target;
    node.outgoingDataItems.each(function (dataItem) {        
        if(dataItem.toNode){
            dataItem.link.isHover = false;                
            dataItem.toNode.label.isHover = false;
        }
    })
    node.incomingDataItems.each(function (dataItem) {
        if(dataItem.fromNode){
            dataItem.link.isHover = false;
           dataItem.fromNode.label.isHover = false;
        }
    })

    node.label.isHover = false;
    })


    var label = nodeTemplate.label;
    label.relativeRotation = 90;

    label.fillOpacity = 0.25;
    var labelHS = label.states.create("hover");
    labelHS.properties.fillOpacity = 1;

    nodeTemplate.cursorOverStyle = am4core.MouseCursorStyle.pointer;
    nodeTemplate.adapter.add("fill", function (fill, target) {
    var node = target;
    var counters = {};
    var mainChar = false;
    node.incomingDataItems.each(function (dataItem) {
        if(colors[dataItem.toName]){
            mainChar = true;
        }

        if(isNaN(counters[dataItem.fromName])){
            counters[dataItem.fromName] = dataItem.value;
        }
        else{
           counters[dataItem.fromName] += dataItem.value;
        }
    })
    if(mainChar){
        return fill;
    }

    var count = 0;
    var color;
    var biggest = 0;
    var biggestName;

    for(var name in counters){
        if(counters[name] > biggest){
            biggestName = name;
            biggest = counters[name]; 
        }        
    }
    if(colors[biggestName]){
        fill = colors[biggestName];
    }
  
    return fill;
    })

    // link template
    var linkTemplate = chart.links.template;
    linkTemplate.strokeOpacity = 0;
    linkTemplate.fillOpacity = 0.1;
    linkTemplate.tooltipText = "{fromName} to {toName} - {value} flows";

    var hoverState = linkTemplate.states.create("hover");
    hoverState.properties.fillOpacity = 0.7;
    hoverState.properties.strokeOpacity = 0.7;

    // data credit label
    var creditLabel = chart.chartContainer.createChild(am4core.TextLink);
    creditLabel.urlTarget = "_blank";
    creditLabel.y = am4core.percent(99);
    creditLabel.x = am4core.percent(99);
    creditLabel.horizontalCenter = "right";
    creditLabel.verticalCenter = "bottom";

    var titleImage = chart.chartContainer.createChild(am4core.Image);
    titleImage.text = "Flow mapping chart"
    titleImage.x = 30
    titleImage.y = 30;
    titleImage.width = 200;
    titleImage.height = 200;
    </script>'''
    fw.write(html_lines)
    fw.close()
 



def generateTopNetworkBandwidthPieChart( filename, intf_dict, stats_name, top_n, chart_name ):

    fw = open( filename, 'a+')
    lines='''
      <style>
      #''' + chart_name + '''{
      width: 100%;
      height: 650px;
      }
      </style>
      <script>
      var chart = AmCharts.makeChart( "''' + chart_name + '''", {
      "type": "pie",
      "theme": "light",
      "dataProvider": [
    '''
    fw.write(lines)
   
    stats_dict = {}
    for host in intf_dict.keys():
        print(intf_dict[host])
        for intf in intf_dict[host].keys():
            k = host + '-' + intf
            print(intf_dict[host])
            v = intf_dict[host][intf][stats_name]
            stats_dict[k] = int(v)

    top_list = sorted(stats_dict, key=stats_dict.get, reverse=True)[:top_n]
    for top_key in top_list:
        lines = """
          {
          "result_category": '""" + top_key + """',
          "count": """ + str(round(float(stats_dict[top_key])/(1024*1024*1024), 4 )) + ""","""
        fw.write(lines)
        lines = """
           },"""
        fw.write(lines)

    lines = """
    ],
    "valueField": "count",
    "titleField": "result_category",
    "colorField": "color",
    "startEffect": "elastic",
    "startDuration": 1,
    "labelRadius": 15,
    "labelText": "[[result_category]] - [[value]] GiB - ([[percents]]%)",
    "innerRadius": "50%",
    "depth3D": 30,
    "balloonText": "[[title]]<br><span style='font-size:14px'><b>[[value]] GiB</b> ([[percents]]%)</span>",
    "angle": 15,
    "export": {
    "enabled": true
    }
    } );
    </script>
    """
    fw.write(lines)
    fw.close()

 
        


def buildHtmlDashboardCharts(filename, chart_dict):

    fw = open( filename, 'a+' )

    print(chart_dict)

    # Iterate over every chart in the chart dict 
    for chart_no in chart_dict.keys():

        # If half width chart and left aligned ..
        if re.search( 'half', chart_dict[chart_no]['width'], re.I ):
           if re.search( 'right', chart_dict[chart_no]['align'], re.I ):
              html_lines = '''
                <div style="display: inline-block;">'''
              fw.write(html_lines)

           if re.search( 'left', chart_dict[chart_no]['align'], re.I ):
              html_lines = '''
                 <div class="row">
                 <div style="display: inline-block;">
                 <div class="col-md-6">'''
              fw.write(html_lines)

           html_lines = '''
                <div class="box box-primary" style="display: inline-block;">
                  <div class="box-header with-border">
                    <i class="fa fa-bar-chart-o"></i>
                    <h3 class="box-title">''' + chart_dict[chart_no]['title'] + '''</h3>
                    <div class="box-tools pull-right">
                <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-minus"></i> </button>
                <button type="button" class="btn btn-box-tool" data-widget="remove"><i class="fa fa-times"></i></button>
                </div>
                <div id="''' + chart_dict[chart_no]['obj'] + '''" style="height: 100%; width: 100%;overflow-y: scroll;overflow-x: scroll"></div> 
               </div>
              <!-- /.box-body-->
              </div>
            </div>'''
           fw.write(html_lines)

           if re.search( 'right', chart_dict[chart_no]['align'], re.I ):
              html_lines = '''
                  </div>
                  <!-- /.row -->
                  </div>'''
              fw.write(html_lines)

        else:
           # Entering full width charts - every div is a new row here ..
           html_lines = '''
              <div class="row">
                <div class="col-xs-12">
                  <div class="box box-primary">
                    <div class="box-header with-border">
                    <i class="fa fa-bar-chart-o"></i>
                      <h3 class="box-title">''' + chart_dict[chart_no]['title'] + '''</h3>
                      <div id="''' + chart_dict[chart_no]['obj'] + '''"></div>
                    </div>
                  </div>
                </div>
              </div>'''
           fw.write(html_lines)

    fw.close()
 
