# Access the Neutron Monitor database with python

![NMDB Logo](https://www.nmdb.eu/img/nmdb-6.png "NMDB")

This package provides python functions to access data from the
[Neutron Monitor database][nmdb].

# Installation

You can install directly from PyPI using
```
pip install nmdb
```

# Usage

- `nmdb_realtime` is an example to access realtime data,
as presented in a [tutorial][realtime] at the [NMDB hybrid conference in 2022][conf2022].

- `nmdb_nest_single` and `nmdb_nest_multi` are examples to get data from the
[NEST][nest] interface into a pandas dataframe.
These examples use the nest module from the nmdb package to generate html strings to query NEST.


--- 

[nmdb]: https://nmdb.eu
[realtime]: https://conf2022.nmdb.eu/abstract/s6/steigies/
[conf2022]: https://conf2022.nmdb.eu
[nest]: https://www.nmdb.eu/nest/

