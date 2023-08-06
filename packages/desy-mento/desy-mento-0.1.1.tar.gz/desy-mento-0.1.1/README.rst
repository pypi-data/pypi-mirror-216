.. SPDX-FileCopyrightText: 2021 S. Vijay Kartik <vijay.kartik@desy.de>, DESY
..
.. SPDX-License-Identifier: CC-BY-4.0

.. |oa| replace:: ``MENTO``
.. _examples: /examples
.. _docs: /docs
.. _tests: /tests
.. _LICENSES: /LICENSES
.. _CITATION.cff: /CITATION.cff
.. _example.py: /examples/autoprocessing_during_daq.py

##################################################
|oa| - Trigger remote processing from the beamline
##################################################

|oa| is a Python (3.7+ only) package for automatically triggering online processing jobs like

#. remote data analysis, and
#. local visualization tasks,

right from the beamline.

The package contains modules and utility functions that automate the boring bits like

#. getting access to remote HPC resources
#. submitting slurm jobs to run online analysis

The package is designed to work on all PETRA III beamlines at DESY.

`Here is a short YouTube video <https://youtu.be/FpYnd3BKvag?t=335>`_ about the main uses of |oa|,
from a talk given at NOBUGS 2022.

Usage
=====

In its simplest form, |oa| can be used at a PETRA-III beamline to launch a data processing job on a remote
HPC (Maxwell) node, without needing to know how to connect to the HPC cluster Maxwell, or how to authenticate
without having a scientific account for Maxwell, or indeed how job submissions work.

A remote analysis program can be started on data acquired at the beamline, by a Python script importing a
|oa| module, creating a |oa| ``Trigger`` object and calling ``run()`` on it.

Here is a minimum working example::

    from mento import Trigger

    my_trigger = Trigger()  # default trigger will submit Slurm jobs on an HPC node

    my_analysis = 'maxwell_program.exe'  # path to analysis program available on Maxwell
    my_args = ['analysis', 'parameters', 'list', 'inputdatafile']  # arguments required by analysis program, including input data

    my_trigger.run([my_analysis, my_args])  # connect to a remote machine with appropriate credentials and start the analysis job there


Note that paths to input data files and output directories can be specified as you see them at
the beamline, and they will be automagically found in the remote core filesystem on Maxwell.

.. TODO: automatic conversion of local paths to remote paths is already present in mento.utils,
   but at the moment the utils functions need to be called by the user. We need to make this the
   default behaviour before we can claim automagic path conversions.

Paths to the analysis program on Maxwell, will of course need to refer to the 'remote' paths
as seen from a Maxwell node, since |oa| cannot know about them from the beamline.

A dummy example of running |oa| to do live data analysis during data acquisition is shown in example.py_.

Prerequisites for using |oa| for online data analysis
-----------------------------------------------------

When using Maxwell to perform the data analysis, |oa| uses Maxwell's Slurm system that manages access to
the compute nodes and schedules processing jobs according to the permissions and resources granted to the
user requesting the processing.
Depending on the resources allocated to the user running |oa|, processing jobs may be queued on Maxwell,
and run at a later time (or never).

Therefore, to have the data processing jobs run live at the same time as data acquisition during a beamtime,
the recommendation is to request 'online' resources on Maxwell at the time of starting the beamtime.
This is explained in detail in the DESY-IT/ASAP3 documentation
for starting beamtimes `here <https://confluence.desy.de/x/ZB8aDQ>`_.

Here is the short version: when starting your beamtime, use the following command to request an 'online' Maxwell
compute node which |oa| will then use to run remote data processing jobs::

    startBeamtime --beamtimeId 999999999 --beamline P9999 --online


(Replace the beamline and beamtime ID with your beamline and beamtime ID, of course).

If your data processing program needs a GPU, please also add ``--feature gpu`` to the startBeamtime command.

To request 'online' Maxwell resources for commissioning runs instead of user beamtimes, please use ``startComissioning``
with the same arguments as for ``startBeamtime`` (``--online`` and ``--feature``).


Customizations
==============

The |oa| trigger can be customized based on the beamline's needs. An example:

Online results visualization
------------------------------------------

For online visualization of results, we need to automatically run plotting programs *locally*.

This can be quickly achieved by created a customized trigger using

``my_trigger = Trigger(TriggerMethod.LOCAL_BASH_SCRIPT)``.

Calling ``run()`` on this trigger would then launch a visualization program (either directly or
wrapped inside a Bash script) locally.

Of course, the input arguments and the parameter list would also need to be appropriately modified.

Installation
============

At PETRA III beamlines, the easiest way to install the |oa| package would be to use ``pip``.
The package can be downloaded as an artifact from the Gitlab repository page, or used directly
in your ``pip`` command as follows::

    python3 -m pip install desy-mento



API documentation
=================
API documentation can be found in docs_.

The documentation is auto-generated, so it should be
as up-to-date as the comments in the source code. ;)

Contributing
============

Contributions in all forms are welcome - be it issues, bug reports, or code!

Citing
======

If you used |oa| and found it relevant to the work you are publishing, please consider citing the |oa|
introduction article that appears in the `SRI 2021 proceedings <https://dx.doi.org/10.1088/1742-6596/2380/1/012104>`_.

You can choose to either use the BibTeX citation given below,
or use the CITATION.cff_ file to export the citation to your favourite format (BibTeX/APA/RIS/EndNote/CodeMeta).

::

    @article{Vijay_Kartik_2022,
    doi = {10.1088/1742-6596/2380/1/012104},
    url = {https://dx.doi.org/10.1088/1742-6596/2380/1/012104},
    year = {2022},
    month = {dec},
    publisher = {IOP Publishing},
    volume = {2380},
    number = {1},
    pages = {012104},
    author = {S Vijay Kartik and Michael Sprung and Fabian Westermeier and Anton Barty},
    title = {MENTO: Automated near real-time data analysis at PETRA III},
    journal = {Journal of Physics: Conference Series},
    }

Licences
========

- All code is licensed under GPL-3.0-or-later
- All documentation is licensed under CC-BY-4.0
- All other files are licensed under CC0-1.0

Full texts of the licences can be found in LICENSES_.

This project aims to be `REUSE <https://reuse.software/>`_ compliant.

Contact
=======

For questions and critiques, please contact S. Vijay Kartik <vijay.kartik@desy.de>.
