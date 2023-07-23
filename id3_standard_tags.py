tagdict = {
'AENC': 'Audio encryption',
'APIC': 'Attached picture',
'ASPI': 'Audio seek point index',
'COMM': 'Comments',
'COMR': 'Commercial frame',
'ENCR': 'Encryption method registration',
'EQU2': 'Equalisation (2)',
'ETCO': 'Event timing codes',
'GEOB': 'General encapsulated object',
'GRID': 'Group identification registration',
'LINK': 'Linked information',
'MCDI': 'Music CD identifier',
'MLLT': 'MPEG location lookup table',
'OWNE': 'Ownership frame',
'PCNT': 'Play counter',
'POPM': 'Popularimeter',
'POSS': 'Position synchronisation frame',
'PRIV': 'Private frame',
'RBUF': 'Recommended buffer size',
'RVA2': 'Relative volume adjustment (2)',
'RVRB': 'Reverb',
'SEEK': 'Seek frame',
'SIGN': 'Signature frame',
'SYLT': 'Synchronised lyric/text',
'SYTC': 'Synchronised tempo codes',
'TALB': 'Album/Movie/Show title',
'TBPM': 'BPM (beats per minute)',
'TYER': 'Year of Release',
'TCOM': 'Composer',
'TCON': 'Content type',
'TCOP': 'Copyright message',
'TDEN': 'Encoding time',
'TDLY': 'Playlist delay',
'TDOR': 'Original release time',
'TDRC': 'Recording time',
'TDRL': 'Release time',
'TDTG': 'Tagging time',
'TENC': 'Encoded by',
'TEXT': 'Lyricist/Text writer',
'TFLT': 'File type',
'TIPL': 'Involved people list',
'TIT1': 'Content group description',
'TIT2': 'Title/songname/content description',
'TIT3': 'Subtitle/Description refinement',
'TKEY': 'Initial key',
'TLAN': 'Language(s)',
'TLEN': 'Length',
'TMCL': 'Musician credits list',
'TMED': 'Media type',
'TMOO': 'Mood',
'TOAL': 'Original album/movie/show title',
'TOFN': 'Original filename',
'TOLY': 'Original lyricist(s)/text writer(s)',
'TOPE': 'Original artist(s)/performer(s)',
'TOWN': 'File owner/licensee',
'TPE1': 'Lead performer(s)/Soloist(s)',
'TPE2': 'Band/orchestra/accompaniment',
'TPE3': 'Conductor/performer refinement',
'TPE4': 'Interpreted, remixed, or otherwise modified by',
'TPOS': 'Part of a set',
'TPRO': 'Produced notice',
'TPUB': 'Publisher',
'TRCK': 'Track number/Position in set',
'TRSN': 'Internet radio station name',
'TRSO': 'Internet radio station owner',
'TSOA': 'Album sort order',
'TSOP': 'Performer sort order',
'TSOT': 'Title sort order',
'TSRC': 'ISRC (international standard recording code)',
'TSSE': 'Software/Hardware and settings used for encoding',
'TSST': 'Set subtitle',
'TXXX': 'User defined text information frame',
'UFID': 'Unique file identifier',
'USER': 'Terms of use',
'USLT': 'Unsynchronised lyric/text transcription',
'WCOM': 'Commercial information',
'WCOP': 'Copyright/Legal information',
'WOAF': 'Official audio file webpage',
'WOAR': 'Official artist/performer webpage',
'WOAS': 'Official audio source webpage',
'WORS': 'Official Internet radio station homepage',
'WPAY': 'Payment',
'WPUB': 'Publishers official webpage',
'WXXX': 'User defined URL link frame'
 }

music_tags = {
'TPE1':('Artist', 'Artist/Group Name'),
'TIT2':('Title', 'Title of Song/Work'),
'TALB':('Album', 'Album Name'),
'TCON':('Genre', 'Genre'),

}

