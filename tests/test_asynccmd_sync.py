import pytest
import asyncio
import sys
from unittest import mock
from io import StringIO
#sys.path.append("..")
from asynccmd import Cmd

'''
#Skip for now
@pytest.mark.parametrize(("platform", "expected"), [
    ("linux", "<_WindowsSelectorEventLoop"),
    ("win32", "<ProactorEventLoop"),
])
def test_create_cmd_win(capsys, platform, expected):
    with capsys.disabled():
        platform_patcher = mock.patch('sys.platform',platform)
        platform_patcher.start()
        aio_cmd = Cmd(mode="Run", run_loop=False)
        aio_cmd.cmdloop()
        assert str(aio_cmd.loop).startswith(expected)
'''
@pytest.mark.parametrize(("platform", "expected"), [
    ("linux", "<_UnixSelectorEventLoop"),
])
def test_create_cmd(loop, platform, expected):
    platform_patcher = mock.patch('sys.platform',platform)
    platform_patcher.start()
    aio_cmd = Cmd(mode="Run", run_loop=False)
    aio_cmd.cmdloop(loop=loop)
    assert str(aio_cmd.loop).startswith(expected)

def test_lastcmd(loop):
    aio_cmd = Cmd(mode="Run", run_loop=False)
    aio_cmd.cmdloop(loop)
    aio_cmd._exec_cmd("?")
    assert aio_cmd.lastcmd == 'help '


@pytest.mark.parametrize(("command", "output"), [
    ("test", "Called buildin function do_test with args: \n"),
    ("help", "Default help handler. Have arg :  , but ignore its.\n\
Available command list: \n\
 -  exit\n\
 -  help\n\
 -  test\n"),
    ("?", "Default help handler. Have arg :  , but ignore its.\n\
Available command list: \n\
 -  exit\n\
 -  help\n\
 -  test\n"),
])
def test__exec_cmd(capsys, aio_cmd, command, output):
    aio_cmd._exec_cmd(command)
    out, err = capsys.readouterr()
    #sys.stdout.write(out)
    #sys.stderr.write(err)
    assert out == output
