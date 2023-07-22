import struct, logging
from tag_musfile import MusFile

logging.basicConfig(level=logging.DEBUG, filename='mp3_splice.log', 
                    format='%(asctime)s - %(levelname)s : %(message)s', force=True)

UBOM = struct.pack('sss', b'\x01', b'\xff', b'\xfe')

def get_id3_sizebytes(size_int):
    '''Get the four unsigned integers that will become the bytes representing size of the ID3
    header.  a used for initial value for sake of convenience
    '''
    size_0b_ints = []
    a = bin(size_int)[2:]

    def chop_a(a):
        if a[-8] == 0:
            size_0b_ints.append('0b' + a[-8:])
            a = a[:-8] + '0'
        else:
            size_0b_ints.append('0b0' + a[-7:])
            a = a[:-7]
        if len(a) >=8 :
            return chop_a(a)
        else:
            return a
    if len(a)>=8:
        a = chop_a(a)
    # less_than_8 = chop_a(a)
    first_8 = '0b' + a.rjust(8, '0')
    size_0b_ints.append(first_8)

    print(size_0b_ints)
    size_ints = [int(bint, 2) for bint in size_0b_ints]
    print(size_ints)

    while len(size_ints)<4:
        size_ints.append(0)
    size_ints.reverse()
    sizebytes = struct.pack('BBBB', *size_ints)
    return sizebytes

def write_tags(musfile:MusFile, formtext):
    '''Take data from form in mp3_gui and write full ID3 header with tags for the mp3
    file associated with them. Combine into new mp3, and return the name of the new file.
    '''

    logging.debug(f'Beginning to write tags for file {musfile.filename}')
    logging.debug(f'Number of tags to write: {len(list(formtext.keys()))}')

    newtags = {}
    tagnumber = 0  # debug variable
    for key, value in formtext.items():
        logging.debug(f"Writing tag {tagnumber}, '{key}' with value '{value}'") 
        key_charlist = []
        for char in key:
            key_charlist.append((ord(char)))
        newkey = struct.pack('BBBB', *key_charlist)
        newvalue = UBOM
        for char in value:
            char = ord(char)
            newvalue += struct.pack('Bs', char, b'\x00')
        sizebytes = struct.pack('>Lss', len(newvalue), b'\x00', b'\x00')
        print(sizebytes)

        newtags[newkey] = sizebytes + newvalue
    # for key, value in newtags:
    print(newtags)

    ID3_h_start = struct.pack('ssssss', b'I', b'D', b'3', b'\x03', b'\x00', b'\x00')
    ID3_size_int = 0
    for key, value in newtags.items():
        ID3_size_int += len(value) + len(key)
    print(ID3_size_int)
    ID3_sizebytes = get_id3_sizebytes(ID3_size_int)
    ID3_header = ID3_h_start + ID3_sizebytes
    ID3_foot_bytes = b'\x00' * 127 + b'\xff'
    ID3_footer = struct.pack('128s', ID3_foot_bytes)
    test_mp3 = open('test.mp3', 'wb')
    mpeg_data = musfile.allbytes[musfile.id3_length:-128]
    test_mp3.write(ID3_header)
    for tagtype, tagdata in newtags.items():
        test_mp3.write(tagtype + tagdata)
    test_mp3.write(mpeg_data)
    test_mp3.write(ID3_footer)
    test_mp3.close()

    
    # ID3_size_bytes =
    # ID3_header = ID3_h_start + 

            
        





    # TIT2 = b'\x54\x49\x54\x32\x00\x00\x00\x0c\x00\x00\x00\x42\x00\x49\x00\x4c\x00\x4c\x00'
    # bob = struct.pack('21c', b'\x54', b'\x49', b'\x54', b'\x32', b'\x00', b'\x00', b'\x00',
    #                 b'\x0b', b'\x00', b'\x00', b'\x01', b'\xff', b'\xfe', b'\x42', b'\x00',
    #                 b'\x49', b'\x00', b'\x4c', b'\x00', b'\x4c', b'\x00')
    # TALB = b'TALB\x00\x00\x00\x0b\x00\x00\x01\xff\xfeD\x00A\x00T\x00A\x00'
    # bill = struct.pack('22s', TIT2)
    # TALB = struct.pack('21s', TALB)
    # print(bob)
    # print(bill)
    # length_tags = len(TIT2)
    # print(length_tags)
    # ID3_h_start = b'ID3\x03\x00\x00'
    # ID3_h_sizebytes = b'\x00' 
    # a = bin(f'bob')
    # print(a)
    # ID3_header = struct.pack('10s', ID3_h_start, ID3_h_sizebytes)


    # test_mp3.write(ID3_header)
    # test_mp3.write(bob)
    # test_mp3.write(TALB)
    # test_mp3.write(mpeg_data)

    # newfile_name = test_mp3.name
    # test_mp3.close()
    # return newfile_name