from collections import OrderedDict
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextLineHorizontal
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

__author__ = 'jijoy'


def parsepdf(filename):
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    # Create a PDF device object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    found_randers = False
    found_aarhus = False
    _randers = []
    headings = [u'Ledige lejligheder\n',u'afd. adresse\n',u'rum m2\n',u'leje \n',
                u'a\xb4c varme a\xb4c vand\n',u'indskud\n',u'ledig pr.\n',u'bem\xe6rkning\n'
                ]
    location_map = OrderedDict()
    header_ycord = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()

        for obj in layout._objs:
            # print obj
            if isinstance(obj,LTTextBoxHorizontal):
                for o in obj._objs:
                    y0 = o.y0
                    # print o
                    if isinstance(o,LTTextLineHorizontal) and obj.get_text() not in headings:

                        if y0 not in header_ycord:
                            if y0 in location_map :
                                objs = location_map.get(y0)
                            else:
                                objs = []
                            string_val = o.get_text().encode('ascii', 'ignore')
                            string_val = string_val.replace('\n','')
                            objs.append(string_val)
                            location_map.__setitem__(y0,objs)
                    else :
                        if y0 not in header_ycord:
                            header_ycord.append(y0)





    for key in location_map:
        print '**************************'
    #     # print key
        print location_map.get(key)
        print '**************************'
    print 'Total Rowss = %s'%len(location_map)
if __name__ == '__main__':
    parsepdf("ledige-lejligheder-29-05-2015.pdf")