import logging, re, sys
from id3_standard_tags import tagdict, tagdict_v22


logging.basicConfig(level=logging.DEBUG, filename='tag_musfile.log', 
                    format = '%(asctime)s - %(levelname)s: %(message)s')


class MusFile():
    '''Base object for creating and holding tag information'''
    def __init__(self, filename):
        self.read_pos = 10
        self.filename = filename
        self.file = open(filename, 'rb')
        self.allbytes = self.file.read()
        self.id3_version = self.allbytes[3]
        if self.id3_version == 3:
            self.bindex = 10
            self.step = 4
            self.tagdict = tagdict
        elif self.id3_version == 2:
            self.bindex = 6
            self.step = 3
            self.tagdict = tagdict_v22
        # Size bytes identical between versions, formula from ID3 specs
        self.id3_length = self.allbytes[6] * (2 ** 21) + self.allbytes[7] * (2**14) + \
        self.allbytes[8] * (2**7) +  self.allbytes[9] * (1) 
        self.taglist = self.make_taglist()
        self.active_tags = self.make_readable_tags()

    def get_tag(self, initial_pos):
        '''Retrieve tag information from a group of binary bytes (b) from an initial read
        position. Gets one ID3 tag'''
        tag_type = self.allbytes[initial_pos:initial_pos+self.step]
        tag_size = int.from_bytes(self.allbytes[initial_pos+self.step:initial_pos+(self.step * 2)])
        self.read_pos += self.bindex + tag_size
        if all(byte == 0 for byte in self.allbytes[initial_pos:self.read_pos]):
            return False

        logging.debug(f'Tag type is {tag_type.decode()}, tag length {tag_size}, read pos {self.read_pos}')
        return self.allbytes[initial_pos:self.read_pos]
    
    def make_taglist(self):
        '''Initialize list of full, binary ID3 tag sections'''
        taglist = []
        while self.read_pos < self.id3_length:
            tag = self.get_tag(self.read_pos)
            if tag and len(tag) < 200:
                taglist.append(tag)
        return taglist

    def make_readable_tags(self):
        active_tags = {}
        for tag in self.taglist:
            bom = re.match(b'\xff\xfe', tag[self.bindex + 1:])
            if bom:
                active_tags[tag[:self.step].decode()] = tag[self.bindex + 3:]
            else:
                active_tags[tag[:self.step].decode()] = tag[self.bindex + 1:]

        for tagtype, tag in active_tags.items():
            logging.debug(f'Processing {tagtype}, {tag}')
            for i in range(len(tag)-2, -1, -1):
                if tag[i] == 0:
                    # logging.debug(f'Removing {tag[i]}')
                    tag = tag[:i] + tag[i+1:]
                    # logging.debug(f"Result {tag.decode(errors='replace')}")

            if tag[-1] == 0:
                tag = tag[:-1]
            tag = re.sub(b'\xff\xfe', b' ', tag)
            active_tags[tagtype] = tag.decode(errors='replace')

        return active_tags


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Please include a full or relative filepath in your command')
        sys.exit()
    musfile = MusFile(sys.argv[1])

#implement conversion from genre list for content type tags
    print('\n')
    for tag, value in musfile.active_tags.items():
        if tag not in musfile.tagdict:
            jtag_type = f'Noncompliant "{tag}"'.ljust(60, '-')
        else:
            jtag_type = musfile.tagdict[tag].ljust(60, '-')
        jtag_value = value.rjust(70, '-')
        print(f' {jtag_type} {jtag_value}')
    print('\n')
