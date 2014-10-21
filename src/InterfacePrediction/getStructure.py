'''
Created on Oct 21, 2014

@author: baskaran_k
'''


from Bio.PDB import MMCIFParser


class getStructure:
    
    def getAtoms(self,pdbName,chainId,cifrepo):
        self.pdbName=pdbName
        self.chainId=chainId-1
        self.cifrepo=cifrepo
        parser = MMCIFParser()
        structure = parser.get_structure(self.pdbName, "%s/%s.cif.gz"%(self.cifrepo,self.pdbName))
        firstModel = structure.get_list()[0]
        self.chain = firstModel.get_list()[self.chainId]
        return self.chain
    
    def getSurfaceAtoms(self,surfaceRes,refRes,searchRadius):
        surfacePatch=[]
        for res in surfaceRes:
            try:
                d=self.chain[res]['CB']-self.chain[refRes]['CB']
            except KeyError:
                try:
                    d=self.chain[res]['CA']-self.chain[refRes]['CA']
                except KeyError:
                    print "Residue %d or %d has no CA or CB"%(res,refRes)
                    d=9999999.9999
            if d<searchRadius:
                surfacePatch.append(res)
        return surfacePatch
                    
        