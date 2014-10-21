'''
Created on Oct 21, 2014

@author: baskaran_k
'''
from scipy import mean,var,sqrt
from random import sample
from scipy.stats.mstats import zscore

class calZScore:
    
    def zvalue(self,core,surface,sampleSize):
        self.core=core
        self.surface=surface
        self.sampleSize=sampleSize
        coreMean=mean(self.core)
        s=[]
        for i in range(self.sampleSize):
            s.append(mean(sample(self.surface,len(self.core))))
        sig= sqrt(var(s))
        return (coreMean-mean(s))/sig
    
    def zvalue2(self,coreRes,surfaceRes,allEnropies):
        self.coreRes=coreRes
        self.surfaceRes=surfaceRes
        self.allEntropies=allEnropies
        z=zscore(allEnropies)
        corez=[z[surfaceRes.index(i)] for i in coreRes]
        return mean(corez)