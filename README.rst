Dev Tools Library
=================

.. image:: https://badge.fury.io/py/DTL.png
    :target: http://badge.fury.io/py/DTL

.. image:: https://travis-ci.org/rocktavious/DevToolsLib.png?branch=master
        :target: https://travis-ci.org/rocktavious/DevToolsLib

.. image:: https://pypip.in/d/DTL/badge.png
        :target: https://crate.io/packages/DTL/
        
Dev Tools Library is a multiplatform tools development api, targeted to help keep you focused on writing the tools and not the connective glue code between packages.
        
Installation
------------

.. code-block:: bash
        
        pip install DTL

Usage
-----

.. code-block:: pycon
        
        >>> import DTL
        >>> #These are the core modules
        >>> from DTL import api, gui, db, networking, perforce
        >>> #This is where you can get access to package related settings
        >>> from DTL.settings import Settings
        ...

Design
------

The Dev Tools Library was designed to handle alot of bolier plate code, to free you up to design tools/scripts/applications without having to implement business logic and shared logic within the same tool/script/application.

It provides useful utilities and class in a number of different areas from general(api) to user interface(gui) even to communication(networking)

Documentation
-------------