tagdict_v22 = {'BUF': 'Recommended buffer size',
 'CNT': 'Play counter',
 'COM': 'Comments',
 'CRA': 'Audio encryption',
 'CRM': 'Encrypted meta frame',
 'EQU': 'Equalization',
 'ETC': 'Event timing codes',
 'GEO': 'General encapsulated object',
 'IPL': 'Involved people list',
 'LNK': 'Linked information',
 'MCI': 'Music CD Identifier',
 'MLL': 'MPEG location lookup table',
 'PIC': 'Attached picture',
 'POP': 'Popularimeter',
 'REV': 'Reverb',
 'RVA': 'Relative volume adjustment',
 'SLT': 'Synchronized lyric/text',
 'STC': 'Synced tempo codes',
 'TAL': 'Album/Movie/Show title',
 'TBP': 'BPM (Beats Per Minute)',
 'TCM': 'Composer',
 'TCO': 'Content type',
 'TCR': 'Copyright message',
 'TDA': 'Date',
 'TDY': 'Playlist delay',
 'TEN': 'Encoded by',
 'TFT': 'File type',
 'TIM': 'Time',
 'TKE': 'Initial key',
 'TLA': 'Language(s)',
 'TLE': 'Length',
 'TMT': 'Media type',
 'TOA': 'Original artist(s)/performer(s)',
 'TOF': 'Original filename',
 'TOL': 'Original Lyricist(s)/text writer(s)',
 'TOR': 'Original release year',
 'TOT': 'Original album/Movie/Show title',
 'TP1': 'Lead artist(s)/Lead performer(s)/Soloist(s)/Performing group',
 'TP2': 'Band/Orchestra/Accompaniment',
 'TP3': 'Conductor/Performer refinement',
 'TP4': 'Interpreted, remixed, or otherwise modified by',
 'TPA': 'Part of a set',
 'TPB': 'Publisher',
 'TRC': 'ISRC (International Standard Recording Code)',
 'TRD': 'Recording dates',
 'TRK': 'Track number/Position in set',
 'TSI': 'Size',
 'TSS': 'Software/hardware and settings used for encoding',
 'TT1': 'Content group description',
 'TT2': 'Title/Songname/Content description',
 'TT3': 'Subtitle/Description refinement',
 'TXT': 'Lyricist/text writer',
 'TXX': 'User defined text information frame',
 'TYE': 'Year',
 'UFI': 'Unique file identifier',
 'ULT': 'Unsychronized lyric/text transcription',
 'WAF': 'Official audio file webpage',
 'WAR': 'Official artist/performer webpage',
 'WAS': 'Official audio source webpage',
 'WCM': 'Commercial information',
 'WCP': 'Copyright/Legal information',
 'WPB': 'Publishers official webpage',
 'WXX': 'URL link frame'}

