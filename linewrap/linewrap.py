# -*- coding: utf8 -*-

import os, sys
import string
import collections
import codecs

Token = collections.namedtuple('Token', ['data','type', 'length'])

PUNCTUATION = u".,:;!?-(){}[]<>\"„”«»"

class Tokenizer(object):
    LETTERS = 0
    PUNCTUATION = 1
    WHITESPACE = 2
    NEWLINE = 3
    OTHER = 4
    
    def __init__(self, stream):
        self.stream = stream
    
    def processStream(self):
        
        x = self.stream.read(1)
        mode = self.getMode(x)
        buff = [x]
        
        while True:
            x = self.stream.read(1)
            
            if not x:
                if len(buff):
                    yield Token(u''.join(buff), mode, len(buff))
                
                raise StopIteration
            
            if self.getMode(x) != mode:
                yield Token(u''.join(buff), mode, len(buff))
                
                mode = self.getMode(x)
                buff = []
            
            buff.append(x)
    
    @staticmethod
    def getMode(char):
        if char.isalnum():
            return Tokenizer.LETTERS
        if char in PUNCTUATION: # string.punctuation:
            return Tokenizer.PUNCTUATION
        if char == '\n':
            return Tokenizer.NEWLINE
        if char in string.whitespace:
            return Tokenizer.WHITESPACE
        
        return Tokenizer.OTHER

def _findBreakPoint(current):
    breakPoint = 0
    
    for i, token in enumerate(current):
        prev = current[i-1] if i > 0 else None
        
        if prev and token.type == Tokenizer.WHITESPACE and (
            prev.type == Tokenizer.PUNCTUATION or (prev.type == Tokenizer.LETTERS and prev.length > 3)):
            
            breakPoint = i + 1
    
    return breakPoint
        
def wrapper(tokenizer, out):
    current = []
    previous = []
    next = []
    
    maxLen = 79
    
    curLen = lambda a = None: sum((t.length for t in current)) + (a.length if a is not None else 0)
    
    for token in tokenizer.processStream():
        
        if curLen(token) > maxLen or token.type == Tokenizer.NEWLINE:
            
            if token.type == Tokenizer.PUNCTUATION:
                if current[-1].length + token.length <= maxLen:
                    next.append(current.pop()) 
            
            if token.type in (Tokenizer.WHITESPACE, Tokenizer.OTHER):
                needed = maxLen - curLen()
                if needed > 0:
                    curLineData, nexLineData = token.data[:needed], token.data[needed:]
                    curToken = Token(curLineData, token.type, len(curLineData))
                    nextToken = Token(nexLineData, token.type, len(nexLineData))
                    
                    current.append(curToken)
                    token = nextToken
            
            if current[-1].type == Tokenizer.LETTERS and current[-1].length <= 3:
                    
                breakPoint = _findBreakPoint(current)
                
                if breakPoint > 0:
                    tmpBuffer = []
                    for dummy in range(breakPoint, len(current)):
                        tmpBuffer.append(current.pop())
                    next.extend(reversed(tmpBuffer))
                    
                    
            next.append(token)
            
            map(out.write, (t.data for t in current))
            
            if token.type != Tokenizer.NEWLINE:
                out.write('\n')
            
            previous, current, next = current, next, []
        
        else:
            current.append(token)
    
    map(out.write, (t.data for t in current))
    
    if current[-1].type != Tokenizer.NEWLINE:
        out.write('\n')


def tokenizeStdin():
    utfStdin = codecs.getreader('utf8')(sys.stdin)
    tokenizer = Tokenizer(utfStdin)

    wrapper(tokenizer, sys.stdout)

if __name__ == '__main__':
    tokenizeStdin()



