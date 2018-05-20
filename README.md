# Dandelion Simulations

This repository contains files for simulating Dandelion routing and adversary
deanonymization attacks.

**Dependencies**

* Tested with Python 3.6.3
* `networkx` version 2.0

**How do I use this library?**

Simulation scripts that output data are prefixed with "main." To run one of
these scripts, execute `python3.6 main_<...>.py` from the appropriate directory
in the command line.

## Contents

* [Directory Contents](#directory-contents): A map of the project directory
* [License](#license)

## <a name="directory-contents"></a> Directory Contents

* **approx-2-regular-k**: Each node has exactly one outbound edge but a variable
  number of inbound edges. The adversary is given routing information.
* **approx-2-regular-u**: Each node has exactly one outbound edge but a variable
  number of inbound edges. The adversary is not given routing information.
* **approx-4-regular-k**: Each node has exactly two outbound edges but a
  variable number of inbound edges. The adversary is given routing information.
* **approx-4-regular-u**: Each node has exactly two outbound edges but a
  variable number of inbound edges. The adversary is not given routing
  information.
* **exact-2-regular-k**: Each node has exactly one outbound edge and exactly one
  inbound edge. The adversary is given routing information.
* **exact-2-regular-u**: Each node has exactly one outbound edge and exactly one
  inbound edge. The adversary is not given routing information.
* **exact-4-regular-k**: Each node has exactly two outbound edges and exactly
  two inbound edges. The adversary is given routing information.
* **exact-4-regular-u**: Each node has exactly two outbound edges and exactly
  two inbound edges. The adversary is not given routing information.
* **fingerprint-d1**: Simulates a fingerprint attack with one outbound edge per
  node, split into the number of messages observed per node.
* **fingerprint-d2**: Simulates a fingerprint attack with two outbound edges per
  node, split into the number of messages observed per node.
* **fingerprint-d4**: Simulates a fingerprint attack with four outbound edges
  per node, split into the number of messages observed per node.
* **fingerprint-d8**: Simulates a fingerprint attack with eight outbound edges
  per node, split into the number of messages observed per node.
* **LICENSE.txt**: License information
* **README.md**: This document

## <a name="license"></a> License

Written in 2017-2018 by Bradley Denby  

To the extent possible under law, the author(s) have dedicated all copyright and
related and neighboring rights to this work to the public domain worldwide. This
work is distributed without any warranty.

You should have received a copy of the CC0 Public Domain Dedication with this
work. If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.
