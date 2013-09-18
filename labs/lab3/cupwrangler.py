
from wrangler import dw
import sys

if(len(sys.argv) < 3):
	sys.exit('Error: Please include an input and output file.  Example python script.py input.csv output.csv')

w = dw.DataWrangler()

# Split data repeatedly on '|-'  into  rows
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="row",
               update=False,
               insert_position="right",
               row=None,
               on="\\|-",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max="0",
               positions=None,
               quote_character=None))

# Cut from data on '| any lowercase word =#FFF any number  any word \|'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\|[a-z]+=#FFF\\d+[a-zA-Z]+\\|",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Extract from data between 'fb|' and '}'
w.add(dw.Extract(column=["data"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=".*",
                 before="}",
                 after="fb\\|",
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Cut from data on '{{fb| any word }}'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="{{fb\\|[a-zA-Z]+}}",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data on '|newline'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\|\n",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Split data repeatedly on newline after ' '
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="column",
               update=False,
               insert_position="right",
               row=None,
               on="\n",
               before=None,
               after=" ",
               ignore_between=None,
               which=1,
               max="0",
               positions=None,
               quote_character=None))

# Set  split  name to  1
w.add(dw.SetName(column=["split"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["1"],
                 header_row=None))

# Set  split1  name to  2
w.add(dw.SetName(column=["split1"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["2"],
                 header_row=None))

# Set  split2  name to  3
w.add(dw.SetName(column=["split2"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["3"],
                 header_row=None))

# Set  split3  name to  4
w.add(dw.SetName(column=["split3"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["4"],
                 header_row=None))

# Drop split4
w.add(dw.Drop(column=["split4"],
              table=0,
              status="active",
              drop=True))

# Drop split5
w.add(dw.Drop(column=["split5"],
              table=0,
              status="active",
              drop=True))

# Fold 1, 2, 3, 4  using  header as a key
w.add(dw.Fold(column=["_1","_2","_3","_4"],
              table=0,
              status="active",
              drop=False,
              keys=[-1]))

# Set  extract  name to  Country
w.add(dw.SetName(column=["extract"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Country"],
                 header_row=None))

# Set  fold  name to  Place
w.add(dw.SetName(column=["fold"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Place"],
                 header_row=None))

# Cut from value on ' any number   any word   any word  Cup|'
w.add(dw.Cut(column=["value"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\d+ [a-zA-Z]+ [a-zA-Z]+ Cup\\|",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Cut from value on '[\['
w.add(dw.Cut(column=["value"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\[\\[",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Cut from value on ']]'
w.add(dw.Cut(column=["value"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="]]",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Cut from value on '#1|\*'
w.add(dw.Cut(column=["value"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="#1\\|\\*",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Cut from value on '|align=center\| .'
w.add(dw.Cut(column=["value"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\|align=center\\| .",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Split value between ' ' and '('
w.add(dw.Split(column=["value"],
               table=0,
               status="active",
               drop=True,
               result="column",
               update=False,
               insert_position="right",
               row=None,
               on=".*",
               before="\\(",
               after=" ",
               ignore_between=None,
               which=1,
               max=1,
               positions=None,
               quote_character=None))

# Drop split
w.add(dw.Drop(column=["split"],
              table=0,
              status="active",
              drop=True))

# Cut from split6 on '('
w.add(dw.Cut(column=["split6"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\(",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from split6 on ')'
w.add(dw.Cut(column=["split6"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\)",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Split split6 repeatedly on ','
w.add(dw.Split(column=["split6"],
               table=0,
               status="active",
               drop=True,
               result="column",
               update=False,
               insert_position="right",
               row=None,
               on=",",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max="0",
               positions=None,
               quote_character=None))

# Delete  rows where Country is null
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.IsNull(column=[],
                table=0,
                status="active",
                drop=False,
                lcol="Country",
                value=None,
                op_str="is null")])))

# Fold split, split7, split8, split9...  using  header as a key
w.add(dw.Fold(column=["split","split7","split8","split9","split10"],
              table=0,
              status="active",
              drop=False,
              keys=[-1]))

# Drop fold
w.add(dw.Drop(column=["fold"],
              table=0,
              status="active",
              drop=True))

# Delete  rows where value is null
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.IsNull(column=[],
                table=0,
                status="active",
                drop=False,
                lcol="value",
                value=None,
                op_str="is null")])))

# Cut from value on '*'
w.add(dw.Cut(column=["value"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\*",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Set  value  name to  Year
w.add(dw.SetName(column=["value"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Year"],
                 header_row=None))

w.apply_to_file(sys.argv[1]).print_csv(sys.argv[2])


