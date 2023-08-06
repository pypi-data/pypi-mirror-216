import numpy as np
from scipy import stats


def stats_parameters(x):

    #          ( Central Parameters )                                 ( پارامترهای مرکزی )
    Mean = np.mean(x)                           #  Mean                                             میانگین
    Median = np.median(x)                       #  Median or Socond Quartile                          میانه
    Mode = stats.mode(x)                        #  Mode                                                مد
    Q1 = np.percentile(a=x,q=25)                #  First  Quartile                                چارک اول
    Q2= np.percentile(a=x,q=50)                 #  Second Quartile or Median          چارک دوم یا همان میانه
    Q3 = np.percentile(a=x,q=75)                #  Third  Quartile                               چارک سوم
    #        ( Dispersion Parameters )                                ( پارامترهای پراکندگی )               
    Range = np.ptp(x)                           #  Range                                              دامنه
    AD_mean = np.mean(np.abs(x - np.mean(x)))   #  Average Deviation of Mean          انحراف متوسط از میانگین
    AD_median = np.mean(np.abs(x - np.mean(x))) #  Average Deviation of Median          انحراف متوسط از میانه
    AD_mode = np.mean(np.abs(x - np.mean(x)))   #  Average Deviation of Mode              انحراف متوسط از مد
    var = np.var(x)                             #  Population Variance                         واریانس جامعه
    std = np.std(x)                             #  Population Standard Deviation           انحراف معیار جامعه
    CV = std/Mean                               #  population Coefficient of Variation   ضریب پراکندگی جامعه
    S_var = np.var(x)                           #  Sample Variance                              واریانس نمونه
    S_std = np.std(x)                           #  Sample Standard Deviation                انحراف معیار نمونه
    S_CV = std/Mean                             #  Sample Coefficient of Variation        ضریب پراکندگی نمونه
    IQR = Q3-Q1                                 #  Interquartile Range                      دامنه میان چارکی
    SIQR = IQR/2                                #  Semi-Interquartile or Quartile Dispersion   انحراف چارکی

    print(f'''
                ( Central Parameters ) 
                
       * Mean   :  {Mean}                              
       * Median :  {Median}                             
       * Mode   :  {Mode}   
       
       * Q1 : {Q1}
       * Q2 : {Q2}
       * Q3 : {Q3} 
       
    --------------------------------------------------------
                ( Dispersion Parameters )
                
       * Range     : {Range}   
       
       * AD_mean   : {AD_mean}                          
       * AD_median : {AD_median}                        
       * AD_mode   : {AD_mode}     
       
       * var       : {var}
       * std       : {std}
       * CV        : {CV}
       
       * S_var     : {S_var}
       * S_std     : {S_std}
       * S_CV      : {S_CV}
       
       * IQR       : {IQR}
       * SIQR      : {SIQR}
       
        
    ''')

    return {'Mean':Mean,'Median':Median,'Mode':Mode,'Q1':Q1,'Q2':Q2,'Q3':Q3,
            'Range':Range,'AD_mean':AD_mean,'AD_median':AD_median,'AD_mode':AD_mode,
            'var':var,'std':std,'CV':CV,'S_var':S_var,'S_std':S_std,'S_CV':S_CV,
            'IQR':IQR,'SIQR':SIQR}





