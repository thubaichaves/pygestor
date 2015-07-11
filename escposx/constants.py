""" ESC/POS Commands (Constants) """

# Feed control sequences
CTL_LF = '\x0a'  # Print and line feed
CTL_FF = '\x0c'  # Form feed
CTL_CR = '\x0d'  # Carriage return
CTL_HT = '\x09'  # Horizontal tab
CTL_VT = '\x0b'  # Vertical tab
# Printer hardware
HW_INIT = '\x1b\x40'  # Clear data in buffer and reset modes
HW_SELECT = '\x1b\x3d\x01'  # Printer select
HW_RESET = '\x1b\x3f\x0a\x00'  # Reset printer hardware
# Cash Drawer
CD_KICK_2 = '\x1b\x70\x00'  # Sends a pulse to pin 2 []
CD_KICK_5 = '\x1b\x70\x01'  # Sends a pulse to pin 5 []
# Paper
PAPER_FULL_CUT = '\x1d\x56\x00'  # Full cut paper
PAPER_PART_CUT = '\x1d\x56\x01'  # Partial cut paper
# Text format

BARCODE_TXT_OFF = '\x1d\x48\x00'  # HRI barcode chars OFF
BARCODE_TXT_ABV = '\x1d\x48\x01'  # HRI barcode chars above
BARCODE_TXT_BLW = '\x1d\x48\x02'  # HRI barcode chars below
BARCODE_TXT_BTH = '\x1d\x48\x03'  # HRI barcode chars both above and below
BARCODE_FONT_A = '\x1d\x66\x00'  # Font type A for HRI barcode chars
BARCODE_FONT_B = '\x1d\x66\x01'  # Font type B for HRI barcode chars
BARCODE_HEIGHT = '\x1d\x68\x64'  # Barcode Height [1-255]
BARCODE_WIDTH = '\x1d\x77\x03'  # Barcode Width  [2-6]
BARCODE_UPC_A = '\x1d\x6b\x00'  # Barcode type UPC-A
BARCODE_UPC_E = '\x1d\x6b\x01'  # Barcode type UPC-E
BARCODE_EAN13 = '\x1d\x6b\x02'  # Barcode type EAN13
BARCODE_EAN8 = '\x1d\x6b\x03'  # Barcode type EAN8
BARCODE_CODE39 = '\x1d\x6b\x04'  # Barcode type CODE39
BARCODE_ITF = '\x1d\x6b\x05'  # Barcode type ITF
BARCODE_NW7 = '\x1d\x6b\x06'  # Barcode type NW7

# Image format
S_RASTER_N = '\x1d\x76\x30\x00'  # Set raster image normal size
S_RASTER_2W = '\x1d\x76\x30\x01'  # Set raster image double width
S_RASTER_2H = '\x1d\x76\x30\x02'  # Set raster image double height
S_RASTER_Q = '\x1d\x76\x30\x03'  # Set raster image quadruple

RESET = '\x1b\x40'

TEXT_STYLE = {
    'bold': {
        0: '\x1b\x45\x00',  # Bold font OFF
        1: '\x1b\x45\x01',  # Bold font ON
    },
    'underline': {
        None: '\x1b\x2d\x00',  # Underline font OFF
        1: '\x1b\x2d\x01',  # Underline font 1-dot ON
        2: '\x1b\x2d\x02',  # Underline font 2-dot ON
    },
    'size': {
        'normal': '\x1b\x21\x00',  # Normal text
        '2h': '\x1b\x21\x10',  # Double height text
        '2w': '\x1b\x21\x20',  # Double width text
        '2x': '\x1b\x21\x30',  # Quad area text
    },
    'font': {
        'a': '\x1b\x4d\x00',  # Font type A
        'b': '\x1b\x4d\x01',  # Font type B
        'c': '\x1b\x4d\x02',  # Font type C (may not support)
    },
    'align': {
        'left': '\x1b\x61\x00',  # Left justification
        'right': '\x1b\x61\x02',  # Right justification
        'center': '\x1b\x61\x01',  # Centering
    },
    'inverted': {
        False: '\x1d\x42\x00',  # Inverted mode ON
        True: '\x1d\x42\x01',  # Inverted mode OFF
    },
    'color': {
        1: '\x1b\x72\x00',  # Select 1st printing color
        2: '\x1b\x72\x00',  # Select 2nd printing color
    }
}

