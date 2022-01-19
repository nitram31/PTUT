#!/usr/bin/python
"""
   Interface to external transmembrane prediction programs.

   NAME   : TMpred.py
   TYPE   : module 
   PYTHON : 1.5.2
   VERSION: 1.0
   AUTHOR : Arne Mueller
   DATE   : 03.09.99

   DESCRIPTION:
   The module TMpred provides a generic interface to different transmembrane
   prediction methods. These methods can be implemented as local programs,
   http-services or as python code inside this module. The class GenericTM
   called with the name of a method returns a prediction object. The prediction
   object is always of the same structure and requires always the same input
   structure.

   To generate a prediction object you have to provide a list of objects with
   an attribute 'seqstr' that represents a protein sequences in a format that
   is suitable for the prediction methods (e.g. fasta format or a plain sequence
   string). The choosen prediction method will use this string to perform it's
   predition.

   The result of the prediction is a list of TM (transmembrane) objects for each
   of the objects in the list.

   A TM object always gives you the following attributes:
   method (string): the name of method to perform the prediction
   score          : a number or string representing a score if available 
   inside (int)   : the residue number of the inside part of the helix
   outside (int)  : outside residue number of TM-helix

   Some methods do not provide a sensible score per predicted TM region and
   accordingly the score is set to 0.0. Also some methods cannot predict
   inside/outside, in these cases indise represents the N-terminus and outside
   the C-terminus of the predicted TM-helix. Check the doc strings of the classes
   to see which TM attributes are sensibly set and which input format is required.
 
   EXAMPLE:
   # 'seq' is a list of objects that keep protein sequence information.
   # Assume each 'seq' object contains an attribute 'name' and 'data'
   # representing the sequence name and the aminoacid sequence.
   seq = Read_a_list_of_sequences(sequence_file_name)
   # generate the 'seqstr' for each sequence in an appropiate format
   # for the prediction method you'll choose (here fasta format).
   for s in seq:
     s.seqstr = '>%s\n%s\n' % (s.name, s.data)
   import TMpred
   # generate the prediction object, the first argument spe3cifies the
   # prediction method, the second (optional and can be set later) the
   # list on which the prediction will be performed. Note that this is
   # a call by reference and the prediction will insert a list of 'tm'
   # objects in each element of your original 'seq' list!
   tm_pred = TMpred.GenericTM('TMHMM', seq) 
   tm_pred.predict() # run the prediction
   # print out the 'seqstr' and all TM predictions for all sequences,
   # if for a sequence no TM region was predicted the 'tm' list is
   # empty.
   for s in seq:
     print s
     for tm in s.tm:
       print tm.inside, tm.outside, tm.score
   
   NOTES:
   Implemented methods (classes):
   o Memesat (local), David Jones
   o Toppred2 (local), E. Wallin & G. von Heijne (working under linux
     only!)
   o GES (encoded in this module), Arne Mueller (Engelman's GES
     hydrophobicity scale over sliding window)
   o HMMTOP (web service, http://www.enzim.hu/hmmtop/), G.E Tusnady
   o TMHMM (local), version 1.0 Anders Krogh

   See class doc strings !!!
"""

import sys
import os
import string
import time

###
### Classes
###

class TMengine:
    """
    Abstract class, inherits to different TM prediction methods
    """
    
    def __init__(self, interface):
        self.cutoff = 0.0
        ### refrerence to calling interface object
        self.generic = interface

    def predict(self):
        import tempfile
        tempfile.tempdir = '/tmp'
        tmp = tempfile.mktemp()
        self.generic.output = []
        for obj in self.generic.obj:
            f = open(tmp, 'w')
            f.write('%s\n' % obj.seqstr)
            f.close()
            cmd = self.prog + ' ' + self.opt + ' ' + tmp
            try:
                p = os.popen(cmd, 'r')
                output = p.read()
                self.generic.output.append(output)
                obj.tm = self.postProcess(output)
            finally:
                try:
                    os.remove(tmp)
                except: pass
                
