#include <math.h>
#include <stdio.h>
#include<time.h>

#define Pi 3.1415926535897932384626433832795
#define TWOPI	6.28318530717958648     /*:  �Ƕ�ת���� */
#define DPAI	6.28318530717958648     /*:  �Ƕ�ת���� */
#define AE          6378.137   		 /*: ��׼�������뾶(����)WGS84��׼  */
#define E2   	    0.0066943800699785	 /*: ����ƫ����ƽ��                 */

int SunAziElv(int Year,int Month,int Day,int Hour,int Minute,int Second,double facis,double landas,double *Azi,double *Elv,double TimeOffset);
void EARTH(double TIME,double *ALPHA,double *ALPDOT,double *CHISUN, double *OBLIQE);
double ZSODSRadto2Pai(double dRad);
double TIMEZ(int nry,int NMON,int NDAY,int NHR,int NMIN, float SEC);
void ICGS(double RX[],double Sth, double Cth, double *Azgs,double *Elgs,double facis);


extern "C" int GetSunAziElvCPP(int Year,int Month,int Day,int Hour,int Minute,int Second,double* Facis,double* Landas,double *Azi,double *Elv,int Width,int Height,float FullScanTime)
{
  long int Length = Width * Height;
  double Azi_temp[1] = {0};
  double Elv_temp[1] = {0};
  double facis = 0;
  double landas = 0;
  double TimeOffset = 0;
  int WhichLine = 0;
  //int Year_Loc,Month_Loc,Day_Loc,Hour_Loc,Minute_Loc,Second_Loc;
  printf("____________________\n");
  for(int i =0;i<Length;i++)
  {
    facis = Facis[i];
    landas = Landas[i];

    //add time for different lines
    WhichLine = int(i/Width);
    TimeOffset = (float(WhichLine)/Height)*FullScanTime;
    //printf("WhichLine %d\n",WhichLine);
    //printf("TimeOffset %f\n",TimeOffset);

    if(facis >= -90 && facis <= 90 && landas >= -180 && landas <= 180)
    {
        SunAziElv(Year,Month,Day,Hour,Minute,Second,facis,landas, Azi_temp,Elv_temp,TimeOffset);
    }
    else
    {
        Azi_temp[0] = 0.0;
        Elv_temp[0] = 0.0;
    }
    Azi[i] = Azi_temp[0];
    Elv[i] = Elv_temp[0];
  }
}

int SunAziElv(int Year,int Month,int Day,int Hour,int Minute,int Second,double facis,double landas,double *Azi,double *Elv,double TimeOffset)
{
	int year,month,day,hour,min;
	float second;
	double SCNLON,sTH,cTH,SCNLAT,SOLAZ,SOLELV;
	double RSOL,COSX,SINX,COSE,SINE,TH;
	double RX[3];
	double StTime;
	double PHIG,DPHIDT,CHISUN,EPSLON;
	double Azgs=0,Elgs=0;
	//sscanf(strTime,"%4d-%2d-%2dT%2d:%2d:%f",&year,&month,&day,&hour,&min,&second);
	year=Year;
	month=Month;
	day=Day;
	hour=Hour;
	min=Minute;
	second=Second;
	StTime=TIMEZ(year,month,day,hour,min,second);
	/////////////////////////////////////
	StTime = StTime + TimeOffset;
	//printf("%f  \n",TimeOffset);
	//printf("%f  \n",StTime);


	SCNLAT=facis*Pi/180.0;
	SCNLON=landas*Pi/180.0;
	EARTH(StTime,&PHIG,&DPHIDT,&CHISUN,&EPSLON);
	 RSOL=149600881.0;
   COSX=cos(CHISUN);
   SINX=sin(CHISUN);
   COSE=cos(EPSLON);
   SINE=sin(EPSLON);
   ///����̫��λ��ʸ��RX(3)
	  RX[0]=RSOL*COSX;
	  RX[1]=RSOL*(SINX*COSE);
	  RX[2]=RSOL*(SINX*SINE);
      TH =fmod(SCNLON+PHIG,TWOPI);
	  cTH=cos(TH);
	  sTH=sin(TH);
    //printf("%lf,%lf,%lf",RX[0],RX[1],RX[2]);
    ICGS(RX,sTH,cTH,&Azgs,&Elgs,SCNLAT);
    *Azi=Azgs;
    *Elv=(Pi/2.0)-Elgs;
    return 0;
}
/*:**************  ICGS �����ײ�����  ******************
*	�������ƣ�ICGS
*	�������⣺��������˲ʱ�����Թ۲���λ��(��λ�Ǻ�����)����
*	�������ã���������˲ʱ�����Թ۲���λ��(��λ�Ǻ�����)
*	���÷�����void ICGS(double RX[],double Sth, double Cth, double *Azgs,double *Elgs)
*	���ò�����
					double RX[]				���ǿռ�λ��ʸ����x,y,z)
					double Sth				�۲��SIN(S) S:�۲��ĵط�����ʱ
					double Cth				�۲��COS(S) S:�۲��ĵط�����ʱ
					double *Azgs			TIMEʱ�̵�������Թ۲�վ�ķ�λ��
					double *Elgs 			TIMEʱ�̵�������Թ۲�վ������
*	����ֵ��  ��
**************  ICGS ��������α���˵��  ************:*/

