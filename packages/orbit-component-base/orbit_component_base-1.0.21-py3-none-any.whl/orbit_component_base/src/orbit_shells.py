from threading import Thread
from loguru import logger as log
from time import sleep
from shutil import which
from asyncio import get_event_loop, create_task, run_coroutine_threadsafe, sleep
from subprocess import Popen, STDOUT
from pty import openpty
from signal import SIGINT
from termios import TIOCSWINSZ
from struct import pack
from fcntl import ioctl
import os
from orbit_component_base.src.orbit_plugin import PluginBase
from orbit_component_base.src.orbit_decorators import Sentry


class Session:

    def __init__ (self, sid=None, root=None, master=None, slave=None, process=None):
        self.sid = sid
        self.root = root
        self.master = master
        self.slave = slave
        self.process = process
        self.finished = False
    
    def keystroke (self, key):
        try:
            os.write (self.master, key)
            return True
        except OSError:
            log.debug('[looks like the shell died]')
            return False

    def resize (self, rows, cols):    
        try:
            winsize = pack("HHHH", rows, cols, 0, 0)
            ioctl(self.master, TIOCSWINSZ, winsize)
        except Exception as e:
            log.warning(f"Resize Error: {str(e)}")
    
    def close (self):
        try:
            self.finished = True
            os.close(self.slave)
            os.close(self.master)
            os.kill(self.process.pid, SIGINT)
            self.process.wait()
        except OSError:
            log.debug("<< Attempt to kill dead process>>")


class Sessions (dict):
    
    def __init__ (self, *args, **kwargs):
        self._by_sid = {}
        return super().__init__(*args, **kwargs)

    def shutdown (self, sid, key):
        session = self.get (f'{sid}|{key}')
        if session:
            session.close()
            del self[f'{sid}|{key}']
            self._by_sid[sid].remove(key)

    def add (self, sid, key, master, slave, process):
        self[f'{sid}|{key}'] = Session(sid, key, master, slave, process)
        if sid not in self._by_sid:
            self._by_sid[sid] = []
        self._by_sid[sid].append(key)
        create_task(self.monitor(sid, key))

    def resize (self, sid, key, rows, cols):
        session = self.get (f'{sid}|{key}')
        if not session:
            log.debug('attempt to resize non-existant session')
        else:
            session.resize (rows, cols)

    async def monitor (self, sid, key):
        session = self[f'{sid}|{key}']
        while True:
            if session.process.poll() is None:
                await sleep(1)
            else:
                return self.shutdown (sid, key)

    def flush (self, sid):
        if sid not in self._by_sid:
            log.error('attempt to flush missing session')
        else:
            for key in self._by_sid[sid]:
                self.shutdown(sid, key)


class Shells:
    
    def __init__ (self):
        self._sessions = Sessions()

    def get_session (self, sid, key):
        return self._sessions.get(f'{sid}|{key}')

    def shutdown (self, sid, key):
        self._sessions.shutdown(sid, key)

    def flush_session (self, sid):
        self._sessions.flush(sid)
        
    def resize (self, sid, key, rows, cols):
        self._sessions.resize (sid, key, rows, cols)
        
    def add_process (self, sid, key, exec):
        master, slave = openpty()
        executable = which(exec)
        if not executable:
            raise Exception('orbit database shell not found!')
        process = Popen(
            [executable],
            preexec_fn=os.setsid,
            stdin=slave,
            stdout=slave,
            close_fds=True,
            stderr=STDOUT)
        self._sessions.add(sid, key, master, slave, process)
        return self

    async def add_thread (self, sid, key, emitter):
        Thread(target=self.io_thread, args=(get_event_loop(), self._sessions[f'{sid}|{key}'], emitter), daemon=True).start()
        return self
    
    def io_thread (self, loop, session, emitter):
        try:
            while not session.finished:
                bytes = b''
                while True:
                    try:
                        chunk = os.read(session.master, 2048)
                        bytes += chunk
                        if bytes:
                            run_coroutine_threadsafe(
                                emitter.emit((f'data_{session.root}', {'sid': session.sid, 'data': bytes.decode()}))
                            , loop)
                            break
                    except UnicodeDecodeError as e:
                        log.error(f"Retry: len={len(bytes)}")
                        pass
                    except OSError:
                        log.warning ('[Shell IO interrupted]')
                        break
        except Exception as e:
            log.exception(e)

    async def add (self, sid, key, exec, emitter):
        if key not in self._sessions:
            await self.add_process(sid, key, exec).add_thread(sid, key, emitter)


class PluginXTerm (PluginBase):

    NAMESPACE = 'xterm'
    EXECUTABLE = '/bin/false'

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shells = Shells()
        self._executable = None      

    async def mount (self, sid, root, executable):
        log.warning(f"Mount: {sid}")
        self._executable = executable
        await self._shells.add(sid, root, executable, self._nql._emitter)
        return {'ok': True}            

    async def send_key (self, sid, root, key, force=False):
        session = self._shells.get_session(sid, root)
        if session:
            if session.keystroke (key.encode('utf-8')):
                return {'ok': True}
            self._shells.shutdown(root)
        return {'ok': False, 'error': 'No active session'}

    async def resize (self, sid, root, rows, cols):
        self._shells.resize(sid, root, rows, cols)
        return {'ok': True}            

    async def disconnect (self, sid):
        self._shells.flush_session(sid)
        await super().on_disconnect(sid)
        return {'ok': True}
    
    @Sentry()
    async def on_send_key (self, *args, **kwargs):
        return await self.send_key(*args, **kwargs)

    @Sentry()
    async def on_resize (self, *args, **kwargs):
        return await self.resize(*args, **kwargs)
            
    @Sentry()
    async def on_disconnect (self, *args, **kwargs):
        return await self.disconnect(*args, **kwargs)
