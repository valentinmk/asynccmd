|Build Status| |codecov| |PyPI version| |PyPI|

asynccmd
========

Async implementation of Cmd Python lib.

Asynccmd is a library to build command line interface for you asyncio
project.

It's very simple like original Cmd lib
https://docs.python.org/3.6/library/cmd.html.

The mechanic is very similar. You have Cmd superclass, you can override
class method and add yours own.

Features
--------

-  support command line for Windows and POSIX systems
-  build-in ``help`` or ``?`` command to list all available command
-  build-in ``exit`` command for emergency stop asyncio loop
-  support repeat last cmd command by sending empty string

Getting started
---------------

Simple example
~~~~~~~~~~~~~~

This is very simple example to show you main features and how they can
be used.

First of all, we are create new class and inherited our ``Cmd`` class.
Do not instantiate ``Cmd`` itself.

Than create instance of this new class and run loop.

.. code:: python

    class SimpleCommander(Cmd):
        def __init__(self, mode, intro, prompt):
            # We need to pass in Cmd class mode of async cmd running
            super().__init__(mode=mode)
            self.intro = intro
            self.prompt = prompt
            self.loop = None

        def do_tasks(self, arg):
            """
            Our example method. Type "tasks <arg>"
            :param arg: contain args that go after command
            :return: None
            """
            for task in asyncio.Task.all_tasks(loop=self.loop):
                print(task)

        def start(self, loop=None):
            # We pass our loop to Cmd class.
            # If None it try to get default asyncio loop.
            self.loop = loop
            # Create async tasks to run in loop. There is run_loop=false by default
            super().cmdloop(loop)

    # For win system we have only Run mode
    # For POSIX system Reader mode is preferred


    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        mode = "Run"
    else:
        loop = asyncio.get_event_loop()
        mode = "Reader"
    # create instance
    cmd = SimpleCommander(mode=mode, intro="This is example", prompt="example> ")
    cmd.start(loop)  # prepaire instance
    try:
        loop.run_forever()  # our cmd will run automatilly from this moment
    except KeyboardInterrupt:
        loop.stop()

`Link to
simple.py <https://github.com/valentinmk/asynccmd/blob/master/examples/simple.py>`__

General example
~~~~~~~~~~~~~~~

We use our sipmle example, but add some new staff: \* ``sleep_n_print``
coroutine that will be called from our cli command \* ``do_sleep`` new
method (sleep cli command) that add task to event loop

.. code:: python

    async def sleep_n_print(loop, time_to_sleep=None):
        """
        This is our simple corutine.
        :param time_to_sleep: time to sleep in seconds
        :return: await sleep for time_to_sleep seconds
        """
        asyncio.set_event_loop(loop)  # set correct event loop
        await asyncio.sleep(int(time_to_sleep))
        print("Wake up! I was slept for {0}s".format(time_to_sleep))

.. code:: python

    def do_sleep(self, arg):
        """
        Our example cmd-command-method for sleep. sleep <arg>
        :param arg: contain args that go after command
        :return: None
        """
        self.loop.create_task(sleep_n_print(self.loop, arg))

`Link to
main.py <https://github.com/valentinmk/asynccmd/blob/master/examples/main.py>`__

Run our cli and make ``sleep 10`` command 3 times. Now we have 3
``sleep_n_print`` async tasks in our event loop. If you use ``tasks``
command, you see something like that.

.. code:: shell

    example>tasks
    <Task pending coro=<sleep_n_print() running at asynccmd\examples\main.py:13> wait_for=<Future pending cb=[Task._wakeup()]>>
    <Task pending coro=<Cmd._read_line() running at C:\Program Files\Python35\lib\site-packages\asynccmd\asynccmd.py:141>>
    <Task pending coro=<sleep_n_print() running at asynccmd\examples\main.py:13> wait_for=<Future pending cb=[Task._wakeup()]>>
    <Task pending coro=<sleep_n_print() running at asynccmd\examples\main.py:13> wait_for=<Future pending cb=[Task._wakeup()]>>
    example>
    Wake up! I was slept for 10s
    Wake up! I was slept for 10s
    Wake up! I was slept for 10s

