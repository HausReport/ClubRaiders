#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import base64
import re
import string
import zlib

from dahuffman import HuffmanCodec

bunchOfQueries = ""
data = []
data.append('[')
data.append('{')
data.append('\'')
data.append(':')
data.append(' ')
data.append(',')
data.append('}')
data.append(']')
data.append('f')
codec=None

#for ch in string.printable:
#    data.append(ch)


def gzip_str(string_: str) -> str:
    global bunchOfQueries
    global data
    global codec

    bunchOfQueries += string_

    dat2 = re.split("[{': ,}]",bunchOfQueries)
    data = data + dat2


    codec = HuffmanCodec.from_data(data)
    codec.print_code_table()
    short = codec.encode(dat2)

    bar = short
    # print( "huffman: " + str(short))
    # bar = base64.urlsafe_b64encode(short)
    # print("base64d: " + str(bar))
    return bar.decode('utf-16')

def gunzip_str(string_:bytes) -> str:
    global codec
    bar = string_.encode('utf-16') #base64.urlsafe_b64decode(string_)
    short = codec.decode(bar)
    print( "decoded: " + str(short))
    return str(short)


if __name__ == '__main__':
    string_ = 'hello there!'
    gzipped_string = gzip_str(string_)#.encode('utf-8'))
    print(gzipped_string)
    original_string = gunzip_str(gzipped_string)
    assert string_ == original_string