PAGE_CP_SET_COMMAND = '\x1b\x74'
PAGE_CP_CODE = {
    'cp437': 0,
    # 'katakana'  : 1,
    'cp850': 2,
    'cp860': 3,
    'cp863': 4,
    'cp865': 5,
    'cp1251': 6,
    'cp866': 7,
    'mac_cyrillic': 8,
    'cp775': 9,
    'cp1253': 10,
    'cp737': 11,
    'cp857': 12,
    'iso8859_9': 13,
    'cp864': 14,
    'cp862': 15,
    'iso8859_2': 16,
    'cp1253': 17,
    'cp1250': 18,
    'cp858': 19,
    'cp1254': 20,
    # 'TIS_14'    : 21,
    # 'TIS_17'    : 22,
    # 'TIS_11'    : 23,
    'cp737': 24,
    'cp1257': 25,
    'cp847': 26,
    # 'cp720'     : 27,
    'cp885': 28,
    'cp857': 29,
    'cp1250': 30,
    'cp775': 31,
    'cp1254': 32,
    # ''          : 33,
    'cp1256': 34,
    'cp1258': 35,
    'iso8859_2': 36,
    'iso8859_3': 37,
    'iso8859_4': 38,
    'iso8859_5': 39,
    'iso8859_6': 40,
    'iso8859_7': 41,
    'iso8859_8': 42,
    'iso8859_9': 43,
    'iso8859_15': 44,
    # '???'       : 45,
    'cp856': 46,
    'cp874': 47,
}

replaces = [
    ("{BoldOff}", '\x1b\x46'),
    ("{Cut}", PAPER_FULL_CUT),
    ("{BoldOn}", '\x1b\x45'),
    ("{CondensedOff}", '\x12'),
    ("{CondensedOn}", '\x0f'),
    ("{Cpi15}", '\x1b\x67'),
    ("{Cpi12}", '\x1b\x4d'),
    ("{Cpi10}", '\x1b\x50'),
    ("{Eject}", '\x0c'),
    ("{ItalicOff}", '\x1b\x35'),
    ("{ExpandedOff}", '\x1b\x57\x00'),
    ("{ExpandedOn}", '\x1b\x57\x01'),
    ("{ItalicOn}", '\x1b\x34'),
    ("{LinesInch6}", '\x1b\x32'),
    ("{LinesInch8}", '\x1b\x30'),
    ("{Normal}", '\x1b\x50'),
    ("{Reset}", RESET),
    ("{UnderlineOff}", '\x1b\x2d\x00'),
    ("{UnderlineOn}", '\x1b\x2d\x01'),
    ("#n#r", '\x0a\x0d'),
    ('{left}', '\x1b\x61\x00'),
    ('{right}', '\x1b\x61\x02'),
    ('{center}', '\x1b\x61\x01'),
    ('{sizenormal}', '\x1b\x21\x00'),
    ('{size2h}', '\x1b\x21\x10'),
    ('{size2w}', '\x1b\x21\x20'),
    ( '{size2x}', '\x1b\x21\x30')
]