void ICGS(double RX[],double Sth, double Cth, double *Azgs,double *Elgs,double facis)
{

		  double  Sla, Cla;
	double Gxic, Gyic, Gzic, Rhx, Rhy, Rhz;
	double Rht, Rxgs, Rygs, Rzgs;
    double HGT,RE2;
    HGT=50.0/6378137.0;
	Sla = sin(facis);
	Cla = cos(facis);
    RE2=AE/sqrt(1.0-E2*Sla*Sla) ;
     Gxic=(RE2+HGT)*Cla*Cth ;
    Gyic=(RE2+HGT)*Cla*Sth ; 
    Gzic=(RE2*(1.0-E2)+HGT)*Sla; 
	Rhx = RX[0]-Gxic;
	Rhy = RX[1]-Gyic;
	Rhz = RX[2]-Gzic;
    Rht=Cth*Rhx+Sth*Rhy;
      Rxgs=Cth*Rhy-Sth*Rhx;
      Rygs=Cla*Rhz-Sla*Rht;    
      Rzgs=Cla*Rht+Sla*Rhz;

	*Azgs = atan2(Rxgs,Rygs);
	if ( *Azgs < 0.0 )
		*Azgs = *Azgs+TWOPI;
	*Elgs = atan(Rzgs/sqrt(Rxgs*Rxgs+Rygs*Rygs));

//	*Rgs = sqrt(Rhx*Rhx+Rhy*Rhy+Rhz*Rhz);

	return;
}

