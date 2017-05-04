tems-examples -- NodeJS
=======================

This is an example of the TEMS DAS catcher written in Javascript and running via the node interpreter.

Prerequisites
-------------

Before you can run this demo you need to make sure the following is true:

-	Have node V7.5 (or later) and npm installed on your system
-	Have an internet connection

Executing the programming
-------------------------

The first time you run the program you need to install all the dependencies it has. This is recorded in the package.json file and we use the npm utility to actually bring these dependencies down from the Internet.

```
npm install
```

You should now see a bunch of lines about it grabbing various packages.

To run the DAS server, we also use npm -- this time with the start command.

```
npm start
```

If all goes right you should see a start up log message indicating the DAS is listening for messages on port 3100 (unless ou changed that via the environment variables documented below)

Environment variables
---------------------

There are a few useful environment variables that can be set before running the DAS that adjusts its behavior slightly.

```
export TEMS_CATCHER_PORT=3100
```

This variable allows you to change which port # the DAS will listen to for TEMS events -- the default is 3100.

```
export TEMS_CREATE_REPLAY_FILE=1
```

Indicates if a replay file (see sim-replay) should be created for each TEMS message received. If this is set to true a replay file per tester will be created in the current working directory.

```
export TEMS_REPLAY_FILE_DIR=/some/path/to/a/writeable/dir
```

This over rides where any replay files will be stored if they are turned on above.
