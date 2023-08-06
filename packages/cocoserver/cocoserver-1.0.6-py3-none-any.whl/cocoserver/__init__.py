from http import HTTPStatus
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import os
import sys
import email
import shutil
import datetime
import webbrowser
import urllib.parse
import importlib.metadata

__version__ = '1.0.6'

class GzipHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.logfile = kwargs.pop('logfile', None)
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        if self.logfile:
            message = format % args
            self.logfile.write("%s - - [%s] %s\n" %
                            (self.address_string(),
                            self.log_date_time_string(),
                            message.translate(self._control_char_table)))

    def send_head(self):
        """Common code for GET and HEAD commands.
        Overridden to provide a gzip'ed file if available.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        have_gz = False
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                # Insist that directory urls should end in '/'.
                # Otherwise redirect - doing basically what apache
                # does.
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index + '.gz') or os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        # Check for trailing "/" which should return 404 since
        # we have already handled directories and macOS does not
        # allow filenames to end in "/".
        if path.endswith("/"):
            self.send_error(HTTPStatus.NOT_FOUND,
                "File not found: %s" % path)
            return None
        try:
            f = open(path + '.gz', 'rb')
            have_gz = True
        except (FileNotFoundError, OSError):
            try:
                f = open(path, 'rb')
            except (FileNotFoundError, OSError):
                try:
                    self.send_error(HTTPStatus.NOT_FOUND,
                        "File not found: %s" % path)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                return None
        try:
            fs = os.fstat(f.fileno())
            # Use browser cache if possible
            if ("If-Modified-Since" in self.headers
                    and "If-None-Match" not in self.headers):
                # compare If-Modified-Since and time of last file modification
                try:
                    ims = email.utils.parsedate_to_datetime(
                        self.headers["If-Modified-Since"])
                except (TypeError, IndexError, OverflowError, ValueError):
                    # ignore ill-formed values
                    pass
                else:
                    if ims.tzinfo is None:
                        # obsolete format with no timezone, cf.
                        # https://tools.ietf.org/html/rfc7231#section-7.1.1.1
                        ims = ims.replace(tzinfo=datetime.timezone.utc)
                    if ims.tzinfo is datetime.timezone.utc:
                        # compare to UTC datetime of last modification
                        last_modif = datetime.datetime.fromtimestamp(
                            fs.st_mtime, datetime.timezone.utc)
                        # remove microseconds, like in If-Modified-Since
                        last_modif = last_modif.replace(microsecond=0)

                        if last_modif <= ims:
                            self.send_response(HTTPStatus.NOT_MODIFIED)
                            self.end_headers()
                            f.close()
                            return None

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(fs[6]))
            if have_gz:
                self.send_header("Content-Encoding", "gzip")
            self.send_header("Last-Modified",
                self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def copyfile(self, source, outputfile):
        try:
            shutil.copyfileobj(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            # Ignore exceptions when the browser closes the connection
            # while receiving a response. They seem to try again anyway.
            pass

class StaticServer:
    """Runs an HTTP server in a background thread.

    The server serves static files, possibly gzipped, from a specified
    root directory.
    """ 

    def __init__(self, root_dir, logfile=None):
        self.site_root = os.path.abspath(root_dir)
        self.httpd = None
        self.logfile = logfile
        if logfile and not hasattr(logfile, 'write'):
            raise ValueError('The logfile must have a write method.')
        
    def start(self):
        server_address = ('127.0.0.1', 0)
        handler = partial(GzipHTTPRequestHandler,
                              directory=self.site_root,
                              logfile=self.logfile)
        self.httpd = ThreadingHTTPServer(server_address, handler)
        self.server_thread = Thread(target=self.httpd.serve_forever,
                                        daemon=True)
        self.server_thread.start()

    def visit(self, path=''):
        if not self.httpd or not self.server_thread.is_alive():
            self.start()
        port = self.httpd.server_address[1]
        url = os.path.join('http://localhost:%s' % port, path)
        webbrowser.open_new_tab(url)
        
