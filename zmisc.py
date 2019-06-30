import sys
import random
import math
import json

class ColDef:
    MODE_INT = 'mode_int'
    MODE_STR = 'mode_str'

    def __init__(self, mode, **kwargs):
        self.mode = mode
        self.kwargs = kwargs

    @staticmethod
    def mode_int(**kwargs):
        return ColDef(ColDef.MODE_INT, **kwargs)

    @staticmethod
    def mode_str(**kwargs):
        return ColDef(ColDef.MODE_STR, **kwargs)

    def get_name(self):
        if 'name' in self.kwargs:
            return self.kwargs['name']
        return '(unnamed ColDef)'

    def get_value(self, obj):
        # if we do not have a name, see if one is available in obj
        if 'name' not in self.kwargs:
            if hasattr(obj, 'get_col_name'):
                self.kwargs['name'] = getattr(obj, 'get_col_name')()

        if 'getter' not in self.kwargs:
            assert False, 'no getter defined in %s' % (self.get_name())
        value = self.kwargs['getter'](obj)

        if (value == None) and ('null_override' in self.kwargs):
            value = self.kwargs['null_override']

        if 'remapper' in self.kwargs:
            value = self.kwargs['remapper'][value]

        if 'subst_table' in self.kwargs:
            for kk,vv in self.kwargs['subst_table'].items():
                value = str(value).replace(kk,vv)

        if 'encoding' in self.kwargs:
            # https://docs.python.org/3/howto/unicode.html
            if 'encoding_mode' in self.kwargs:
                value = str(value).encode(self.kwargs['encoding'], self.kwargs['encoding_mode'])
            else:
                value = str(value).encode(self.kwargs['encoding'])

            value = value.decode('ascii')

        return value

    def to_csv_value(self, obj):
        if self.mode == self.MODE_INT:
            return str(self.get_value(obj))
        elif self.mode == self.MODE_STR:
            return '"%s"' % (str(self.get_value(obj)))
        assert False, 'unknown mode %s in %s' % (self.mode, self.get_name())

class DictColDef:
    @staticmethod
    def mode_int(col_name, key_name, **kwargs):
        return ColDef.mode_int(name=col_name, getter=lambda obj: DictColDef.private_getter(obj, key_name), **kwargs)

    @staticmethod
    def mode_str(col_name, key_name, **kwargs):
        return ColDef.mode_str(name=col_name, getter=lambda obj: DictColDef.private_getter(obj, key_name), **kwargs)

    @staticmethod
    def private_getter(obj, key_name):
        if key_name not in obj.dict:
            return None
        return obj.dict[key_name]

def GetterColDef(col_name, getter, **kwargs):
    return ColDef.mode_str(name=col_name, getter=getter, **kwargs)

class RowDef:
    def __init__(self, *col_defs):
        self.col_defs = col_defs

    def to_csv_row(self, obj):
        values = [col_def.to_csv_value(obj) for col_def in self.col_defs]
        return ','.join(values)

def read_text_lines(text_filename):
    txt = read_file(text_filename)
    return [x.strip() for x in txt.split('\n') if len(x) > 0]

class RowDb:
    def __init__(self, raw_rows, row_class):
        self.row_class = row_class
        self.rows = []

        for ndx in range(len(raw_rows)):
            raw = raw_rows[ndx]
            #print('NDX %d of %d, ROW type %s: %s' % (ndx, len(jj), type(row), row))
            row = self.row_class(raw)
            if self.row_class.is_valid(row):
                self.rows.append(row)

    def print_rows(self, to_str_fn):
        for row in self.rows:
            print('%s' % (to_str_fn(row)))

class Args:
    def __init__(self, args):
        self.args = args
        self.ndx = 0
        self.arg_count = len(args)

    def is_empty(self):
        return self.ndx >= self.arg_count

    def get_next(self):
        assert self.ndx < self.arg_count
        result = self.args[self.ndx]
        self.ndx += 1
        return result

def scramble(seq):
    dup = [x for x in seq]
    result = []

    while len(dup) > 0:
        ndx = random.randint(0, len(dup)-1)
        result.append(dup[ndx])
        del dup[ndx]

    return result

def to_json_str(obj):
    return json.dumps(obj, indent=2)

def read_file(filename):
    ff = open(filename, 'r')
    txt = ff.read()
    ff.close()
    return txt

def read_json_file(filename):
    ff = open(filename, 'rb')
    jj =  json.load(ff)
    ff.close()
    return jj

def read_file_as_dict(filename):
    result = {}
    stripped = [x.strip() for x in read_file(filename).split('\n')]
    lines = [x for x in stripped if len(x) > 0 and x[0] != '#']
    for line in lines:
        assert '=' in line
        parts = [x.strip() for x in line.split('=')]
        assert len(parts) == 2
        result[parts[0]] = parts[1]

    return result

def parse_csv_line(txt):
    return [x.strip() for x in txt.split(',')]

def read_csv(filename):
    txt = read_file(filename)
    return [parse_csv_line(x) for x in txt.split('\n') if len(x) > 0]

def get_column_values(lines, column_number):
    ss = set()

    for line in lines:
        ss.add(line[column_number])

    result = [x for x in ss]
    result.sort()
    return result

def get_column_match_count(lines, column_number, column_value):
    total = 0

    for line in lines:
        if line[column_number] == column_value:
            total += 1

    return total

def get_column_content(lines, prime_index, prime_value, lookup_index):
    result = {}

    for line in lines:
        value = line[prime_index]
        if value == prime_value:
            matchme = line[lookup_index]
            if matchme in result:
                result[matchme] += 1
            else:
                result[matchme] = 1

    return result

def get_global_content(lines):
    result = {}

    for line in lines:
        for value in line:
            if value in result:
                result[value] += 1
            else:
                result[value] = 1

    return result
