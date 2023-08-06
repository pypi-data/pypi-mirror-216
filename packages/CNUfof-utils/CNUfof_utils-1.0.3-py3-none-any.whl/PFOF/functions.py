#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import astropy.cosmology 
import astropy.units as u
import pandas as pd
from astropy.cosmology import FlatLambdaCDM , Planck18
import time
from pydl.goddard.astro import gcirc
import astropy.units as u
import ray
import sys
sys.setrecursionlimit(10**6)



# In[ ]:


class fofradecV():
    def __init__(self,h0c,omegamc,omegalc,omegakc,c,dcondc,vcondc): 
        self.h0c = h0c 
        self.omegamc = omegamc
        self.omegalc = omegalc
        self.omegakc = omegakc
        self.c = c 
        self.dcondc = dcondc
        self.vcondc = vcondc
    
    
    def solution(self,i1,k,flag,lst,ra,de,v):
        rax = ra[i1]
        dex = de[i1]
        vx = v[i1]
        range1 = np.where(flag != 1)[0]
        cnt = range1.size 
        if (cnt >= 1):
            d12 = gcirc(rax/15,dex,ra[range1]/15,de[range1],1) 
            cosmo = FlatLambdaCDM(H0 = self.h0c, Om0 = self.omegamc)
            sdcond = cosmo.arcsec_per_kpc_proper(vx/self.c)*self.dcondc*u.kpc/u.arcsec
            v12 = abs((vx-v[range1])/(1.+vx/self.c))
            grj = np.where((d12 > 0.)&(d12 <= sdcond)&(v12 <= self.vcondc))[0].astype(int)

            num = grj.size
            if (num == 0): pass
            if (num == 1):  
                lst[k+1] = range1[grj]
                flag[range1[grj]] = 1
                k += 1 
                
            if (num >= 2):
                lst[k+1:k+num+1] = range1[grj]
                flag[range1[grj]] = 1
                k+= num

            for j in range(0,num):
                alpha = range1[grj[j]]
                lst,flag,k =  self.solution(alpha,k,flag,lst,ra,de,v)
        return lst,flag,k 

@ray.remote
def mainloop(file,H0,omegamc,omegalc,omegakc,c,dcondc,vcondc,nmin):
    print("start")
    field = np.loadtxt(file)
    field = field[field[:,2].argsort()]
    ti = time.time()

    ##########################
    #                        #
    #                        #
    #    common paramters    #
    #                        #
    #                        #
    ##########################



    fname = ["N"] 
    fra = [-99.]
    fde = [-99.]
    fz = [-99]
    fnum = [-9.] 
    ra = field[:,0]
    dec = field[:,1]
    z = field[:,2]

    ID = field[:,3].astype("str")
    v=z*c


    ngal = len(ra)
    gname = np.ones(ngal)*(-1)    
    ngroup = 0 
    flag = np.zeros(ngal)
    for i in range(ngal):
        lst = np.array([-1 for _ in range(ngal)])
        if (flag[i] != 0): continue 
        k = 0 
        flag[i] = 1
        lst[k] = i 
        fof = fofradecV(H0,omegamc,omegalc,omegakc,c,dcondc,vcondc)
        lst,flag,k = fof.solution(i,k,flag,lst,ra,dec,v)
        if (k >= nmin-1):
            l0 = lst[0]
            ind = np.where(lst >= 0)[0].astype(int)
            cnt = ind.size
            str1 = ID[l0]

            str1 = str1.replace(" ","")
            gname[lst[ind]] = str1
            fname.append(str1) 

            toto1 = np.where(ra[lst[ind]] < 90)[0]
            ntoto1 = toto1.size

            toto2 = np.where(ra[lst[ind]] > 270)[0]
            ntoto2 = toto2.size 

            fra.append("{0:6f}".format(np.mean(ra[lst[ind]]) % 360))
            fde.append("{0:6f}".format(np.mean(dec[lst[ind]])))
            fz.append("{0:5f}".format(np.mean(z[lst[ind]])))
            fnum.append(cnt)
            ngroup += 1 
        tf = time.time()
    if ngroup >= 1:
        fname = fname[1:ngroup+1] 
        fra = fra[1:ngroup+1]
        fde = fde[1:ngroup+1]
        fz = fz[1:ngroup+1]
        fnum = fnum[1:ngroup+1]

    print(f'{(tf-ti)//60} mins {((tf-ti)%60)//1} second')                

    idx = np.where(gname != -1)[0]

    arr = np.array([ID,ra,dec,z,gname]).astype(float).T

    return arr


# In[ ]:


