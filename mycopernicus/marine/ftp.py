import datetime as dt
import os

import ftplib


class CopernicusConnector:
    def __init__(self, hostname, user, pwd, product_id=None, dataset_id=None, timeout=100):
        self.hostname = hostname
        self.user = user
        self.pwd = pwd
        self.product_id = product_id
        self.dataset_id = dataset_id
        self.path = None
        self.timeout = timeout
        self._connect_ftp()
        self._set_path()

    def change_host(self, hostname):
        if hostname == self.hostname:
            raise f"You are in this host: {hostname}"
        else:
            self.hostname = hostname
            self.close()
            self._connect_ftp()

    def _connect_ftp(self):
        self.ftp = ftplib.FTP(self.hostname, self.user, self.pwd, timeout=self.timeout)
        self.ftp.encoding = "utf-8"

    def cd(self, path):
        try:
            self.ftp.cwd(path)
            self.path = self.ftp.pwd()
        except Exception as err:
            print(f"Unexpected {err}, {type(err)}")
            raise
    

    def get_dir(self):
        return self.fpt.pwd()


    def nlist(self):
        return self.ftp.nlst()

    def close(self):
        self.ftp.close()

    def size(self):
        self.ftp.size()

    def _set_path(self):
        if self.product_id and self.dataset_id:
            self.ftp.cwd(f"Core/{self.product_id}/{self.dataset_id}")
        elif self.product_id:
            self.ftp.cwd(f"Core/{self.product_id}")
        else:
            self.ftp.cwd("Core")
        self.path = self.ftp.pwd()

    def get_hostname(self):
        return self.hostname

    def get_list_products(self):
        if self.path == "Core":
            return self.nlist()
        original_path = self.path
        self.ftp.cwd("Core")
        ls = self.nlist()
        self.cwd(original_path)
        return ls

    def set_product(self, pid):
        self.product_id = pid
        self._set_path()

    def set_dataset(self, did):
        if self.product_id:
            self.dataset_id = did
            self._set_path()
        else:
            raise Exception("Define product_id before")

    def download(self, nf, local, info=True):
        if not os.path.exists(local):
            os.makedirs(local)
        if info:
            print(f"Downloading: {nf}")
        file = open(os.path.join(local, nf), "wb")
        self.ftp.retrbinary("RETR " + nf, file.write)
        file.close()

    def download_from_to(self, localpath, _from, _to, info=False, period=1):
        delta = dt.timedelta(days=period)
        for year in range(_from.year, _to.year + 1):
            print(f"Downloading year: {year}")
            self.cd(f"{year}")
            local = os.path.join(localpath, "{}".format(year))
            for fn in self.nlist():
                t = _from
                while t <= _to:
                    if t.strftime("%Y%m%d") in fn:
                        self.download(fn, local, info=info)
                        _from = t
                        t = _to
                    t += delta
            self.cd("..")