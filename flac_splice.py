import struct, logging
from tag_flacfile import FlacFile

logging.basicConfig(level=logging.DEBUG, filename='mp3_splice.log', 
                    format='%(asctime)s - %(levelname)s : %(message)s', force=True)


def write_tags(flacfile: FlacFile, formtext):
    '''Given input from flac_gui form, create proper binary-format comments
        and combine it with other comments to make a comment block, then stitch
        it back together with the other data from the flac file.
    '''
    tagdict = {}
    cblock_newsize = 0
    for tag in formtext:
        logging.debug(f'Processing tag {tag} length {len(tag)}')
        tag_length = struct.pack('<I', len(tag))
        btag = b''
        for char in tag:
            char = ord(char)
            btag += struct.pack('B', char)
        tagdict[btag] = tag_length
        cblock_newsize += len(btag) + len(tag_length)
    cblock_newsize += len(flacfile.venstring) + 8   # venstring, its size, and # of comments

    test_flac = open('test.flac', 'wb')
    test_flac.write(flacfile.allbytes[:26])
    blank_md5 = b'\x00' * 16
    test_flac.write(blank_md5)
    # test_flac.write(flacfile.allbytes[:42])

    for type, blocktup in flacfile.block_dict.items():
        test_flac.write(struct.pack('B', type))
 

        if type != 4:
            full_intbytes = struct.pack('>I', blocktup[1])
            if full_intbytes[0] != 0:
                raise OverflowError('Block size too large')
            block_sizebytes = full_intbytes[1:]
            test_flac.write(block_sizebytes)
            test_flac.write(blocktup[0])
        else: 
            full_intbytes = struct.pack('>I', cblock_newsize)
            if full_intbytes[0] != 0:
                raise OverflowError('Block size too large')
            block_sizebytes = full_intbytes[1:]
            test_flac.write(block_sizebytes)
            logging.debug('Writing vorbis comments...')
            test_flac.write(struct.pack('<I', len(flacfile.venstring)))
            test_flac.write(flacfile.venstring)
            test_flac.write(struct.pack('<I', len(list(tagdict.keys()))))
            for tag, length in tagdict.items():
                logging.debug(f'Writing {tag}')
                test_flac.write(length + tag)
    
    logging.debug('Finished writing blocks. Writing audio data...')
    test_flac.write(flacfile.allbytes[flacfile.read_pos:])
    logging.debug('Audio data written. Closing file...')
    test_flac.close()
