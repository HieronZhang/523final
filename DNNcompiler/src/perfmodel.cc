#include "perfmodel.h"
#include <stdlib.h>
#include <math.h>
#include <algorithm>
#include <iostream>

using std::max;

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
// BW_ssd_rest: The rest of SSD bandwidth useable when handling PF (for prefetching) (B/ms)
// BW_pcie_rest: The rest of PCIe bandwidth usable when handling PF (for prefetching) （B/ms）

void performance_model(double t_00, double t_10, double t_11, double r_input, double r_output, 
                       double r_input_ssd, double r_output_ssd, long s_input, long s_output, 
                       double BW_pcie, double BW_ssd, int l_sys, int l_ssd, 
                       double& deltaT_PF, double& BW_ssd_rest, double& BW_pcie_rest) {
    
    Assert(r_input >= 0 && r_input <= 1);
    Assert(r_output >=0 && r_output <= 1);
    Assert(r_input_ssd >= 0 && r_input_ssd <= 1);
    Assert(r_output_ssd >= 0 && r_output_ssd <= 1);

    double BW_cpu_in;
    double BW_cpu_out;

    if (t_00 <= t_11)
    {
        t_00 = t_11;
    }
    if (t_10 < t_11)
    {
        t_10 = t_11;
    }
    if (t_10 > t_00)
    {
        t_10 = t_00;
    }

    if (t_00 == t_10)
    {
        BW_cpu_in = 1063004400;
    }
    else
    {
        BW_cpu_in = s_input / (t_00 - t_10);
    }
    if (t_10 == t_11)
    {
        BW_cpu_out = 1063004400;
    }
    else
    {
        BW_cpu_out = s_output / (t_10 - t_11);
    }

    double BW_ssd_in = BW_cpu_in * l_sys / (l_sys + l_ssd);
    double BW_ssd_out = BW_cpu_out * l_sys / (l_sys + l_ssd);

    if (BW_ssd_in > BW_ssd)
    {
        BW_ssd_in = BW_ssd;
    }
    if (BW_ssd_out > BW_ssd)
    {
        BW_ssd_out = BW_ssd;
    }
    if (r_input_ssd == 0)
    {
        BW_ssd_in = 0;
    }
    if (r_output_ssd == 0)
    {
        BW_ssd_out = 0;
    }
    
    

    if (BW_cpu_in > BW_pcie - max(BW_ssd_in, BW_ssd_out))
    {
        BW_cpu_in = BW_pcie - max(BW_ssd_in, BW_ssd_out);
    }

    if (BW_cpu_out > BW_pcie - max(BW_ssd_in, BW_ssd_out))
    {
        BW_cpu_out = BW_pcie - max(BW_ssd_in, BW_ssd_out);
    }

    double ssd_input_pf_time;
    double ssd_output_pf_time;
    
    if (r_input_ssd==0)
    {
        ssd_input_pf_time = 0;
    }
    else
    {
        ssd_input_pf_time = r_input*r_input_ssd*s_input/BW_ssd_in;
    }

    if(r_output_ssd==0)
    {
        ssd_output_pf_time = 0;
    }
    else
    {
        ssd_output_pf_time = r_output*r_output_ssd*s_output/BW_ssd_out;
    }
    double cpu_pf_time = r_input*(1-r_input_ssd)*s_input/BW_cpu_in + r_output*(1-r_output_ssd)*s_output/BW_cpu_out;
    

    deltaT_PF = max(ssd_input_pf_time + ssd_output_pf_time, cpu_pf_time);

    BW_ssd_rest = (r_input_ssd*r_input==0 && r_output_ssd*r_output==0) ? BW_ssd : BW_ssd - max(BW_ssd_in, BW_ssd_out);
    BW_pcie_rest = (cpu_pf_time==0) ? BW_pcie : BW_pcie - max(BW_cpu_in, BW_cpu_out);

}

