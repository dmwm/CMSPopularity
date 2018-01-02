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

### Tasks:
In this project we'll follow the following
[tasks](https://docs.google.com/document/d/1XDkFkoPBvlKtb_jrQffWW-Qb16YpffsvIzNHyeh1dbw/edit)

### Refernces:
[CMS popularity](http://iopscience.iop.org/article/10.1088/1742-6596/898/9/092030/pdf)
[CMS data-management](http://iopscience.iop.org/article/10.1088/1742-6596/513/4/042052/pdf)
[CMSSpark](https://github.com/vkuznet/CMSSpark)
[PySpark](https://spark.apache.org/docs/latest/api/python/index.html)