genre_list = {'0': 'Blues',
 '1': 'Classic Rock',
 '10': 'New Age',
 '100': 'Humour',
 '101': 'Speech',
 '102': 'Chanson',
 '103': 'Opera',
 '104': 'Chamber Music',
 '105': 'Sonata',
 '106': 'Symphony',
 '107': 'Booty Bass',
 '108': 'Primus',
 '109': 'Porn Groove',
 '11': 'Oldies',
 '110': 'Satire',
 '111': 'Slow Jam',
 '112': 'Club',
 '113': 'Tango',
 '114': 'Samba',
 '115': 'Folklore',
 '116': 'Ballad',
 '117': 'Power Ballad',
 '118': 'Rhythmic Soul',
 '119': 'Freestyle',
 '12': 'Other',
 '120': 'Duet',
 '121': 'Punk Rock',
 '122': 'Drum Solo',
 '123': 'A capella',
 '124': 'Euro-House',
 '125': 'Dance Hall',
 '13': 'Pop',
 '14': 'R&B',
 '15': 'Rap',
 '16': 'Reggae',
 '17': 'Rock',
 '18': 'Techno',
 '19': 'Industrial',
 '2': 'Country',
 '20': 'Alternative',
 '21': 'Ska',
 '22': 'Death Metal',
 '23': 'Pranks',
 '24': 'Soundtrack',
 '25': 'Euro-Techno',
 '26': 'Ambient',
 '27': 'Trip-Hop',
 '28': 'Vocal',
 '29': 'Jazz+Funk',
 '3': 'Dance',
 '30': 'Fusion',
 '31': 'Trance',
 '32': 'Classical',
 '33': 'Instrumental',
 '34': 'Acid',
 '35': 'House',
 '36': 'Game',
 '37': 'Sound Clip',
 '38': 'Gospel',
 '39': 'Noise',
 '4': 'Disco',
 '40': 'AlternRock',
 '41': 'Bass',
 '42': 'Soul',
 '43': 'Punk',
 '44': 'Space',
 '45': 'Meditative',
 '46': 'Instrumental Pop',
 '47': 'Instrumental Rock',
 '48': 'Ethnic',
 '49': 'Gothic',
 '5': 'Funk',
 '50': 'Darkwave',
 '51': 'Techno-Industrial',
 '52': 'Electronic',
 '53': 'Pop-Folk',
 '54': 'Eurodance',
 '55': 'Dream',
 '56': 'Southern Rock',
 '57': 'Comedy',
 '58': 'Cult',
 '59': 'Gangsta',
 '6': 'Grunge',
 '60': 'Top 40',
 '61': 'Christian Rap',
 '62': 'Pop/Funk',
 '63': 'Jungle',
 '64': 'Native American',
 '65': 'Cabaret',
 '66': 'New Wave',
 '67': 'Psychadelic',
 '68': 'Rave',
 '69': 'Showtunes',
 '7': 'Hip-Hop',
 '70': 'Trailer',
 '71': 'Lo-Fi',
 '72': 'Tribal',
 '73': 'Acid Punk',
 '74': 'Acid Jazz',
 '75': 'Polka',
 '76': 'Retro',
 '77': 'Musical',
 '78': 'Rock & Roll',
 '79': 'Hard Rock',
 '8': 'Jazz',
 '80': 'Folk',
 '81': 'Folk-Rock',
 '82': 'National Folk',
 '83': 'Swing',
 '84': 'Fast Fusion',
 '85': 'Bebob',
 '86': 'Latin',
 '87': 'Revival',
 '88': 'Celtic',
 '89': 'Bluegrass',
 '9': 'Metal',
 '90': 'Avantgarde',
 '91': 'Gothic Rock',
 '92': 'Progressive Rock',
 '93': 'Psychedelic Rock',
 '94': 'Symphonic Rock',
 '95': 'Slow Rock',
 '96': 'Big Band',
 '97': 'Chorus',
 '98': 'Easy Listening',
 '99': 'Acoustic'}

vorbis_dict = {'TITLE': 'Track/Work name',
'VERSION' : 'Version of track title (e.g. remix info)',
'ALBUM' : 'Name of album',
'TRACKNUMBER': "Track number",
'ARTIST': 'Artist/Group name',
'PERFORMER': 'The artist(s) who performed the work',
'COPYRIGHT': 'Copyright attribution',
'LICENSE': 'License information',
'ORGANIZATION': 'Record label',
'DESCRIPTION': 'A short description',
'GENRE': 'Genre',
'DATE': 'Date recorded',
'LOCATION': 'Location recorded',
'CONTACT': 'Contact information',
'ISRC': 'ISRC number',
'COMPOSER': 'Composer name',
'ALBUM ARTIST' : 'Artist name',
'ALBUMARTIST' : 'Artist name',
'DISCNUMBER' : 'Disc Number',
'TOTALDISCS' : 'Total number of discs',
'TOTALTRACKS' : 'Total number of tracks',
'COMMENT' : 'A short comment',




}