void EARTH(double TIME,double *ALPHA,double *ALPDOT,double *CHISUN, double *OBLIQE) 
{
	///@code
    double PHIGRN[3],CHIMS[3],MEARTH[3],OMEGA[3],EPSLON[2], 		 
             DELPSI[2], DELEPS[2];  
    double KAPPA,MANOM0,ZERO80,CENTCT,DDATE,DATE, EPTIME,CENTNO ; 
    double ALPHA0,DADT,CHIMO,DXMDT,OMEGA0,DMDT,DWDT, EPSLN0, 
	     DEDT,DELP0,DDPDT,DELE0,DDEDT,CHI0,DXDT,ANUT0,DANDT,Dtime;
	int IDATE2;
    PHIGRN[0]=1.739935890;
	PHIGRN[1]=628.33195070; 
	PHIGRN[2]=.000006754947810;
    CHIMS[0]=4.881633570,
	CHIMS[1]=	  628.3319487050, 
	CHIMS[2]=	  1.4468088e-10;

    MEARTH[0]=6.256581470; 
	MEARTH[1]= 628.3019468590; 
	MEARTH[2]= -7.1676766e-11;
    OMEGA[0]= 4.523636080;
	OMEGA[1]= -33.7571619360;
	OMEGA[2]= 9.9285594E-10; 
    EPSLON[0]= .40936890950;
	EPSLON[1]= - 2.27232172336e-4; 
    KAPPA = .0335020;         
    DELPSI[0]=8.35465e-5; 
	DELPSI[1]=.61712e-5;
    DELEPS[0]=4.46513e-5; 
	DELEPS[1]=.26771e-5;     
    ZERO80=29219.50;
	CENTCT=36525.0;
// *** I) IF THIS THE FIRSTCALL TO EARTH THEN 
//! ***   A) THE JULIAN DAY NUMBER NEAREST THE INPUT TIME IS DETERMINE
//!      IF(FIRST.eq. 1.0) then 
    DDATE=ZERO80+TIME/86400.0 ;
    IDATE2=2.*DDATE ;  
    if((IDATE2%2) == 0) IDATE2=IDATE2-1 ;
    DATE=IDATE2*.50 ;
    if (DDATE-DATE > .50) DATE=DATE+1.0  ;
    EPTIME=(DATE-ZERO80)*86400.0  ;
    CENTNO=DATE/CENTCT  ;   
// ***    B) THE HOUR ANGLE (ALPHA), NUTATION (ANUT),LONGITUDE OF THE
//! ***       SUN (CHI) AND OBLIQUITY OF THE ECLIPTIC (EPSLN) AND THEI
//***       DERIVATIVES AT THE EPOCH TID5 ARE DETERMINED. 

    ALPHA0=ZSODSRadto2Pai(PHIGRN[0]+   										  
             ZSODSRadto2Pai(CENTNO*(PHIGRN[1]+CENTNO*PHIGRN[2])));
    DADT =   (TWOPI+(PHIGRN[1]+2.*CENTNO*PHIGRN[2])/CENTCT)/86400.  ;
    CHIMO  = ZSODSRadto2Pai(CHIMS[0] +   									  
               ZSODSRadto2Pai(CENTNO*(CHIMS[1]+CENTNO*CHIMS[2]))) ;
    DXMDT  = (CHIMS[1]+2.*CENTNO*CHIMS[2])/(86400.0*CENTCT)  ;
      MANOM0=ZSODSRadto2Pai(MEARTH[0] +  										  
             ZSODSRadto2Pai(CENTNO*(MEARTH[1]+CENTNO*MEARTH[2]))) ;
    DMDT= (MEARTH[1]+2.*CENTNO*MEARTH[2])/(86400.0*CENTCT); 
    OMEGA0 = ZSODSRadto2Pai(OMEGA[0] +   									  
               ZSODSRadto2Pai(CENTNO*(OMEGA[1]+CENTNO*OMEGA[2])))  ;
    DWDT   = (OMEGA[1]+2.*CENTNO*OMEGA[2])/(86400.0*CENTCT)  ;
    EPSLN0 = EPSLON[0] + CENTNO*EPSLON[1]  ;
    DEDT   = EPSLON[1]/(86400.0*CENTCT) ;
    DELP0=DELPSI[0]*sin(OMEGA0)+DELPSI[1]*sin(2.0*CHIMO)  ;
    DDPDT = DELPSI[0]*cos(OMEGA0)*DWDT+DELPSI[1]*cos(2.*CHIMO)    
              *2.0*DXMDT ;
    DELE0  = DELEPS[0]*cos(OMEGA0) + DELEPS[1]*cos(2.0*CHIMO);
    DDEDT  =-DELEPS[0]*sin(OMEGA0)*DWDT -  						 
              DELEPS[1]*sin(2.0*CHIMO)*2.0*DXMDT    ;
    CHI0  = CHIMO + KAPPA*sin(MANOM0)              ;
    DXDT  = DXMDT + KAPPA*cos(MANOM0)*DMDT         ;
    ANUT0 = DELP0*cos(EPSLN0+DELE0)    ;
    DANDT=DDPDT*ANUT0/DELP0-DELP0*sin(EPSLN0+DELE0)*(DEDT+DDEDT)  ;
    Dtime= TIME-EPTIME  ;
    *ALPHA = ZSODSRadto2Pai(ALPHA0+ANUT0+(DADT+DANDT)*Dtime)  ;
    *ALPDOT = DADT+DANDT   ;
    *CHISUN = ZSODSRadto2Pai(CHI0+DXDT*Dtime) ;
    *OBLIQE = EPSLN0 +DELE0+(DEDT+DDEDT)*Dtime ;
    return;
    
    ///@endcode
}

double ZSODSRadto2Pai(double dRad)
{
	double dresult;
	
	dresult = dRad - DPAI*((int)(dRad/DPAI));
	if ( dRad<0.0 )
		dresult +=DPAI;

	return dresult;
}
double TIMEZ(int nry,int NMON,int NDAY,int NHR,int NMIN, float SEC)   
{
	///@code
    int iyr0, iyr, MDAYS;
	int MON[12]={31,59,90,120,151,181,212,243,273,304,334,365};
	double TIMEZT;
    if(nry >= 2000 || nry <= 90) 
    {
        iyr0=nry%100;
        iyr=100+iyr0;
        
	}
	else iyr=nry%100;

    if(iyr>=80) MDAYS=365*(iyr-80)+(iyr-77)/4  ;
    if(iyr<80) MDAYS=365*(iyr-80)+(iyr-80)/4  ;

    if(NMON!=1) MDAYS=MDAYS+MON[NMON-2];   
    if(NMON >2 && ((iyr%4)==0 )) MDAYS=MDAYS+1;
//	printf("    MDAYS2=%d %d %d %d\n" ,MDAYS,NDAY,NHR,NMIN);
    
    TIMEZT=86400.0*(double)(MDAYS+NDAY-1)+3600.0*(double)NHR+60*(double)NMIN+SEC ; 
//	printf("t=%f\n",TIMEZT);
    return TIMEZT;
    ///@endcode
} 