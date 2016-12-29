[![Build Status](https://travis-ci.org/valentinmk/asynccmd.svg?branch=master)](https://travis-ci.org/valentinmk/asynccmd)
[![codecov](https://codecov.io/gh/valentinmk/asynccmd/branch/master/graph/badge.svg)](https://codecov.io/gh/valentinmk/asynccmd)
[![PyPI version](https://badge.fury.io/py/asynccmd.svg)](https://badge.fury.io/py/asynccmd)


[![PyPI](https://img.shields.io/pypi/dm/asynccmd.svg?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/l/asynccmd.svg?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/pyversions/asynccmd.svg?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/status/asynccmd.svg?style=flat-square)]()

# asynccmd
Async implementation of Cmd Python lib.

Asynccmd is a library to build command
line interface for you asyncio project.

It's very simple like original Cmd lib [https://docs.python.org/3.6/library/cmd.html](https://docs.python.org/3.6/library/cmd.html).

The mechanic is very similar. You have Cmd superclass, you can override class method and add yours own.

## Features
* support command line for Windows and POSIX systems
* build-in `help` or `?` command to list all available  command
* build-in `exit` command for emergency stop asyncio loop
* support repeat last cmd command by pressing up arrow

## Getting started


### Simple example
This is very simple example to show you main feature and how to use.

First of all, we are create new class and inherited  our `Cmd` class. Do not
instantiate `Cmd` itself.

Than create instance of this new class and run loop.
```Python
class SimpleCommander(Cmd):
    def __init__(self, mode, intro, prompt):
        super().__init__(mode=mode) # We need to pass in Cmd class mode of async cmd running
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
        self.loop = loop # We pass our loop to Cmd class. If None it try to get default asyncio loop.
        super().cmdloop(loop) # Create async tasks to run in loop. There is run_loop=false by default

# For win system we have only Run mode
# For POSIX system Reader mode is preferred
if sys.platform == 'win32':
   loop = asyncio.ProactorEventLoop()
   mode = "Run"
else:
   loop = asyncio.get_event_loop()
   mode = "Reader"
cmd = SimpleCommander(mode=mode, intro="This is example", prompt="example> ") #create instance
cmd.start(loop) #prepaire instanse
try:
    loop.run_forever() # our command line will run automatically from this point
except KeyboardInterrupt:
    loop.stop()
```
[Link to simple.py](https://github.com/valentinmk/asynccmd/blob/master/examples/simple.py)

### General example
We are use sipmle example, but adding some new staff:
* `sleep_n_print` coroutine that will be called from our cli command
* `do_sleep` new method (sleep cli command) that add task to event loop

```Python
async def sleep_n_print(loop, time_to_sleep = None):
    """
    This is our simple corutine.
    :param time_to_sleep: time to sleep in seconds
    :return: await sleep for time_to_sleep seconds
    """
    asyncio.set_event_loop(loop) #set correct event loop
    await asyncio.sleep(int(time_to_sleep))
    print("Wake up! I was slept for {0}s".format(time_to_sleep))
```

```Python
def do_sleep(self, arg):
    """
    Our example cmd-command-method for sleep. sleep <arg>
    :param arg: contain args that go after command
    :return: None
    """
    self.loop.create_task(sleep_n_print(self.loop, arg))
```
[Link to main.py](https://github.com/valentinmk/asynccmd/blob/master/examples/main.py)

Now we could run our cli. Let's make `sleep 10` command 3 times. Now we use `tasks`
command to see what is happen.

```bash
example>tasks
<Task pending coro=<sleep_n_print() running at asynccmd\examples\main.py:13> wait_for=<Future pending cb=[Task._wakeup()]>>
<Task pending coro=<Cmd._read_line() running at C:\Program Files\Python35\lib\site-packages\asynccmd\asynccmd.py:141>>
<Task pending coro=<sleep_n_print() running at asynccmd\examples\main.py:13> wait_for=<Future pending cb=[Task._wakeup()]>>
<Task pending coro=<sleep_n_print() running at asynccmd\examples\main.py:13> wait_for=<Future pending cb=[Task._wakeup()]>>
example>
Wake up! I was slept for 10s
Wake up! I was slept for 10s
Wake up! I was slept for 10s
```

### Aiohttp implementation
This is practical example control aiohttp instances. We will create two cli command
`start_server` and `stop_server`. This command get port number as only argument.
Let's make some changes for our general example:
TBD


## Documentation
TBD

## Contributing

Main stream is fork project, commit changes and send pull request.
For contributing to lib you could make in form of feedback, bug reports or pull requests.
CONTRIBUTING.md - TBD.

## Requirements
* Python >= 3.5

## License
`asynccmd` is offered under the Apache 2 license.

## Source code
The latest developer version is avalible at [https://github.com/valentinmk/asynccmd](https://github.com/valentinmk/asynccmd)
