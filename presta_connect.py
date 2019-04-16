# -*- coding: utf-8 -*-
# Copyright 2019 Subteno IT
# License MIT License

import requests
import xmltodict
import string
import random
import io


class PrestaConnectError(RuntimeError):
    pass


class PrestaConnect:
    _BOUNDARY_CHARS = string.digits + string.ascii_letters
    _STATUSES = (200, 201)

    def __init__(self, api, key):
        self.api = api
        self.key = key

    def _get_url(self, path):
        return self.api + '/' + path

    def _check_response(self, res, ret):
        if res.status_code not in self._STATUSES:
            raise PrestaConnectError('Status %s, %s' % (res.status_code, ret))
        return ret

    def _encode_multipart_formdata(self, files):
        """Encode files to an http multipart/form-data.
        :param files: a sequence of (type, filename, value)
             elements for data to be uploaded as files.
        :return: headers and body.
        """
        BOUNDARY = (''.join(random.choice(self._BOUNDARY_CHARS) for i in range(30)))
        CRLF = b'\r\n'
        L = []
        for (key, filename, value) in files:
            L.append(bytes(('--' + BOUNDARY).encode('utf8')))
            L.append(
                bytes(('Content-Disposition: form-data; \
                   name="%s"; filename="%s"' % (key, filename)).encode('utf8')))
            L.append(bytes(('Content-Type: %s' % self._get_content_type(filename)).encode('utf8')))
            L.append(b'')
            L.append(value)
        L.append(bytes(('--' + BOUNDARY + '--').encode('utf8')))
        L.append(b'')
        body = CRLF.join(L)
        headers = {
            'Content-Type': 'multipart/form-data; boundary=%s' % BOUNDARY
        }
        return headers, body

    def add(self, path, data):
        return self._request('POST', path, data=data)

    def _load_image(self, file_name):
        """loads image to upload"""
        fd = io.open(file_name, "rb")
        content = fd.read()
        fd.close()
        return content, file_name

    def _request(self, method, path, params=None, data=None, files=None):
        if data is not None:
            data = xmltodict.unparse({'prestashop': data}).encode('utf-8')
        res = requests.request(method, self._get_url(path),
                               auth=(self._api_token(), ''),
                               params=params,
                               data=data,
                               files=files)
        return self._check_response(res, xmltodict.parse(res.text)['prestashop'] if not files and res.text else None)

    def add_image(self, path, file_name, exists=False):
        content, file_name = self._load_image(file_name)
        files = [('image', file_name, content)]
        headers, data = self._encode_multipart_formdata(files)
        return self._request('POST', 'images/' + path, params={'ps_method': 'PUT'} if exists else None, data=data, headers=headers)

    def get(self, path, params=None):
        return self._request('GET', path, params)

    def edit(self, path, data):
        return self._request('PUT', path, data=data)

    def delete(self, path):
        return self._request('DELETE', path)