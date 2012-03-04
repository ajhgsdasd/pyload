# -*- coding: utf-8 -*-

"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.
    
    @author: mkaay
"""

from module.plugins.Account import Account
from time import strptime, mktime
import re

class ShareonlineBiz(Account):
    __name__ = "ShareonlineBiz"
    __version__ = "0.22"
    __type__ = "account"
    __description__ = """share-online.biz account plugin"""
    __author_name__ = ("mkaay", "zoidberg")
    __author_mail__ = ("mkaay@mkaay.de", "zoidberg@mujmail.cz")
    
    info_threshold = 60
    
    def loadAccountInfo(self, user, req):
        src = req.load("http://api.share-online.biz/account.php?username=%s&password=%s&act=userDetails" % (user, self.accounts[user]["password"]))
        
        info = {}
        for line in src.splitlines():
            if "=" in line:
                key, value = line.split("=")
                info[key] = value
                
        if "dl" in info and info["dl"].lower() != "not_available":
            req.cj.setCookie("share-online.biz", "dl", info["dl"])
        if "a" in info and info["a"].lower() != "not_available":
            req.cj.setCookie("share-online.biz", "a", info["a"])
            
        return {"validuntil": int(info["expire_date"]) if "expire_date" in info else -1, 
                "trafficleft": -1, 
                "premium": True if ("dl" in info or "a" in info) and (info["group"] == "Premium") else False}
        
    def login(self, user, data, req):
        req.lastURL = "http://www.share-online.biz/"
        req.load("https://www.share-online.biz/user/login", cookies=True, post={
                    "user": user,
                    "pass": data["password"]})
