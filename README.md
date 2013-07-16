Dev Tools Library [![Build Status](https://travis-ci.org/rocktavious/DevToolsLib.png)](https://travis-ci.org/rocktavious/DevToolsLib)
====================
Multiplatform tools development api

Installation
---------

```
$ pip install DTL
```

Usage
-----
```python
import DTL
#These are the core modules
from DTL import api, gui, db, networking, perforce
#This is where you can get access to package related settings
from DTL.settings import Settings

```

Design
------
The Dev Tools Library was designed to handle alot of bolier plate code, to free you up to design tools/scripts/applications without having to implement business logic and shared logic within the same tool/script/application.

It provides useful utilities and class in a number of different areas from general(api) to user interface(gui) even to communication(networking)