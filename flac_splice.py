import struct, logging

logging.basicConfig(level=logging.DEBUG, filename='flac_splice.log', 
                    format='%(asctime)s - %(levelname)s : %(message)s')

flacfile = open('music\\Heroes of Might and Magic II ~ The Price of\
 Loyalty (Rob King, Steve Baca, Paul Romero)\\10 - City of the Wizard.flac', 'rb')

b = flacfile.read()
logging.debug(f'Reading {b[:4].decode()} at {flacfile.name}') 
print(b[:4])
read_pos = 42
block_dict = {}

block_type = b[read_pos]
next_block_size = int.from_bytes(b[read_pos+1:read_pos + 4])
print(next_block_size)

