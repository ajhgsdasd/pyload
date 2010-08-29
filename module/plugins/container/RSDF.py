#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import binascii

from module.plugins.Container import Container

class RSDF(Container):
    __name__ = "RSDF"
    __version__ = "0.2"
    __pattern__ = r"(?!http://).*\.rsdf"
    __description__ = """RSDF Container Decode Plugin"""
    __author_name__ = ("RaNaN", "spoob")
    __author_mail__ = ("RaNaN@pyload.org", "spoob@pyload.org")

    
    def decrypt(self, pyfile):
    
        from Crypto.Cipher import AES

        infile = pyfile.url.replace("\n", "")
        Key = binascii.unhexlify('8C35192D964DC3182C6F84F3252239EB4A320D2500000000')

        IV = binascii.unhexlify('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
        IV_Cipher = AES.new(Key, AES.MODE_ECB)
        IV = IV_Cipher.encrypt(IV)

        obj = AES.new(Key, AES.MODE_CFB, IV)

        rsdf = open(infile, 'r')

        data = rsdf.read()
        data = binascii.unhexlify(''.join(data.split()))
        data = data.splitlines()

        links = []
        for link in data:
            link = base64.b64decode(link)
            link = obj.decrypt(link)
            decryptedUrl = link.replace('CCF: ', '')
            links.append(decryptedUrl)

        rsdf.close()
        
        self.packages.append((pyfile.name, links, pyfile.name))