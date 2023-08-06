#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    0. Base on update.cz88.net
    1. Download innoextract and put it in the /usr/local/bin/ directory
    2. Download the offline version (EXE file) of the community version of the Pure IP Library
    3. Extract the EXE file
    4. Use innoextract to extract the EXE file
    5. Copy qqwry.dat to the specified directory
"""

import re
import os
import zipfile
import shutil
import requests
from subprocess import Popen, PIPE
from html.parser import HTMLParser

__all__ = ('UpdateQQwry',)


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.download_link = None
        self.article_url = None
        self.date = None

    def handle_starttag(self, tag, attrs):
        # If the tag is li and the class attribute value is album__list-item js_album_item js_wx_tap_highlight wx_tap_cell
        if tag == "li" and ("class", "album__list-item js_album_item js_wx_tap_highlight wx_tap_cell") in attrs:
            # Traverse all attributes, find the data-link attribute, and save its value
            for attr, value in attrs:
                # If the data-link attribute is found and the download_link has not been found yet
                if attr == "data-link" and not self.download_link:
                    self.download_link = value
                    break

    def handle_data(self, data):
        # If the download_link has been found and the date has not been found yet
        if self.download_link and not self.date:
            # Use regular expressions to match the date format and save the first matching result
            match = re.search(r"\d{4}-\d{2}-\d{2}", data)
            if match:
                self.date = match.group()


class UpdateQQwry:
    def __init__(self, destination_file):
        self.destination_file = destination_file
        if os.getlogin() == 'root':
            self.innoextract_path = '/usr/local/bin/innoextract'
        else:
            bin_path = os.path.join(os.path.expanduser("~"), 'bin')
            if not os.path.exists(bin_path):
                os.makedirs(bin_path)
            self.innoextract_path = os.path.join(bin_path, 'innoextract')

    def run_cmd(self, cmd):
        """
        Execute cmd command
        @param cmd str:cmd command  e.g. ls -lh
        @return tuple: returncode, stdout, stderr
        """
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = proc.communicate()
        return proc.returncode, out.decode(), err.decode()

    def download_innoextract(self):
        """
        Download innoextract from https://github.com/out0fmemory/qqwry.dat/ and put it in /usr/local/bin/
        """
        url = 'https://github.com/out0fmemory/qqwry.dat/raw/master/exe_tool/innoextract'
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print("Download {} failed".format(url))
            return False
        if not os.path.exists(self.innoextract_path):
            with open(self.innoextract_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            print("Download {} to {} completed".format(url, self.innoextract_path))
        os.chmod(self.innoextract_path, 0o755)
        return self.check_innoextract()

    def download_latest_exe(self):
        """
        Download the offline version (EXE file) of the community version of the Pure IP Library
        """
        url = 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Mzc0NTA3NA==&action=getalbum&album_id=2329805780276838401'
        response = requests.get(url)
        parser = MyHTMLParser()
        # Use the re module to replace the a tag in response.text with album__list-item-cover js_album_item_cover wx_tap_cell
        new_text = re.sub(r"<a.*?>(.*?)</a>",
                          r"<a class='album__list-item-cover js_album_item_cover wx_tap_cell'>\1</a>", response.text)
        # Use the HTML parser object to parse the new text
        # Get the latest article address and date
        parser.feed(new_text)
        # Get the article content
        response = requests.get(parser.download_link)
        # Regularly match the download link
        zip_list = re.findall(r'https://www.cz88.net/soft/.*.zip', response.text)
        if len(zip_list) > 0:
            save_path = "/tmp/{}.zip".format(parser.date)
            if not os.path.exists(save_path):
                zip_url = zip_list[0]
                print("{} Downloading...".format(zip_url))
                response = requests.get(zip_url, stream=True)
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                print("{} Download completed".format(zip_url))
            # unzip file
            extract_dir = "/tmp/"
            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                # Extract all files to the specified directory
                zip_ref.extractall(extract_dir)
            exe_path = os.path.join(extract_dir, "setup.exe")
            if not os.path.exists(exe_path):
                return False, "The offline version (EXE file) of the community version of the Pure IP Library was not found"
            # Delete zip file
            os.remove(save_path)
            return True, exe_path
        else:
            return False, "No download link matched"

    def check_innoextract(self):
        """
        Check if innoextract is valid
        """
        command = "{} -v".format(self.innoextract_path)
        ret_code, _, _ = self.run_cmd(command)
        if ret_code != 0:
            return False
        return True

    def update(self):
        # Check if innoextract is valid
        if not self.check_innoextract():
            if not self.download_innoextract():
                print("{} is invalid".format(self.innoextract_path))
                return False
            else:
                print("{} is valid".format(self.innoextract_path))
        else:
            print("{} is valid".format(self.innoextract_path))

        download_status, exe_path = self.download_latest_exe()
        if not download_status:
            print(exe_path)
            return False
        command = "cd /tmp/ && {} -I app/qqwry.dat {}".format(self.innoextract_path, exe_path)
        ret_code, stdout, stderr = self.run_cmd(command)
        source_file = '/tmp/app/qqwry.dat'
        if ret_code == 0 and 'app/qqwry.dat' in stdout and os.path.exists(source_file):
            shutil.copy(source_file, self.destination_file)
            print("copy {} to {} completed".format(source_file, self.destination_file))
            # Delete temporary files
            shutil.rmtree('/tmp/app')
            return True
        else:
            print("Execution of {} failed, msg:{}".format(command, stderr))
            return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Please provide at least 1 parameter: <the specified directory>")
        exit(1)
    elif os.name != 'posix':
        print("The current system is not Linux, exiting")
        exit(1)
    else:
        # Get command line parameters
        destination_file = sys.argv[1]
        qq = UpdateQQwry(destination_file)
        qq.update()
