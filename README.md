# CMSPopularity
CMSPopularity is a community project to cover various aspects of CMS popularity via data-stream aggregation on HDFS.

### Introduction
We'll use [CMSSpark](https://github.com/vkuznet/CMSSpark) package to produce
and collect various metrics from HDFS. These metrics represent use activities
with various CMS data-services. For description of data-services and available
data please refer to CMSSpark package.

For previous effort to aggregated different metrics please refer to
summer student [reports](https://github.com/justinasr/CERNReports).

So far we feed data into CERN MONIT system with the following dashboards:
- [CMS popularity](https://monit-kibana.cern.ch/kibana/goto/5f1a88d69910666b61fedb6a1a0b74a1)
- [CMS popularity DN](https://monit-kibana.cern.ch/kibana/goto/ac711427f1c00ce7ccdd9e830a9f70de)
- [CNS popularity CPU](https://monit-kibana.cern.ch/kibana/goto/3613b07cce4a488d9a740267334a4de6)


Data Popularity Scrutiny Plot Specification

This histogram shows dataset usage by CMS jobs. The bins of the plot are labeled by number of accesses. One access is equal to reading 100% of the events or files in the dataset. The 1-bin includes any non-zero reading < 150% of the dataset. Higher accesses are rounded to the nearest integer. The 0-bin contains datasets created during the period but not used. The 0-old bin contains datasets created before the period but not used.

Each bin is broken into three sub-bins that cover the last three months, the last six months, and the full time period of the plot.

Each bin is weighted by the dataset sizes in the bin. The size calculation starts with the average replica size at a site, which is the daily weighted average size of the dataset during the time it is present at a site. Then the average sizes are summed for each day of the dataset’s lifetime over all the sites where replicas are located. This sum is divided by the number of days in the period to give an overall daily weighted average of the CMS disk space taken up by the dataset during the period.

The plot is usually limited to showing data for datasets on T1s and T2s.


### Tasks:
In this project we'll follow the following
[tasks](https://docs.google.com/document/d/1XDkFkoPBvlKtb_jrQffWW-Qb16YpffsvIzNHyeh1dbw/edit)

### References:
[CMS popularity](http://iopscience.iop.org/article/10.1088/1742-6596/898/9/092030/pdf)
[CMS data-management](http://iopscience.iop.org/article/10.1088/1742-6596/513/4/042052/pdf)
[CMSSpark](https://github.com/vkuznet/CMSSpark)
[PySpark](https://spark.apache.org/docs/latest/api/python/index.html)