class TM:
    """
    Prediction class holding the results of a transmembrane
    prediction for one (sequence) object
    """

    def __init__(self):
        self.score = 0.0
        self.inside = 0
        self.outside = 0
        self.method = None

class GenericTM:
    """
    User class, the generic interface between a specific method
    and the data.

    ARGUMENTS:
    method: a string giving the name of the method (class) to be used
            for the prediction
    obj   : optional list keeping the objects the prediction will be
            performed on (can be set later but befor prediction off
            course.
    """

    def __init__(self, method, obj=[]):
        self.obj = obj
        self.mark = '.'
        self.finished = 100
        try:
            self.method = eval('%s(self)' % method)
        except NameError:
            sys.stderr.write('ERROR: %s is not a valid method\n' % method)

    def predict(self):
        self.method.predict()
        
###
### Class implementation for different prediction methods
###
        
class Toppred(TMengine):

    """
    Toppred2, version 1

    local method, has to be installed somewhere in the system

    INPUT-FORMAT: plain sequence string 

    NOTE: strange C++ program, managed to compile with gcc under linux
    only! The score is a string, a region is only accepted as a TM region
    is the score is 'certain'.
    """

    SyntaxError = 'invalid filefomrmat for Toppred (line, linenr)'
    
    def __init__(self, interface):
        TMengine.__init__(self, interface);
        self.cutoff = 'Certain'
        ### program parameters
        self.prog = 'toppred '
        self.opt = ' --prokaryot --resultfiles tmList -p '

    def postProcess(self, input):
        pred = []
        a = string.find(input, 'Certainity\n') + 11
        b = string.find(input, '---', a) - 2
        input = string.strip(string.rstrip(input[a:b]) )
        data = string.split(input, '\n')
        for i in data:
            e = string.split(i)
            if len(e) != 5: break
            tm = TM()
            tm.inside  = string.atoi(e[1])
            tm.outside = string.atoi(e[2])
            tm.score   = e[4]
            tm.method = self
            if tm.score == self.cutoff:
                pred.append(tm)
        return pred
        
                
class Memsat(TMengine):

    """
    Memsat, version 1.7

    local method, has to be installed somewhere in the system

    INPUT-FORMAT: fasta
    """

    def __init__(self, interface):
        TMengine.__init__(self, interface);
        self.cutoff = 1.0
        ### program parameters
        self.prog = 'memsat'
        self.opt = '-m19 -x30 '
                
    def postProcess(self, input):
        data = string.split(input, '\n')
        pred = []
        data.reverse()
        while data:
            if data[len(data)-1] == 'FINAL PREDICTION':
                data.pop()
                data.pop()
                while data and data[len(data)-1]:
                    p = self.processTM(data[len(data)-1])
                    #if abs(p.score) >= self.cutoff:
                    if p.score >= self.cutoff:
                        p.method = self
                        pred.append(p)
                    data.pop()
                break
            data.pop()
        return pred

    def processTM(self, str):
        fin = string.split(str)
        fin.reverse()
        p = TM()
        self.key = 'in'
        if len(fin) >= 4: # first entry
            fin.pop()
            self.key = fin[len(fin)-1][1:-1] # either 'in' or 'out'
        fin.pop()
        tmp = string.split(fin[len(fin)-1], '-', 2)
        if self.key == 'in':
            inside = string.atoi(tmp[0])
            outside = string.atoi(tmp[1])
        else:
            outside = string.atoi(tmp[0])
            inside = string.atoi(tmp[1])
        fin.pop()
        p.inside = inside
        p.outside = outside
        p.score = string.atof(fin[0][1:-1])
        return p
    
