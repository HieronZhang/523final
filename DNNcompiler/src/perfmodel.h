#ifndef __PERFMODEL_H__
#define __PERFMODEL_H__

#include "utility.h"

//Input: 
// t_00: Fully PF execution time from profiling (ms)
// t_10: (InputPF) Output Fully PF time from profiling (ms)
// t_11: no PF execution time from profiling (ms)
// r_input: the ratio of PF data in the input tensors (and not in-transfer)
// r_output: the ratio of PF data in the output tensors (and not in-transfer)
// r_input_ssd: the ratio of SSD PFs in the PFs (not in-transfer) in the input tensors
// r_output_ssd: the ratio of SSD PFs in the PFs (not in-transfer) in the output tensors
// s_input: total input tensor size (byte)
// s_output: total output tensor size (byte)
// BW_pcie: PCIe bandwidth (B/ms)
// BW_ssd: SSD bandwidth (B/ms)
// l_sys: System (CPU far-fault handling) latency (us)
// l_ssd: SSD latency (us)

//Output:
// delteT_PF: delta t for page fault handling (ms) 
// BW_ssd_rest: The rest of SSD bandwidth useable when handling PF (for prefetching) (B/ms). Can be 0!! 
// BW_pcie_rest: The rest of PCIe bandwidth usable when handling PF (for prefetching) （B/ms. Can be 0!!

void performance_model(double t_00, double t_10, double t_11, double r_input, double r_output, 
                       double r_input_ssd, double r_output_ssd, long s_input, long s_output, 
                       double BW_pcie, double BW_ssd, int l_sys, int l_ssd, 
                       double& deltaT_PF, double& BW_ssd_rest, double& BW_pcie_rest);

#endif