class nc_all_sky_divide():
    def __init__(self,file,div_ra,div_dec,H,omegamc,dcondc):
        self.ra = np.array(file.ra)
        self.dec = np.array(file.dec)
        self.z = np.array(file.redshift)
        self.h0c = H 
        self.omegamc = omegamc 
        self.dcondc = dcondc 
        self.div_ra = div_ra
        self.div_dec = div_dec
        self.min_z = min(file.redshift)
    def only_dec(self):
        dec = self.dec
        z = self.z
        div_dec = self.div_dec
        dec_index_parallel_field = []
        div_dec_param = abs(int(max(dec)+1)-int(min(dec)-1))/div_dec
        f_dec = int(min(dec)-1)
        for _ in range(div_dec):
            if f_dec != int(min(dec)-1):
                idx = np.where((dec>=f_dec) & (dec<f_dec+div_dec_param))[0].astype(int)
            else: 
                idx = np.where(dec<f_dec+div_dec_param)[0].astype(int)
            
            dec_index_parallel_field.append(idx)
            f_dec += div_dec_param
        return dec_index_parallel_field
    def common_field_dec(self): 
        dec = self.dec 
        z = self.z 
        min_z = self.min_z 
        div_dec = self.div_dec 
        div_dec_param = abs((int(max(dec)+1)-int(min(dec)-1)))/div_dec
        cosmo = FlatLambdaCDM(H0 = self.h0c, Om0 = self.omegamc)
        link_len = cosmo.arcsec_per_kpc_proper(min_z)/3600*self.dcondc*u.kpc/u.arcsec #[degree]
        print("linkling_angular is",link_len,"[degree]")
        dec_index_common_field = []
        f_dec = int(min(dec)-1)
        
        for _ in range(div_dec-1):
            idx = np.where((dec>=f_dec+div_dec_param-link_len)&(dec<=f_dec+div_dec_param+link_len))[0].astype(int)
            
            f_dec += div_dec_param 
            
            dec_index_common_field.append(idx)
        
        return dec_index_common_field
def red_process(file):
    blue_shift = np.where(np.array(file.redshift) <= 10**(-3))[0].astype(int)
    file.drop(blue_shift,axis=0, inplace=True)
    return file


# In[ ]:


def common_field_merging(common_field,field):
    
    #-----------------------#
    #                       #
    #    group merge cell   #
    #                       #
    #-----------------------# 
    field_copy = field.copy()
    common_field_copy = common_field.copy()

    inter,common_ind,field_ind = np.intersect1d(common_field[:,0],field[:,0],return_indices=True)

    com_g_field = field[field_ind]
    com_g = common_field[common_ind]
    c = 0 
 
    common_index_list = np.array([])
    for idx , val in enumerate(np.unique(com_g[:,4])):
        
        common_list = np.where(common_field[:,4] == val)[0].astype(int)
        common_index_list = np.append(common_index_list,common_list)
        for i in common_field[common_list][:,0]:
            gal_id = np.where(field[:,0] == i)[0].astype(int)
            ndx = gal_id.size
            if (ndx == 1) :
                group_id = field[:,4][gal_id]
                common_field_copy[common_list][:,4] = group_id
                break 
    common_index_list = common_index_list.astype(int)

    field_copy = np.append(field_copy,common_field_copy[common_index_list],axis=0)
    
    inter_unique,un_copy_ind,copy_ind = np.intersect1d(np.unique(field_copy[:,0]),field_copy[:,0],return_indices=True)
    
    return field_copy[copy_ind]

def Total_merging(field1,field2,common_field):
    arr1 =  common_field_merging(common_field,field1)
    arr2 =  common_field_merging(common_field,field2)
     
    concate_whole = np.concatenate((arr1,arr2))
    
    inter_unique,con_uni_ind,con_ind = np.intersect1d(np.unique(concate_whole[:,0]),concate_whole[:,0],return_indices=True) 
    
    arr3 = concate_whole[con_ind.astype(int)]
    setdiff = np.setdiff1d(common_field[:,0],arr3[:,0])
    ind_arr = np.array([])
   
    for i in setdiff:
        setdiff_idx = np.where(common_field[:,0] == i)[0].astype(int)
        ind_arr = np.append(ind_arr,setdiff_idx)
    
    arr3 = np.append(arr3,common_field[ind_arr.astype(int)],axis=0)
    return arr3


# In[ ]:


def sub_to_not_group(result):
    arr = []
    for i in range(len(result)):
        index = np.where(result[i][:,4] != -1)[0].astype(int)
        arr.append(result[i][index])
    return arr 

def finally_unique(result):
    inter_unique,con_uni_ind,con_ind = np.intersect1d(np.unique(result[:,0]),result[:,0],return_indices=True) 
    return result[con_ind]


# In[ ]:


def nmin_unique(fields):
    lst = np.array([])
    for idx,val in enumerate(np.unique(fields[:,4])):
        find = np.where(fields[:,4] == val)[0].astype(int)
        if find.size <= 4 :
            fields = np.delete(fields,find,axis=0)
    return fields 


# In[ ]:


def save_file(file,div_ra,div_dec,H,omegamc,dcondc,dir2):
    lst = nc_all_sky_divide(file,div_ra,div_dec,H,omegamc,dcondc).only_dec()
    lst1 = nc_all_sky_divide(file,div_ra,div_dec,H,omegamc,dcondc).common_field_dec()
    for i in range(len(lst)): 
        imfo = np.array([np.array(file.ra)[lst[i]],np.array(file.dec)[lst[i]],np.array(file.redshift)[lst[i]],np.array(file.ID)[lst[i]]]).T
        np.savetxt(dir2+"field_"+str(i),imfo)
    for i in range(len(lst1)):
        imfo1 = np.array([np.array(file.ra)[lst1[i]],np.array(file.dec)[lst1[i]],np.array(file.redshift)[lst1[i]],np.array(file.ID)[lst1[i]]]).T
        np.savetxt(dir2+"common_field_"+str(i),imfo1)