class GES(TMengine):
    """
    GES, sequence sliding window over GES (Engelman hydrophobicity)
    scale

    Implementation in this class.

    INPUT-FORMAT: plain sequence string. 
    
    Engelman et al (1986), Ann Rev. Biophys. Chem. 115; 321-53 986

    NOTES: no topology prediction, inside/outside corresponds to N-terminus
    and C-terminus of the TM region.
    
    """
    
    ### GES scale
    ges = {'A': -1.60,  'a': -1.60,
           'B':  7.00,  'b':  7.00,
           'C': -2.00,  'c': -2.00,
           'D':  9.20,  'd':  9.20,
           'E':  8.20,  'e':  8.20,
           'F': -3.70,  'f': -3.70,
           'G': -1.00,  'g': -1.00,
           'H':  3.00,  'h':  3.00,
           'I': -3.10,  'j': -3.10,
           'K':  8.80,  'k':  8.80,
           'L': -2.80,  'l': -2.80,
           'M': -3.40,  'm': -3.40,
           'N':  4.80,  'n':  4.80,
           'P':  0.20,  'p':  0.20,
           'Q':  4.10,  'q':  4.10,
           'R': 12.30,  'r': 12.30,
           'S': -0.60,  's': -0.60,
           'T': -1.20,  't': -1.20,
           'V': -2.60,  'v': -2.60,
           'W': -1.90,  'w': -1.90,
           'X':  0.00,  'x':  0.00,
           'Y':  0.70,  'y':  0.70,
           'Z':  6.15,  'z':  6.15,
           '*':  0.00,  '-':  0.00             
           }

    def __init__(self, interface):
        TMengine.__init__(self, interface);
        ### program parameters
        self.scale = GES.ges # hydrophobicity scale
        self.cutoff = -1.2   # hydrophobicity cutoff (below which a TM is considered) 
        self.window = 20     # length of sliding windwo for averaging hydrophobicity
        self.min = 19
        self.max = 30

    def scale_sum(self, region):
        h = 0.0
        for r in region:
            h = h + self.scale[r]
        return h

    def predict(self):
        self.generic.output = []
        processed = 0
        for obj in self.generic.obj:
            ### calculate average hydrophobicity for query sequence in sliding window
            obj.avghyphob = len(obj.seqstr) * [[0.0], 0]
            last = len(obj.seqstr)
            for n in range(last):
                best = [1000000.0, 0]
                finish = 0
                for w in range(self.min, self.max + 1):
                    m = n + w
                    if m > last:
                        w = w - (m - last)
                        m = last
                        finish = 1                 
                    score = self.scale_sum(obj.seqstr[n:m]) / w
                    if score < best[0]:
                        best = [score, w]
                    if finish: break
                obj.avghyphob[n] = best
            ### look for TM regions in precalculated hydrophobicity scores
            max = last - 1
            obj.tm = []
            n = 0
            while n <= max: # go through whole sequence
                if obj.avghyphob[n][0] < self.cutoff: # TM region ?
                    tm = TM()
                    tm.inside = n + 1
                    tm.outside = n + obj.avghyphob[n][1]
                    tm.score = obj.avghyphob[n][0]
                    tm.method = self
                    obj.tm.append(tm)
                    n = n + obj.avghyphob[n][1]
                else:
                    n = n + 1
            processed = processed + 1
            if processed >= self.generic.finished:
                sys.stderr.write(self.generic.mark)
                processed = 0
        # delattr(self, 'generic')
        sys.stderr.write('\n')


