# Copyright (c) 2016-present Valentin Kazakov
#
# This module is part of asyncpg and is released under
# the Apache 2.0 License: http://www.apache.org/licenses/LICENSE-2.0
#
# This lib is inspired by Cmd standart lib Python >3.5 (under Python Software
# Foundation License 2)

import asyncio
import string
import sys
from contextlib import suppress


class Cmd:
    """
    TODO: need documentation
    TODO: need to review
    TODO: need to refactor in doc like ->
    TODO: need to refactor protected methods
    Reader not supported in Win32

    """
    loop = None  # asyncio.get_even_loop()
    mode = "Reader"  # Reader:loop.add_reader OR Run:loop.run_in_executor
    run_loop = False  # True: loop.run_forever OR False: no run event loop
    prompt = "asynccmd > "  # Str: it would writen before input
    intro = "asynccmd ready to serve"  # Str: intro message before cli start
    currentcmd = ""  # Str: currentcmd that catch
    lastcmd = ""  # Str: last cmd command
    allowedchars = string.ascii_letters + string.digits + '_'
    stdin = sys.stdin
    stdout = sys.stdout

    #
    # CMD command section
    #

    @staticmethod
    def do_test(arg):
        print("Called buildin function do_test with args:", arg)

    def do_help(self, arg):
        print("Default help handler. Have arg :", arg, ", but ignore its.")
        print("Available command list: ")
        for i in dir(self.__class__):
            if i.startswith("do_"):
                print(" - ", i[3:])

    def do_exit(self, arg):
        print("Rescue exit!!")
        raise KeyboardInterrupt

    #
    # Cmd section
    #

    def __init__(self, mode="Reader", run_loop=False):
        self.mode = mode
        self.run_loop = run_loop

    def cmdloop(self, loop=None):
        self._start_controller(loop)

    def _start_controller(self, loop):
        """
        Control structure to start new cmd
        :param loop: event loop
        :return: None
        """
        # Loop check
        if loop is None:
            if sys.platform == 'win32':
                self.loop = asyncio.ProactorEventLoop()
            else:
                self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop
        # Starting by add "tasks" in "loop"
        if self.mode == "Reader":
            self._start_reader()
        elif self.mode == "Run":
            self._start_run()
        else:
            raise TypeError("self.mode is not Reader or Run.")
        # Start or not loop.run_forever
        if self.run_loop:
            try:
                print("Cmd._start_controller start loop inside Cmd object!")
                self.stdout.flush()
                self.loop.run_forever()
            except KeyboardInterrupt:
                print("Cmd._start_controller stop loop. Bye.")
                self.loop.stop()
                pending = asyncio.Task.all_tasks(loop=self.loop)
                print(asyncio.Task.all_tasks(loop=self.loop))
                for task in pending:
                    task.cancel()
                    with suppress(asyncio.CancelledError):
                        self.loop.run_until_complete(task)
                # self.loop.close()

    def _start_run(self):
        if self.loop is None:
            raise TypeError("self.loop is None.")
        self.loop.create_task(self._read_line())
        self.loop.create_task(self._greeting())

    def _start_reader(self):
        if self.loop is None:
            raise TypeError("self.loop is None.")
        self.loop.add_reader(self.stdin.fileno(), self.reader)
        self.loop.create_task(self._greeting())

    def reader(self):
        line = sys.stdin.readline()
        self._exec_cmd(line)
        sys.stdout.write(self.prompt)
        sys.stdout.flush()

    async def _read_line(self):
        while True:
            line = await self.loop.run_in_executor(None, sys.stdin.readline)
            self._exec_cmd(line)
            print(self.prompt)
            sys.stdout.flush()
    #
    # Additional methods for work with input
    #

    def _exec_cmd(self, line):
        command, arg, line = self.parseline(line=line)
        if not line:
            return self._emptyline(line)
        if command is None:
            return self._default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if command == '':
            return self._default(line)
        else:
            try:
                func = getattr(self, 'do_' + command)
            except AttributeError:
                return self._default(line)
            except KeyboardInterrupt:
                return func(arg)
            return func(arg)

    def parseline(self, line):
        line = line.strip()
        if not line:
            return None, None, line
        elif line[0] == '?':
            line = 'help ' + line[1:]
        elif line[0] == '!':
            if hasattr(self, 'do_shell'):
                line = 'shell ' + line[1:]
            else:
                return None, None, line
        iline, nline = 0, len(line)
        while iline < nline and line[iline] in self.allowedchars:
            iline += 1
        command = line[:iline]
        arg = line[iline:].strip()
        return command, arg, line

    @staticmethod
    def _default(line):
        print("Invalid command: ", line)

    async def _greeting(self):
        print(self.intro)
        self.stdout.write(self.prompt)
        self.stdout.flush()

    def _emptyline(self, line):
        """
        handler for empty line if entered.
        :param line: this is unused arg (TODO: remove)
        :return: None
        """
        if self.lastcmd:
            print("Empty line. Try to repeat last command.", line)
            self._exec_cmd(self.lastcmd)
            return
        else:
            print("Empty line. Nothing happen.", line)
            return
