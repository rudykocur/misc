# -*- coding: utf8 -*-
import unittest
import sys
from StringIO import StringIO
from linewrap import Tokenizer, wrapper

class LinewrapperTests(unittest.TestCase):
    def test_tokenizeStream(self):
        inputStream = StringIO(u"Jam jest jontek ... zażółć \ngęślą jaźń.")
        
        tokenizer = Tokenizer(inputStream)

        tokens = list(tokenizer.processStream())
        
        expectedData = [u'Jam', u' ', u'jest', u' ', u'jontek', u' ', u'...', u' ', u'zażółć',
                        u' ', u'\n', u'gęślą', u' ', u'jaźń', u'.']
        expectedTypes = [Tokenizer.LETTERS, Tokenizer.WHITESPACE, Tokenizer.LETTERS, Tokenizer.WHITESPACE,
                          Tokenizer.LETTERS, Tokenizer.WHITESPACE, Tokenizer.PUNCTUATION, Tokenizer.WHITESPACE,
                          Tokenizer.LETTERS, Tokenizer.WHITESPACE, Tokenizer.NEWLINE, Tokenizer.LETTERS, 
                          Tokenizer.WHITESPACE, Tokenizer.LETTERS, Tokenizer.PUNCTUATION]
        
        self.assertEqual([t.data for t in tokens], expectedData)
        self.assertEqual([t.type for t in tokens], expectedTypes)
    
    def _compare(self, input, output):
        inputStream = StringIO(input)
        out = StringIO()
        tokenizer = Tokenizer(inputStream)
        wrapper(tokenizer, out)
        
        

        try:
            self.assertEqual(out.getvalue(), output)
        except:
            print
            print
            print 'OMG FAIL'
            print 'OMG EXPECTED', repr(output)
            print 'OMG ACTUAL  ', repr(out.getvalue())
            print
            
            raise
    
    def test_simpleWrapping(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć "
                u"nad żółcie. ")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz\n"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć \n"
                u"nad żółcie. \n")
        
        self._compare(data, result)
    
    def test_doNotAddAdditionalNewlineAtEnd(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć "
                u"nad żółcie.\n")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz\n"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć \n"
                u"nad żółcie.\n")
        
        self._compare(data, result)
    
    def test_newlinesInTheMiddle(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń.\nPrzychodzem do Ciebie jako i Ty przychodzisz"
                u" do mnie.\nTegoż ten temat jest zająknięty na maxa...\nToćto hańba i srom i żółć "
                u"nad żółcie.")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń.\n"
                u"Przychodzem do Ciebie jako i Ty przychodzisz do mnie.\n"
                u"Tegoż ten temat jest zająknięty na maxa...\n"
                u"Toćto hańba i srom i żółć nad żółcie.\n")
        
        self._compare(data, result)
    
    def test_longLine(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz "
                u"lalalalalalalalaalallllllllllllllllllllllllllllllllllllllllllllllllllllllllllalalalalala")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz\n"
                u" \n"
                u"lalalalalalalalaalallllllllllllllllllllllllllllllllllllllllllllllllllllllllllalalalalala\n")
        
        self._compare(data, result)
    
    def test_longPunctuationLine(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz "
                u".............;.;.;.;.;.;>:>;.;>:>:.........>>>>>>>.....................................")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz\n"
                u" \n"
                u".............;.;.;.;.;.;>:>;.;>:>:.........>>>>>>>.....................................\n")
        
        self._compare(data, result)
    
    def test_lineWithPunctuationOnEnd(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz..."
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć "
                u"nad żółcie. ")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty \n"
                u"przychodzisz... do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba\n"
                u" i srom i żółć nad żółcie. \n")
        
        self._compare(data, result)
    
    def test_breakWhitespaces(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć   "
                u"nad żółcie. ")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz\n"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć \n"
                u"  nad żółcie. \n")
        
        self._compare(data, result)
    
    def test_punctuationAtBeginning(self):
        data = (u"... jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć "
                u"nad żółcie. ")
        
        result = (
                u"... jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty przychodzisz\n"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć \n"
                u"nad żółcie. \n")
        
        self._compare(data, result)
    
    def test_cannotEndWithShortWord(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty prz cho zi z"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć "
                u"nad żółcie. ")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako \n"
                u"i Ty prz cho zi z do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto \n"
                u"hańba i srom i żółć nad żółcie. \n")
        
        self._compare(data, result)
    
    def test_onlyShortWordsInLine(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodze do Ciebie jako i Ty przychodzisz "
                u"aa bb ccc ddd eee ff gg hhh ii jjj kkk lll mmm nnn ooo pp rr ss tt uu w x y zzz"
                u" nad żółcie. ")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodze do Ciebie jako i Ty przychodzisz \n"
                u"aa bb ccc ddd eee ff gg hhh ii jjj kkk lll mmm nnn ooo pp rr ss tt uu w x y zzz\n"
                u" nad żółcie. \n")
        
        self._compare(data, result)
    
    def test_onlyShortWordsInLineMixedWithPunctuation(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodze do Ciebie jako i Ty przychodzisz "
                u"aa bb ccc ddd eee ff gg hhh ii ... kkk lll mmm nnn ooo pp rr ss tt uu w x y zzz"
                u" nad żółcie. ")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodze do Ciebie jako i Ty przychodzisz \n"
                u"aa bb ccc ddd eee ff gg hhh ii ... \n"
                u"kkk lll mmm nnn ooo pp rr ss tt uu w x y zzz nad żółcie. \n")
        
        self._compare(data, result)
    
    def test_onlyShortWordsInLineMixedWithPunctuation2(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodze do Ciebie jako i Ty przychodzisz "
                u"aa bb ccc ddd eee ff gg hhh ii ... kkk lll mmm nnn ooo .. rr ss tt uu w x y zzz"
                u" nad żółcie. ")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodze do Ciebie jako i Ty przychodzisz \n"
                u"aa bb ccc ddd eee ff gg hhh ii ... kkk lll mmm nnn ooo .. \n"
                u"rr ss tt uu w x y zzz nad żółcie. \n")
        
        self._compare(data, result)
    
    def test_multipleParagraphs(self):
        #       u".........!.........!.........!.........!.........!.........!.........!........."
        data = (u"Jam jest jontek zażółć gęślą jaźń. Przychodze do Ciebie jako i Ty przychodzisz "
                u"aa bb ccc ddd eee ff gg hhh ii ... kkk lll mmm nnn ooo pp rr ss tt uu w x y zzz"
                u" nad żółcie. \n"
                u"\n"
                u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako i Ty prz cho zi z"
                u" do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto hańba i srom i żółć "
                u"nad żółcie. ")
        
        result = (
                u"Jam jest jontek zażółć gęślą jaźń. Przychodze do Ciebie jako i Ty przychodzisz \n"
                u"aa bb ccc ddd eee ff gg hhh ii ... \n"
                u"kkk lll mmm nnn ooo pp rr ss tt uu w x y zzz nad żółcie. \n"
                u"\n"
                u"Jam jest jontek zażółć gęślą jaźń. Przychodzem do Ciebie jako \n"
                u"i Ty prz cho zi z do mnie. Tegoż ten temat jest zająknięty na maxa... Toćto \n"
                u"hańba i srom i żółć nad żółcie. \n")
        
        self._compare(data, result)
    

if __name__ == "__main__":
    unittest.main()