'''
Epson FX Printer Codes


	Printer Operation:
	Decimal      ASCII		    Description
	 7	     BEL	  Beeper
	17	     DC1	  Select printer
	19	     DC3	  Deselect printer
	27 25 48     ESC EM 0	  Turn cut sheet feeder control off
	27 25 52     ESC EM 4	  Turn cut sheet feeder control on
	27 56	     ESC 8	  Disable paper out sensor
	27 57	     ESC 9	  Enable paper out sensor
	27 60	     ESC <	  Select unidirectional mode for one line
	27 64	     ESC @	  Initialize printer
	27 85 48     ESC U 0	  Cancel unidirectional mode
	27 85 49     ESC U 1	  Select unidirectional mode
	27 115 48    ESC s 0	  Turn half speed mode off
	27 115 49    ESC s 1	  Turn half speed mode on

	Vertical/Horizontal Motion:
	Decimal      ASCII		    Description
	 8	     BS 	  Backspace
	 9	     HT 	  Horizontal tab
	10	     LF 	  Line Feed
	11	     VT 	  Vertical Tab
	12	     FF 	  Form Feed
	27 47 c      ESC / c	  Select vertical tab channel (c=0..7)
	27 48	     ESC 0	  Select 8 lines per inch
	27 49	     ESC 1	  Select 7/72 inch line spacing
	27 50	     ESC 2	  Select 6 lines per inch
	27 51 n      ESC 3 n	  Select n/216 inch line spacing (n=0..255)
	27 65 n      ESC A n	  Select n/72 inch line spacing (n=0..85)
	27 66 0      ESC B NUL	  Clear Vertical tabs
	27 66 tabs   ESC B tabs   Select up to 16 vertical tabs where tabs are
				  ascending values from 1..255 ending with NUL
	27 67 n      ESC C n	  Select page length in lines (n=1..127)
	27 67 48 n   ESC C 0 n	  Select page length in inches (n=1..22)
	27 68 0      ESC D NUL	  Clears all horizontal tables
	27 68 tabs 0 ESC D tabs NUL  Sets up to 32 horizontal tabs with
				  ascending values 1-137.  NUL or a value
				  less than previous tab ends command.
	27 74 n      ESC J n	  Immediate n/216 inch line feed (n=0..255)
	27 78 n      ESC N n	  Select skip over perforation (n=1..127)
	27 79	     ESC O	  Cancel skip over perforation
	27 81 n      ESC Q n	  Set right margin (n=column)
	27 98 b c 0  ESC b c NUL  Clear vertical tabs in channel (c=0..7)
	27 98 c tabs ESC b c tabs Select up to 16 vertical tabs in channels
				  (c=0..7) where tabs are ascending values
				  from 1..255 ending with NUL
	27 101 48 s  ESC e 0 s	  Set horizontal tab to increments of 's'
	27 101 49 s  ESC e 1 s	  Set vertical tab to increments of 's'
	27 102 48 s  ESC f 0 s	  Set horizontal skip to increments of 's'
	27 102 49 s  ESC f 1 s	  Set vertical skip to increments of 's'
	27 106 n     ESC j n	  Reverse linefeed (n/216 inch after buffer)
	27 108 n     ESC l n	  Set left margin (n=column)

	Printing Style:
	Decimal      ASCII		    Description
	27 33 n      ESC ! n	  Master select where n is a combination of:
				    0  Pica		 16  Double Strike
				    1  Elite		 32  Double Wide
				    4  Condensed	 64  Italic
				    8  Emphasized	128  Underline
				  Pica & Elite and Condensed/Emphasized are
				  mutually exclusive
	27 107 48    ESC k 0	  Select NLQ Roman font
	27 107 49    ESC k 1	  Select NLQ Sans Serif font
	27 120 48    ESC x 0	  Select draft mode
	27 120 49    ESC x 1	  Select NLQ mode

	Print Size and Character Width:
	Decimal     ASCII		   Description
	14	    SO		  Select double width for one line
	15	    SI		  Select condensed mode
	18	    DC2 	  Cancel condensed mode
	20	    DC4 	  Cancel one line double width mode
	27 14	    ESC SO	  Double width for one line (duplicate)
	27 15	    ESC SI	  Select condensed mode (duplicate)
	27 77	    ESC M	  Select elite width (12 cpi)
	27 80	    ESC P	  Select pica width (10 cpi)
	27 87 48    ESC W 0	  Cancel double width mode
	27 87 49    ESC W 1	  Select double width mode

	Print Enhancement:
	Decimal     ASCII		   Description
	27 45 48    ESC - 0	  Cancel underlining
	27 45 49    ESC - 1	  Select underlining
	27 69	    ESC E	  Select emphasized mode
	27 70	    ESC F	  Cancel emphasized mode
	27 71	    ESC G	  Select double strike mode
	27 72	    ESC H	  Cancel double strike mode
	27 83 48    ESC S 0	  Select superscript
	27 83 49    ESC S 1	  Select subscript
	27 84	    ESC T	  Cancel superscript/subscript

	Character Sets:
	Decimal     ASCII		   Description
	27 52	    ESC 4	  Select italic mode
	27 53	    ESC 5	  Cancel italic mode
	27 54	    ESC 6	  Enable printing of characters (128-159,255)
	27 55	    ESC 7	  Cancel [ESC 6] command
	27 82 n     ESC R n	  Select International character set where
				  numeric 'n' is:
				    0  USA		  7  Spain I
				    1  France		  8  Japan
				    2  Germany		  9  Norway
				    3  United Kingdom	 10  Denmark II
				    4  Denmark I	 11  Spain II
				    5  Sweden		 12  Latin America
				    6  Italy
	27 116 0    ESC t NUL	 Select italic character set
	27 116 1    ESC t SOH	 Select Epson character set

	User Defined Characters:
	Decimal		ASCII			Description
	27 37 0      ESC % NUL		Selects normal character set
	27 37 1      ESC % SOH		Selects user defined set
	27 38 0      ESC & NUL ?	Select user defined chars (see manual)
	27 58 0 0 0  ESC : NUL NUL NUL	Copy ROM into RAM

	Graphics Character Sets:
	Decimal		ASCII			Description
	27 42 0 n1 n2  ESC * NUL n1 n2	Select single density graphics
	27 42 1 n1 n2  ESC * SOH n1 n2	Select double density graphics
	27 63 s n      ESC ? s n	Reassign graphics mode
					's'=(K,L,Y or Z) to mode 'n'=(0..6)
	27 75 n1 n2    ESC K n1 n2	Single density graphics (60 dpi)
	27 76 n1 n2    ESC L n1 n2	Double density graphics (120 dpi)
	27 89 n1 n2    ESC Y n1 n2	Hi-speed double den graphics (120 dpi)
	27 90 n1 n2    ESC Z n1 n2	Quad density graphics (240 dpi)
	27 94 m n1 n2  ESC ^ m n1 n2	Select 9 pin graphics mode

	number of columns = n1 + (n2 * 256)

	Other:
	Decimal      ASCII		    Description
	 13	     CR 	  Carriage Return
	 24	     CAN	  Cancel text in line (but not control codes)
	127	     DEL	  Delete character (but not control codes)
	 27 32 n     ESC SP n	  Space in n/72 inch following each NLQ char
	 27 35	     ESC #	  MSB control sequence cancel
	 27 36	     ESC $	  Select absolute dot position
	 27 61	     ESC =	  MSB = 0
	 27 62	     ESC >	  MSB = 1
	 27 73 48    ESC I 0	  Cancel above [ESC I 1]
	 27 73 49    ESC I 1	  Printable codes expansion (0-31,128-159)
	 27 92	     ESC \	  Select relative dot position
	 27 97	n    ESC a n	  NLQ justification where numeric 'n' is:
				    0  left justification  (default)
				    1  center
				    2  right justification
				    3  full justification
	 27 112      ESC p	  Select/cancel proportional mode


	- the codes listed are relative to the Epson LX 800
	- in several situations where a numeric value of zero or one is
	  required, the ASCII value of the number can be substituted
'''