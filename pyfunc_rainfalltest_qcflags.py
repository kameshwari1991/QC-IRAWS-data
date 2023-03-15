

def pyfunc_rainfalltest_qcflags(var,hh):
#% cc=1;last_st=0;bb=1
    cc=1
#temp=[];temp[1:len(var)+1] = var
    d = [x - var[i - 1] for i, x in enumerate(var)][1:];
    badd=[]
    ind = [jj for jj in range(len(d)) if d[jj] < 0]
    for ii in range(len(ind)):
        if (ii<=len(ind)-1) & (ind[ii] != len(var)-1):
            if (hh[ind[ii]] != 23) & (var[ind[ii]+1]<=10):
                badd.append(ind[ii])
                badd.append(ind[ii]+1)
                cc=cc+2;
            elif (var[ind[ii]+1]>10):
                if ((var[ind[ii]-1]<10) | (var[ind[ii]-2]<10) | (var[ind[ii]-3]<10)):
                    badd.append(ind[ii])
                    badd.append(ind[ii]+1)
                    cc=cc+2;
        if (cc == 1 & ii==len(ind)-1):
            badd=[];
            
    return badd
    
#%%

#badd = pyfunc_rainfalltest_qcflags(var,hour0)
        

            
            