from struct import *
f = open("D:\\temp_10.24.189.195\\FY4A-_LMI---_N_REGX_1047E_L2-_HRIT_NIR-_GLL_20171201005710_20171201005810_010KM_00000_GRB.DAT","rb")
# hh,hhh= unpack(">2sH",f.read(4))
# print hh,hhh

a,b,c,d,e,ff,g,i = unpack(">sH9s7s2sHH2s",f.read(27))
print str(a),b,c,d,e,ff,g,i

l,m,n= unpack(">2sH125s",f.read(129))
print str(l),m,n

o,p,q,r,s,t,u= unpack(">sHsHis17s",f.read(28))
print o,p,q,r,s,t,u

v,w,x= unpack(">2sH65532s",f.read(65536))
print v,w,x