class HMMTOP(TMengine):
    """
    HMMTOP

    web-service on http://www.enzim.hu/hmmtop/hmmtop.cgi

    INPUT-FORMAT: Name separated by ',' from data
                  sequence_name,sequene_data
    """

    def __init__(self, interface):
        TMengine.__init__(self, interface);
        self.timeout = 10
        self.server = 'www.enzim.hu'
        self.prog = '/hmmtop/hmmtop.cgi'
        self.opt  = ''

    def predict(self):
        import http
        self.generic.output = []
        
        for obj in self.generic.obj:
            name, sequence = string.split(obj.seqstr, ',')
            request = "format=FAS&seqp=>%s%%0A%s&%s" % (name, sequence, self.opt)  
            length = '%s' % len(request)
            failures = 0
            while failures < self.timeout:
                self.h = HTTP(self.server)
                self.h.putrequest('POST', self.prog)
                self.h.putheader('Content-type', 'application/x-www-form-urlencoded')
                self.h.putheader('Content-length', length)
                self.h.endheaders()
                self.h.send(request)
                errcode, errmsg, headers = self.h.getreply()
                if errcode != 200:
                    failures = failures + 1
                    print(errcode, errmsg, headers)
                    sys.stderr.write('error in reply from server: (%d, %s)' % (errcode,errmsg))
                    time.sleep(10)
                else:
                    break
            if failures ==  self.timeout:
                sys.stderr.write('error in %s! Giving up after %d trials ...' % (name,failures))
            sys.stderr.write('got good reply for %s ...\n' % name)
            f = self.h.getfile()
            data = f.read()
            f.close()
            self.generic.output.append(data)
            obj.tm = self.postProcess(data)

    def postProcess(self, data):
        result = []
        lines = string.split(data, '\n')
        i = 0
        for l in lines:
            if l and l[:6] == 'Number':
                n = string.split(l)
                if n[len(n) - 1] == '0':
                    return result
                else:
                    i = i + 1
                    break
            i = i + 1
        is_block = 0
        while i < len(lines):
            l = lines[i]
            if l[:8] == 'Position':
                is_block = 1
            elif is_block:
                n = string.split(l)
                if len(n) == 3:
                    tm = TM()
                    tm.inside = string.atoi(n[1])
                    tm.outside = string.atoi(n[2])
                    tm.score = 0.0
                    tm.method = self
                    result.append(tm)
                else:
                    return result
            i = i + 1    
        return result

class TMHMM(TMengine):
    """
    TMHMM version 1.0

    local method, has to be installed somewhere in the system

    Erik L.L. Sonnhammer, Gunnar von Heijne, and Anders Krogh:
    A hidden Markov model for predicting transmembrane helices in protein
    sequences. In J. Glasgow et al., eds.: Proc. Sixth Int. Conf. on Intelligent
    Systems for Molecular Biology, pages 175-182. AAAI Press, 1998.

    INPUT-FORMAT: fasta.

    NOTES: The score is meaningless (always 0.0)

    CONTACT: Anders Krogh, krogh@cbs.dtu.dk
    """
    
    def __init__(self, interface):
        TMengine.__init__(self, interface);
        ### program parameters
        self.prog = 'decodeanhmm '
        ### option's file + prepare reading from stdin ... 
        self.opt = '-f /bmm/soft/IRIX_6.5/TMHMM1.0/TMHMM1.0.options <'
        import re
        self.descr = re.compile('\?0\s+([oOMi]+)')

    def postProcess(self, input):
        residues = ''
        input = string.split(input, '\n')
        for line in input:
            match = self.descr.search(line)
            if match: residues = residues + match.group(1)
        location = 'inside'
        new = 1
        pred = []
        for i in range(len(residues)):
            r = residues[i]
            if r != 'M':
                if r == 'i':
                    location = 'inside'
                elif r == 'o' or 'O' == r:
                    location = 'outside'
                if not new:
                    exec('tm.%s = %d' % (location, i))
                    pred.append(tm)
                    new = 1
            elif new:
                tm = TM()
                tm.method = self
                exec('tm.%s = %d' % (location, i + 1))
                new = 0
        return pred
    
###
### Testing ...
###

if __name__ == '__main__':
    print('Testing ...')
    import seq
    f = open('/bmm/home/mueller/jdat/MG/MG.pep')
    #f = open('/bmm/home/mueller/tmp/MG038.fasta')
    #f = open('/bmm/home/mueller/bio_soft/memsat/example.seq')
    #f = open('/bmm/home/mueller/lang/Python/test.pep')
    dat = seq.ReadFastaFile(f)
    for i in dat:
        i.seqstr = '%s\n' % i
    g = GenericTM('TMHMM')
    g.obj = dat
    g.predict()
    for o in g.obj:
        print(o.seqstr)
        for i in o.tm: 
            print('inside = %d, outside = %d'%(i.inside,i.outside))
