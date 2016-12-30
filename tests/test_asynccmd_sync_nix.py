# Copyright (c) 2016-present Valentin Kazakov
#
# This module is part of asyncpg and is released under
# the Apache 2.0 License: http://www.apache.org/licenses/LICENSE-2.0

import pytest
from unittest import mock
from asynccmd import Cmd


@pytest.mark.parametrize(("platform", "expected"), [
    ("linux", "<_UnixSelectorEventLoop"),
])
def test_create_cmd(loop, platform, expected):
    platform_patcher = mock.patch('sys.platform', platform)
    platform_patcher.start()
    aio_cmd = Cmd(mode="Run", run_loop=False)
    aio_cmd.cmdloop(loop=loop)
    assert str(aio_cmd.loop).startswith(expected)


@pytest.mark.parametrize(("mode", "expected"), [
    ("Run", "help "),
    # ("Reader", "help "),
])
def test_lastcmd(loop, mode, expected):
    aio_cmd = Cmd(mode=mode, run_loop=False)
    aio_cmd.cmdloop(loop)
    aio_cmd._exec_cmd("?")
    assert aio_cmd.lastcmd == 'help '


@pytest.mark.parametrize(("mode", "command", "output"), [
    ("Run", "test", "Called buildin function do_test with args: \n"),
    ("Run", "help", "Default help handler. Have arg :  , but ignore its.\n\
Available command list: \n\
 -  exit\n\
 -  help\n\
 -  test\n"),
    ("Run", "?", "Default help handler. Have arg :  , but ignore its.\n\
Available command list: \n\
 -  exit\n\
 -  help\n\
 -  test\n"),
    # ("Reader", "test", "Called buildin function do_test with args: \n"),
    # ("Reader", "help", "Default help handler. Have arg :  , but ignore its.\n\
    # Available command list: \n\
    #  -  exit\n\
    #  -  help\n\
    #  -  test\n"),
    #     ("Reader", "?", "Default help handler. Have arg :  , but ignore its.\n\
    # Available command list: \n\
    #  -  exit\n\
    #  -  help\n\
    # -  test\n"),
])
def test__exec_cmd(capsys, aio_cmd, mode, command, output):
    aio_cmd._exec_cmd(command)
    out, err = capsys.readouterr()
    # sys.stdout.write(out)
    # sys.stderr.write(err)
    assert out == output
