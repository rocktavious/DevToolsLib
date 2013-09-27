Dev Tools Library(DTL): Multiplatform tools development api
=========================

.. image:: https://badge.fury.io/py/DTL.png
    :target: http://badge.fury.io/py/DTL

.. image:: https://travis-ci.org/rocktavious/DTL.png?branch=master
        :target: https://travis-ci.org/rocktavious/DTL

.. image:: https://pypip.in/d/DTL/badge.png
        :target: https://crate.io/packages/DTL/
        
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