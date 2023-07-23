import struct, logging

logging.basicConfig(level=logging.DEBUG, filename='flac_splice.log', 
                    format='%(asctime)s - %(levelname)s : %(message)s')


class FlacFile():
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'rb')
        self.allbytes = self.file.read()
        logging.debug(f'Reading {self.allbytes[:4].decode()} at {self.file.name}') 
        print(self.allbytes[:4])
        self.read_pos = 42
        self.block_dict = self.get_metadata_blocks()
        self.vcomment_block = self.block_dict[4]
        self.vcomments, self.venstring = self.get_vorbis_comments()
        print(self.vcomment_block)

    def get_metadata_blocks(self):
        block_dict = {}
        while self.allbytes[self.read_pos] != 129:  # hex 81, identifier for padding block
            block_type = self.allbytes[self.read_pos]
            next_block_size = int.from_bytes(self.allbytes[self.read_pos+1:self.read_pos + 4])
            logging.debug(f'Getting next block (type {self.allbytes[self.read_pos]}), \
size {next_block_size}')
            self.read_pos += 4
            block_dict[block_type] = self.allbytes[self.read_pos:self.read_pos+next_block_size]
            self.read_pos += next_block_size
        return block_dict

    def get_vorbis_comments(self):
        vread_pos = 0
        bk = self.vcomment_block
        logging.debug(f'Processing Comments from bk {bk}')
        ven_str_length = int.from_bytes(bk[vread_pos:vread_pos+4], 'little')
        vread_pos += 4
        ven_string = bk[vread_pos:vread_pos+ven_str_length]
        vread_pos += ven_str_length
        num_comments = int.from_bytes(bk[vread_pos:vread_pos+4], 'little')
        vread_pos += 4
        vcomments = []
        logging.debug(f'Vendor String {ven_string} parsed, getting {num_comments} comments')
        while vread_pos < len(bk)-1:
            comm_length = int.from_bytes(bk[vread_pos:vread_pos+4], 'little')
            vread_pos += 4
            comment = bk[vread_pos:vread_pos+comm_length]
            logging.debug(f'Getting comment, length {comm_length}, {comment}')
            vread_pos += comm_length
            vcomments.append(comment)
        return vcomments, ven_string

flacfile = FlacFile('music\\Heroes of Might and Magic II ~ The Price of\
 Loyalty (Rob King, Steve Baca, Paul Romero)\\10 - City of the Wizard.flac')
print(flacfile.vcomments)

            

