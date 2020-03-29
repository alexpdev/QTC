#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qtc v0.2
##
## This code written for the "Qtc" program
##
## This project is licensed with:
## GNU AFFERO GENERAL PUBLIC LICENSE
##
## Please refer to the LICENSE file locate in the root directory of this
## project or visit <https://www.gnu.org/licenses/agpl-3.0 for more
## information.
##
## THE COPYRIGHT HOLDERS PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY
## KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
## THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH
## YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL
## NECESSARY SERVICING, REPAIR OR CORRECTION.
##
## IN NO EVENT ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
## CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
## INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
## OUT OF THE USE OR INABILITY TO USE THE PROGRAM EVEN IF SUCH HOLDER OR OTHER
## PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
###
######
################################################################################

import os
import json
from datetime import datetime,timedelta
from PyQt5.QtGui import QStandardItem
from Qtc.widgets import StandardItem
from PyQt5.QtChart import (QBarSeries, QBarSet, QChart, QValueAxis,
                            QBarCategoryAxis, QValueAxis, QLineSeries)
from PyQt5.QtCore import Qt

class ItemFactory:

    """ Factory Class for generating items for GUI tables. """

    def __init__(self):
        """ Calls `self.load_fields()` immediately and returns. """
        self.load_fields()


    def load_fields(self):
        """ loads field data from `fields.json` in the same directory. """
        path = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(path,"fields.json")
        fields = json.load(open(json_file))
        self.fields = fields
        self.funcs = {0 : self.convert_const,    1 : self.convert_bytes,
                      2 : self.convert_duration, 3 : self.convert_bps,
                      4 : self.convert_time,     5 : self.convert_isotime,
                      6 : self.convert_ratio,    7 : self.convert_delta}

    def gen_item(self,field,data):
        """ StandardItem factory function.

            Takes Item's Header label and corresponding data.
            Returns QStandardItem for TableView.
        """
        item = self.convert_data(field,data)
        return item

    def transform(self,field,data,display_data,label):
        item = StandardItem(display_data)
        item.set_value(data)
        item.set_field(field)
        item.set_label(label)
        item.set_display_value(display_data)
        item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        return item

    def convert_data(self,field,data):
        """ Function for converting raw data into more readable format. """

        label = self.get_label(field)
        idx = self.fields[field]["conv"]
        func = self.funcs[idx]
        display_data = func(data)
        data_item = self.transform(field,data,display_data,label)
        return data_item

    def get_label(self,field):
        """ Formats the db field to title case for table headers """
        label = self.fields[field]["label"]
        return label

    def convert_duration(self,data):
        """ Changes a datetime.timestamp integer to human readable format """
        now = datetime.now()
        d = datetime.fromtimestamp(data)
        return str(abs(now - d))

    def convert_bytes(self,data):
        """ Formats bytes to appropriate order of magnitude. e.g. GB MB. """
        val = data
        if val > 1_000_000_000:
            nval = str(round(val / 1_000_000_000,2))+"GB"
        elif val > 1_000_000:
            nval = str(round(val / 1_000_000,2))+"MB"
        elif val > 1000:
            nval = str(round(val / 1000,2))+"KB"
        else:
            nval = str(val)+" B"
        return nval

    def convert_bps(self,data):
        val = self.convert_bytes(data)
        val += "/s"
        return val

    def convert_const(self,data):
        return str(data)

    def convert_time(self,data):
        return str(datetime.fromtimestamp(data))

    def convert_ratio(self,data):
        return str(round(data,5))

    def convert_delta(self,data):
        data = int(data)
        d = timedelta(seconds=data)
        return str(d)

    def convert_isotime(self,data):
        return str(datetime.fromisoformat(data))

    def convert_stamp(self,timestamp):
        d = datetime.fromisoformat(timestamp)
        s = f"{d.month}/{d.day} ({d.hour}:{d.minute})"
        return s

    def compile_torrent_charts(self,db_rows):
        """ Factory method for generating charts.

            Input -> All database rows for a single torrent.
            Output -> Line and Bar Charts for Ratio and Upload.
        """
        line_series = QLineSeries()
        ul_series = QBarSeries()
        ratio_series = QBarSeries()
        ulset = QBarSet("Uploaded")
        ratioset = QBarSet("Ratio")

        """ Generate empty bar and line charts for data series.
        """

        seq = []
        ul_top, ratio_top = 0, 0
        ul_last, skip_count = 0,0
        for i,row in enumerate(db_rows):
            ul = row["uploaded"]
            ratio = row["ratio"]

            """ Compare current iteration to previous and skip if values
                most of the measured values are identical to avoid clutter.
            """
            if ul == ul_last and skip_count < 6:
                skip_count += 1
                continue
            skip_count = 0
            ul_last = ul
            if ul > ul_top:
                ul_top, ratio_top = ul, ratio
            ulset.append(ul)
            ratioset.append(ratio)

            """ Change IsoFormatted time into a more compact datetime format
            """
            stamp = self.convert_stamp(row["timestamp"])
            seq.append(stamp)
        ul_series.append(ulset)
        ratio_series.append(ratioset)
        line_chart = self.get_diff_chart(line_series,db_rows)
        ul_chart = self.form_chart(ul_series,"Uploaded",seq,ul_top)
        ratio_chart = self.form_chart(ratio_series,"Ratio",seq,ratio_top)
        return ul_chart, ratio_chart, line_chart

    def get_diff_chart(self,line_series,db_rows):
        top_val,counter,seq = 0,0,[]
        for diff in self.calculate_diffs(db_rows):
            stamp,ul,ratio = diff
            line_series.append(counter,ul)
            seq.append(str(stamp))
            if ul > top_val:
                top_val = ul
            counter += 1
        return self.form_chart(line_series,"Daily Upload",seq,top_val)


    def form_chart(self,series,title,cats,top_range):

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.AllAnimations)

        xaxis = QBarCategoryAxis()
        yaxis = QValueAxis()

        xaxis.append(cats)
        yaxis.setRange(0,top_range)

        chart.addAxis(xaxis,Qt.AlignBottom)
        chart.addAxis(yaxis,Qt.AlignLeft)

        series.attachAxis(xaxis)
        series.attachAxis(yaxis)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        return chart


    def calculate_diffs(self,rows):
        iso = lambda x: datetime.fromisoformat(x["timestamp"])
        rowsSrted = sorted(rows,key=iso)

        diffs,last_stamp,last_ul,last_ratio = [],None,None,None
        for row in rowsSrted:
            stamp = iso(row)
            ratio,ul = row["ratio"],row["uploaded"]

            if last_stamp:
                timediff = abs(stamp - last_stamp)
                uldiff = abs(ul - last_ul)
                ratiodiff = abs(ratio - last_ratio)
                yield (timediff, uldiff, ratiodiff)
            last_stamp, last_ul, last_ratio = stamp, ul, ratio
        return diffs
