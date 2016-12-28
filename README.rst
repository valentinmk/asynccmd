asynccmd
===============
asynccmd Async implementation of cmd Python lib.


|Build Status| |codecov| |PyPI version| 

It’s very simple like original Cmd lib
https://docs.python.org/3.6/library/cmd.html.

The mechanic is very similar. You have Cmd class, you can override class
method and add yours own.

.. code:: python

    import asyncio
    import sys
    from asynccmd import Cmd

    class SimpleCommander(Cmd):
        def __init__(self, mode, intro, prompt):
            super().__init__(mode=mode)
            self.intro = intro
            self.prompt = prompt
            self.loop = None

        def do_tasks(self, arg):
            """
            Fake command. Type "tasks {arg}"
            :param arg: args occurred from cmd after command
            :return:
            """
            print(asyncio.Task.all_tasks(loop=self.loop))

        def start(self, loop=None):
            self.loop = loop
            super().cmdloop(loop)
            print(super().mode)

    if sys.platform == 'win32':
       loop = asyncio.ProactorEventLoop()
       mode = "Run"
    else:
       loop = asyncio.get_event_loop()
       mode = "Reader"
    cmd = SimpleCommander(mode=mode, intro="This is example", prompt="example> ")
    cmd.start(loop)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()

.. |Build Status| image:: https://travis-ci.org/valentinmk/asynccmd.svg?branch=master
   :target: https://travis-ci.org/valentinmk/asynccmd
.. |codecov| image:: https://codecov.io/gh/valentinmk/asynccmd/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/valentinmk/asynccmd
.. |PyPI version| image:: https://badge.fury.io/py/asynccmd.svg
   :target: https://badge.fury.io/py/asynccmd
