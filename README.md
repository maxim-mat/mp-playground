multiprocessing playground

## `x**2` for n = 10e7 (10000000)
- Single process single thread (sync):  2.5519540309906006
- Multi process single thread:  14.020305871963501
- Single process single thread (async):  2.5800271034240723
- Single process multi thread:  **2.1620001792907715**

## `x**3` for n = 10e7 
- Single process single thread (sync):  2.8120005130767822
- Multi process single thread:  14.818955421447754
- Single process single thread (async):  3.053964138031006
- Single process multi thread:  **2.1350317001342773**

## `math.sin(x**2 + 5)` for n = 10e7 
- Single process single thread (sync):  4.2489588260650635
- Multi process single thread:  **2.891026735305786**
- Single process single thread (async):  4.280002593994141
- Single process multi thread:  3.7430050373077393