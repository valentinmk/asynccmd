import pytest
import asyncio
import sys
from unittest import mock
from io import StringIO
from asynccmd import Cmd


@pytest.mark.parametrize(("platform", "expected"), [
    ("win32", "<ProactorEventLoop"),
])
def test_create_cmd_win(platform, expected):
    platform_patcher = mock.patch('sys.platform',platform)
    platform_patcher.start()
    aio_cmd = Cmd(mode="Run", run_loop=False)

@pytest.mark.parametrize(("mode", "expected"), [
    ("Run", "help "),
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
])
def test__exec_cmd(capsys,aio_cmd, mode, command, output):
    aio_cmd._exec_cmd(command)
    out, err = capsys.readouterr()
    #sys.stdout.write(out)
    #sys.stderr.write(err)
    assert out == output
