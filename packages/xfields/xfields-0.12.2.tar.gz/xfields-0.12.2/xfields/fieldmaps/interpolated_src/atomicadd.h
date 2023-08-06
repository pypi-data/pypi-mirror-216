// copyright ################################# //
// This file is part of the Xfields Package.   //
// Copyright (c) CERN, 2021.                   //
// ########################################### //

#ifndef _ATOMICADD_H_
#define _ATOMICADD_H_

inline void atomicAdd(double *addr, double val)
{
   #pragma omp atomic //only_for_context cpu_openmp	
   *addr = *addr + val;
}

#endif
