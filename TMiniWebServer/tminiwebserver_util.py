import gc
import sys
from os import stat


class TMiniWebServerUtil:
    @staticmethod
    def unquote(s):
        r = str(s).split('%')
        try:
            b = r[0].encode()
            for i in range(1, len(r)):
                try:
                    b += bytes([int(r[i][:2], 16)]) + r[i][2:].encode()
                except:
                    b += b'%' + r[i].encode()
            return b.decode('UTF-8')
        except:
            return str(s)
    
    @staticmethod
    def unquote_plus(s):
        return TMiniWebServerUtil.unquote(s.replace('+', ' '))
    
    @staticmethod
    def escape_html(s):
        return ''.join(TMiniWebServerUtil._html_escape_chars.get(c,c) for c in s)


    @staticmethod
    def is_exist_file(path):
        result = False
        try:
            stat(path)
            result = True
        except Exception as ex:
            # sys.print_exception(ex)
            pass
        
        gc.collect()
        return result

    @staticmethod
    def get_minetype_from_ext(file_path):
        file_path = file_path.lower()
        for ext in TMiniWebServerUtil._mime_types:
            if file_path.endswith(ext):
                return TMiniWebServerUtil._mime_types[ext]
        return 'application/octet-stream'

    @staticmethod
    def get_file_size(path):
        try:
            info = stat(path)
            return info[6] ## file_size
        except Exception as ex:
            sys.print_exception(ex)
            return 0

    _html_escape_chars = {
        "&" : "&amp;",
        '"' : "&quot;",
        "'" : "&apos;",
        ">" : "&gt;",
        "<" : "&lt;"
    }

    _mime_types = {
        '.txt' : 'text/plain',
        '.htm' : 'text/html',
        '.html' : 'text/html',
        '.css' : 'text/css',
        '.csv' : 'text/csv',
        '.js' : 'application/javascript',
        '.xml' : 'application/xml',
        '.xhtml' : 'application/xhtml+xml',
        '.json' : 'application/json',
        '.zip' : 'application/zip',
        '.gz' : 'application/gzip',
        '.pdf' : 'application/pdf',
        '.tar' : 'application/x-tar',
        '.7z'  : 'application/x-7z-compressed',
        '.ts' : 'application/typescript',
        '.woff' : 'font/woff',
        '.woff2' : 'font/woff2',
        '.jpg' : 'image/jpeg',
        '.jpeg' : 'image/jpeg',
        '.png' : 'image/png',
        '.gif' : 'image/gif',
        '.svg' : 'image/svg+xml',
        '.ico' : 'image/x-icon',
        '.bin' : 'application/octet-stream'
    }

class HttpStatusCode:
    SWITCH_PROTOCOLS = 101
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206

    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    TEMPORARY_REDIRECT = 307

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    REQUEST_ENTITY_TOO_LARGE = 413
    REQUEST_URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417

    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
