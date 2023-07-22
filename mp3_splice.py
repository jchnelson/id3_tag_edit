import struct
from tag_musfile import MusFile

def write_tags(basemp3:MusFile) -> str:

    mpeg_data = basemp3.allbytes[basemp3.id3_length:]

    test_mp3 = open('test_.mp3', 'wb')

    TIT2 = b'\x54\x49\x54\x32\x00\x00\x00\x0c\x00\x00\x00\x42\x00\x49\x00\x4c\x00\x4c\x00'
    bob = struct.pack('21c', b'\x54', b'\x49', b'\x54', b'\x32', b'\x00', b'\x00', b'\x00',
                    b'\x0b', b'\x00', b'\x00', b'\x01', b'\xff', b'\xfe', b'\x42', b'\x00',
                    b'\x49', b'\x00', b'\x4c', b'\x00', b'\x4c', b'\x00')
    TALB = b'TALB\x00\x00\x00\x0b\x00\x00\x01\xff\xfeD\x00A\x00T\x00A\x00'
    bill = struct.pack('22s', TIT2)
    TALB = struct.pack('21s', TALB)
    print(bob)
    print(bill)
    length_tags = len(TIT2)
    print(length_tags)
    ID3_h_start = b'ID3\x03\x00\x00'
    ID3_h_sizebytes = b'\x00' 
    a = bin(f'bob')
    print(a)
    ID3_header = struct.pack('10s', ID3_h_start, ID3_h_sizebytes)


    test_mp3.write(ID3_header)
    test_mp3.write(bob)
    test_mp3.write(TALB)
    test_mp3.write(mpeg_data)

    newfile_name = test_mp3.name
    test_mp3.close()
    return newfile_name