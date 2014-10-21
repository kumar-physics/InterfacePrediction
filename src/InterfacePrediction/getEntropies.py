'''
Created on Oct 21, 2014

@author: baskaran_k
'''

from MySQLdb import Connect
from string import atoi,atof
from calZScore import calZScore

class getEntopies:
    
    def readMySQLdb(self,pdbName,interfaceId,side,host,user,passwd,dbName):
        self.pdbName=pdbName
        self.interfaceId=interfaceId
        self.side=side
        self.host=host
        self.user=user
        self.passwd=passwd
        self.dbName=dbName
        dbConnection=Connect(host=host,user=user,passwd=passwd,db=dbName)
        cur=dbConnection.cursor()
        cur.execute("select r.pdbResidueNumber,r.region,r.entropyScore \
        from Residue as r inner join Interface as i on i.uid=r.interfaceItem_uid \
        where i.pdbCode='%s' and i.interfaceId=%d and r.side=%d and r.region>=0;"%(self.pdbName,self.interfaceId,self.side))
        self.entropyScore= list(cur.fetchall())
        return self.entropyScore
    
    def getAllSurfaceResidues(self):
        self.allsurfaceResidues=[atoi(res[0]) for res in self.entropyScore]
        return self.allsurfaceResidues
    
    def getAllSurfaceEntropies(self):
        self.allsurfaceEntropies=[atof(res[2]) for res in self.entropyScore]
        return self.allsurfaceEntropies
    
    def getSurfaceEntropies(self):
        self.surfaceEntropies=[atof(res[2]) for res in self.entropyScore if res[1]==0 or res[1]==1]
        return self.surfaceEntropies
    
    def getSurfaceResidues(self):
        self.surfaceResidues=[atoi(res[0]) for res in self.entropyScore if res[1]==0 or res[1]==1]
        return self.surfaceResidues
    
    def get70CoreResidues(self):
        self.core70Residues=[atoi(res[0]) for res in self.entropyScore if res[1]>1]
        return self.core70Residues
        
    def get70CoreEntropies(self):
        self.core70Entropies=[atof(res[2]) for res in self.entropyScore if res[1]>1]
        return self.core70Entropies
    
    def get95CoreResidues(self):
        self.core95Residues=[atoi(res[0]) for res in self.entropyScore if res[1]>2]
        return self.core95Residues
        
    def get95CoreEntropies(self):
        self.core95Entropies=[atof(res[2]) for res in self.entropyScore if res[1]>2]
        return self.core95Entropies


if __name__=="__main__":
    from sys import argv
    p=getEntopies()
    s=calZScore()
    p.readMySQLdb(argv[1], atoi(argv[2]), atoi(argv[3]), argv[4], argv[5], argv[6], argv[7])
    print len(p.getAllSurfaceResidues()),len(p.getSurfaceResidues()),len(p.get70CoreResidues()),len(p.get95CoreResidues())  
    print p.get70CoreResidues(),p.get95CoreResidues(),s.zvalue(p.get70CoreEntropies(), p.getSurfaceEntropies(), 1000)
    print s.zvalue2(p.get70CoreResidues(), p.getAllSurfaceResidues(), p.getAllSurfaceEntropies())  