Aiohttp implementation
~~~~~~~~~~~~~~~~~~~~~~

This is practical example how to control aiohttp instances. We will
create two cli command ``start`` and ``stop``. This commands get port
number as only one argument. Let's make some changes for our general
example:

Create class helper that will be do all aiohttp staff for us.

.. code:: python

    class AiohttpCmdHelper:
        """
        Helper class that do all aiohttp start stop manipulation
        """
        port = 8080  # Default port
        loop = None  # By default loop is not set

        def __init__(self, loop, port):
            self.loop = loop
            self.port = port

        async def handle(self, request):
            """
            Simple handler that answer http request get with port and name
            """
            name = request.match_info.get('name', "Anonymous")
            text = 'Aiohttp server running on {0} port. Hello, {1}'.format(
                str(self.port), str(name))
            return web.Response(text=text)

        async def start(self):
            """
            Start aiohttp web server
            """
            self.app = web.Application()
            self.app.router.add_get('/', self.handle)
            self.app.router.add_get('/{name}', self.handle)
            self.handler = self.app.make_handler()
            self.f = self.loop.create_server(self.handler,
                                             host='0.0.0.0',
                                             port=self.port)
            # Event loop is already runing, so we await create server instead
            # of run_until_complete
            self.srv = await self.f

        async def stop(self):
            """
            Stop aiohttp server
            """
            self.srv.close()
            await self.srv.wait_closed()
            await self.app.shutdown()
            await self.handler.shutdown(60.0)
            await self.app.cleanup()

Now we ready to add ``start`` and ``stop`` command to ``Commander``.

.. code:: python

    # Add property to store helper objects
        aiohttp_servers = []
    # ...

    def do_start(self, arg):
        """
        Our example cli-command-method for start aiohttp server. start <arg>
        :param arg: Port number
        :return: None
        """
        if not arg:  # we use simple check in our demonstration
            print("Error port is empty")
        else:
            test = AiohttpCmdHelper(loop=self.loop, port=int(arg))
            self.aiohttp_servers.append({'port': int(arg),'server': test})
            self.loop.create_task(test.start())

    def do_stop(self, arg):
        """
        Our example cli-command-method for stop aiohttp server. start <arg>
        :param arg: Port number
        :return: None
        """
        if not arg:  # we use simple check in our demonstration
            print("Error! Provided port is empty")
        else:
            aiohttp_servers = []
            for srv in self.aiohttp_servers:
                if srv['port'] == int(arg):
                    self.loop.create_task(srv['server'].stop())
                else:
                    aiohttp_servers.append({'port': srv['port'], 'server': srv['server']})
            self.aiohttp_servers = aiohttp_servers

We need to add ``asyncio.set_event_loop(loop)`` addition to our main
example to prevent aiohttp to create its own loop.

.. code:: python

    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        mode = "Run"
    else:
        loop = asyncio.get_event_loop()
        mode = "Reader"

    asyncio.set_event_loop(loop)  # set our event loop for aiohttp (fix for Win32)

That's all. Now we can run multiple aiohttp server from our code.

`Link to
aiohttp\_example.py <https://github.com/valentinmk/asynccmd/blob/master/examples/aiohttp_example.py>`__

Documentation
-------------

TBD

Contributing
------------

Main stream is fork project, commit changes and send pull request.
Contributing to lib you could make in form of feedback, bug reports or
pull requests. CONTRIBUTING.md - TBD.

Requirements
------------

-  Python >= 3.5

License
-------

``asynccmd`` is offered under the Apache 2 license.

Source code
-----------

The latest developer version is avalible at
https://github.com/valentinmk/asynccmd

.. |Build Status| image:: https://travis-ci.org/valentinmk/asynccmd.svg?branch=master
   :target: https://travis-ci.org/valentinmk/asynccmd
.. |codecov| image:: https://codecov.io/gh/valentinmk/asynccmd/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/valentinmk/asynccmd
.. |PyPI version| image:: https://badge.fury.io/py/asynccmd.svg
   :target: https://badge.fury.io/py/asynccmd
.. |PyPI| image:: https://img.shields.io/pypi/status/asynccmd.svg
   :target:
