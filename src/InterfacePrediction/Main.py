'''
Created on Oct 21, 2014

@author: baskaran_k
'''

import getEntropies
import calZScore
import getStructure
from string import atoi,atof
from pylab import hist,mean,sqrt,var
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from numpy import linspace
from MySQLdb import Connect




def runDataset(host,user,passwd,dbName,tableName,cifrepo):
    p=getEntropies.getEntopies()
    s=calZScore.calZScore()
    c=getStructure.getStructure()
    dbConnection=Connect(host=host,user=user,passwd=passwd,db=dbName)
    cur=dbConnection.cursor()
    cur.execute("select pdbCode,interfaceId from %s where h1>30 and h2>30 and pdbCode not in ('1s83','2bz6','1utj','2h7i');"%(tableName))
    pdblist=list(cur.fetchall())
    for pdb in pdblist:
        print "working on %s"%(pdb[0]) 
        p.readMySQLdb(pdb[0], pdb[1], 1, host, user, passwd, dbName)
        chain=c.getAtoms(pdb[0], 1, cifrepo)
        surfaceRes=p.getAllSurfaceResidues()
        allEntropies=p.getAllSurfaceEntropies()
        z=[]
        z2=[]
        fo=open('/home/baskaran_k/eppic_pred/bio/%s_d.dat'%(pdb[0]),'w')
        for r in surfaceRes:
            core=c.getSurfaceAtoms(surfaceRes,r, 6.0)
            coreEntropies=[allEntropies[surfaceRes.index(i)] for i in core]
            zv=s.zvalue(coreEntropies, allEntropies, 1000)
            zv2=s.zvalue2(core, surfaceRes, allEntropies)
            fo.write("%s\t%d\t%f\t%f\n"%(pdb[0],r,zv,zv2))
        fo.close()
#             z.append(zv)
#             z2.append(zv2)
#         pdf=gaussian_kde(z)
#         pdf2=gaussian_kde(z2)
#         x=linspace(-5,5,1000)
#         plt.plot(x,pdf(x),label=pdb)
#         plt.plot(x,pdf2(x),label=pdb)
#         plt.title(pdb[0])
#         plt.show()
     
def runDataset2(host,user,passwd,dbName,tableName,cifrepo,patch):
    p=getEntropies.getEntopies()
    s=calZScore.calZScore()
    c=getStructure.getStructure()
    dbConnection=Connect(host=host,user=user,passwd=passwd,db=dbName)
    cur=dbConnection.cursor()
    cur.execute("select pdbCode,interfaceId from %s where h1>30 and h2>30 and pdbCode not in ('1s83','2bz6','2qb5','2h7i');"%(tableName))
    pdblist=list(cur.fetchall())
    
    for pdb in pdblist:
        #print "working on %s"%(pdb[0]) 
        p.readMySQLdb(pdb[0], pdb[1], 1, host, user, passwd, dbName)
        chain=c.getAtoms(pdb[0], 1, cifrepo)
        surfaceRes=p.getAllSurfaceResidues()
        allEntropies=p.getAllSurfaceEntropies()
        n=int(round(len(surfaceRes)*(patch/100)))
        #print n,len(surfaceRes)
        dat=sorted([[allEntropies[i],surfaceRes[i]] for i in range(len(surfaceRes))])[:n]
        d=[]
        for i in range(len(dat)):
            for j in range(i+1,len(dat)):
                dis=chain[dat[i][1]]['CA']-chain[dat[j][1]]['CA']
                d.append(dis)
        m=mean(d)
        sig=sqrt(var(d))
        print pdb[0],m,sig
        
#         pdf=gaussian_kde(d)
#         x=linspace(0,150,1000)
#         plt.plot(x,pdf(x))
#         plt.title(pdb[0])
#         plt.show()




if __name__=="__main__":
    from sys import argv
    #runDataset(argv[1], argv[2], argv[3], argv[4], 'dc_xtal', argv[5],atof(argv[6]))
    runDataset(argv[1], argv[2], argv[3], argv[4], 'dc_bio', argv[5])
#     p=getEntropies.getEntopies()
#     s=calZScore.calZScore()
#     c=getStructure.getStructure()
#     p.readMySQLdb(argv[1], atoi(argv[2]), atoi(argv[3]), argv[4], argv[5], argv[6], argv[7])
#     chain=c.getAtoms(argv[1], 1, argv[8])
#     surfaceRes=p.getAllSurfaceResidues()
#     allEntropies=p.getAllSurfaceEntropies()
#     z=[]
#     for r in surfaceRes:
#         core=c.getSurfaceAtoms(surfaceRes,r, 6.0)
#         zv=s.zvalue2(core, surfaceRes, allEntropies)
#         z.append(zv)
#     pdf=gaussian_kde(z)
#     x=linspace(min(z),max(z),1000)
#     plt.plot(x,pdf(x))
#     plt.show()