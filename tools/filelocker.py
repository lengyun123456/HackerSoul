#!/usr/bin/env python
# coding=utf-8
# windows2000@ff0000team

import os
import time
import struct
import getpass
import optparse
import platform

try:
    from Crypto.Cipher import DES
except Exception:
    print 'The module PyCrypto is needed.'
    print 'You may install it by running "pip install pycrypto',
    print 'or "easy_install pycrypto" under command line.'
    exit(1)


class FileLocker(object):
    block_size = 8

    def __init__(self):
        self._init_cmd_paser()
        self._input_password()
        self.cipher = DES.new(self.password, DES.MODE_ECB)

    def _init_cmd_paser(self):
        usage = "python filelocker.py -e/-d INPUT_FILE OUTPUT_FILE\n\n"\
                "e.g. : python filelocker.py -e c:\\1.txt d:\\2.txt\n"\
                "       python filelocker.py -d /tmp/1.xxx /home/2.yyy"
        parser = optparse.OptionParser(usage=usage)
        parser.add_option('-e', '--encrypt',
                          action='store_true', dest='is_encrypt',
                          help='to do encryption.')
        parser.add_option('-d', '--decrypt',
                          action='store_false', dest='is_encrypt',
                          help='to do decryption.')
        parser.add_option('-c', '--clean_original',
                          action='store_true', dest='clean_original', default=False,
                          help='clean the original input file after encryption.')
        (self.options, self.args) = parser.parse_args()
        try:
            self.in_file_path = self.args[0]
            self.out_file_path = self.args[1] if len(self.args) > 1 else u''
        except Exception, err:
            parser.print_help()
            exit(1)

        if not os.path.exists(self.in_file_path):
            print 'Error: input file not exists!'
            exit(1)
        self.__paths_to_unicode()

    def __paths_to_unicode(self):
        system = platform.system().lower()
        encoding = 'gbk' if system == 'windows' else 'utf8'
        if self.in_file_path:
            self.in_file_path = self.in_file_path.decode(encoding, 'ignore')
        if self.out_file_path:
            self.out_file_path = self.out_file_path.decode(encoding, 'ignore')

    def _input_password(self):
        if self.options.is_encrypt:
            self.password = getpass.getpass('Please input you password for Encryption: ')
            password_again = getpass.getpass('Please confirm you password: ')
            if self.password != password_again:
                print 'Error: the two passwords input are not the same!'
                exit(1)
            if len(self.password) < self.block_size:
                print 'Error: password too short!'
                exit(1)
        else:
            self.password = getpass.getpass('Please input you password for Decryption: ')
            if len(self.password) < self.block_size:
                print 'Error: password incorrect!'
                exit(1)

        self.password = self.password[:self.block_size]

    def encrypt_file(self):
        fi = open(self.in_file_path, mode='rb')
        fo = open(self.out_file_path, mode='wb')
        fsize = os.path.getsize(self.in_file_path)
        fo.write(self.cipher.encrypt(struct.pack('Q', fsize)))
        extra_size = fsize % self.block_size
        fo.write(self.cipher.encrypt(fi.read(fsize - extra_size)))
        if extra_size:
            last_block = fi.read(self.block_size) + ' ' * (self.block_size - extra_size)
            fo.write(self.cipher.encrypt(last_block))
        fi.close()
        fo.close()
        if self.options.clean_original:
            os.remove(self.in_file_path)

    def decrypt_file(self):
        fi = open(self.in_file_path, mode='rb')
        fo = open(self.out_file_path, mode='wb')
        origin_fsize = struct.unpack('Q', self.cipher.decrypt(
            fi.read(struct.calcsize('Q'))))[0]
        cur_fsize = os.path.getsize(self.in_file_path) - struct.calcsize('Q')
        last_block_size = self.block_size - (cur_fsize - origin_fsize)
        fo.write(self.cipher.decrypt(fi.read(cur_fsize - self.block_size)))
        fo.write(self.cipher.decrypt(fi.read(self.block_size))[:last_block_size])
        fi.close()
        fo.close()

    def run(self):
        start_time = time.time()
        if self.options.is_encrypt:
            print 'encrypting...'
            self.encrypt_file()
            print 'encrypted file has generated at %s,'\
                  % os.path.abspath(self.out_file_path),
        else:
            print 'decrypting...'
            self.decrypt_file()
            print 'decrypted file has generated at %s,'\
                  % os.path.abspath(self.out_file_path),
        print '%fs costed.' % (time.time() - start_time)


if __name__ == '__main__':
    fl = FileLocker()
    fl.run()
