# -*- coding: utf-8 -*-
"""

    Copyright (C) 2018-2018 plugin.video.youtube

    SPDX-License-Identifier: GPL-2.0-only
    See LICENSES/GPL-2.0-only for more information.
"""

from . import JSONStore
import base64

key = base64.b64decode('QUl6YVN5RExCM0NtV0dOOEpqV0k0U0xMdEdMZVhGaWl1cldJWHRz')
cid = base64.b64decode('ODc0NzQ5OTE4OC03NTFyZmw4ZXA3b2VtOWZxaTgyaTUycG82dTlwNzdmYg==')
csc = base64.b64decode('X1RoNjdpRXdKQnNGN0Q0Q1F2SWlBSmEt')

class APIKeyStore(JSONStore):
    def __init__(self):
        JSONStore.__init__(self, 'api_keys.json')

    def set_defaults(self):
        data = self.get_data()
        if 'keys' not in data:
            #data = {'keys': {'personal': {'api_key': '', 'client_id': '', 'client_secret': ''}, 'developer': {}}}
            data = {'keys': {'personal': {'api_key': key, 'client_id': cid, 'client_secret': csc}, 'developer': {}}}
        if 'keys' in data:
            data = {'keys': {'personal': {'api_key': key, 'client_id': cid, 'client_secret': csc}, 'developer': {}}}
        if 'personal' not in data['keys']:
            data['keys']['personal'] = {'api_key': '', 'client_id': '', 'client_secret': ''}
        if 'developer' not in data['keys']:
            data['keys']['developer'] = {}
        self.save(data)
