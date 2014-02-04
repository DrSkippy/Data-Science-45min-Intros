#!/usr/bin/env python
import sys
import re
import codecs
# globals
    
#  --sans regex w/ order
str_replacements=[ #(search,replacement)
('grep_stmt=',''),
('| grep','_AND_grep'),
('|','_OR_'),
('\\b','_BG_'),
("'",''),
(',',''),
('?','_QM_'),
(' ','_'),
('/','_'),
('<','_LT_'),
('%','_PT_'),
('@','_AT_'),
('#','_SH_'),
('["]','_LQT_'),
('"','_QT_'),
('&','_AMP_'),
('$','_DOL_'),
("\\","")
]

# --regex
re_dict={ #'search':'replacement'
'[__]+':'_'
}

# unicode
reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

# replacements set
for file_name in sys.stdin:
    for search,replacement in str_replacements:
        file_name=file_name.replace(search,replacement)
    for key in re_dict:
        for item in re.findall(key,file_name):
            file_name=file_name.replace(item,re_dict[key])

# out
print file_name 

