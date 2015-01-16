#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv,codecs,cStringIO

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        '''next() -> unicode
        This function reads and returns the next line as a Unicode string.
        '''
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

with open('rady.csv','rb') as fin, open('result.csv','wb') as fout:
    writer = UnicodeWriter(fout, quoting=csv.QUOTE_ALL)
    spamreader = csv.reader(fin, delimiter=',', quotechar='"')
    for row in spamreader:
        print row[0]
        row = [v.decode('utf8') if isinstance(v, str) else v for v in row]
        if row[2]:
            splitted_row3 = row[3].split(',')
            if splitted_row3.__len__() == 6:
                writer.writerow([row[0],
                 row[1],
                 row[2],
                 splitted_row3[0],
                 splitted_row3[1],
                 splitted_row3[2],
                 splitted_row3[3],
                 splitted_row3[4],
                 splitted_row3[5],
                 ])
            if splitted_row3.__len__() == 5:
                writer.writerow([row[0],
                 row[1],
                 row[2],
                 splitted_row3[0],
                 splitted_row3[1],
                 splitted_row3[2],
                 splitted_row3[3],
                 splitted_row3[4],
                 '',
                 ])
            if splitted_row3.__len__() == 4:
                writer.writerow([row[0],
                 row[1],
                 row[2],
                 splitted_row3[0],
                 splitted_row3[1],
                 splitted_row3[2],
                 splitted_row3[3],
                 '',
                 '',
                 ])
        else:
            writer.writerow([row[0],row[1],row[2],'','','','','','','',])
