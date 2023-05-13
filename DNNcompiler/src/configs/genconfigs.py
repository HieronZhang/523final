#         modelname       : (netname,             config foldername,  output foldername,[batch sizes]) 
models = {"Inceptionv3"   : ("Inceptionv3",       "Inceptionv3",      "Inceptionv3",    [512, 768, 1024, 1152, 1280, 1408, 1536, 1664, 1792]), 
          "ResNet152"     : ("ResNet152",         "ResNet152",        "ResNet152",      [256, 512, 768, 1024, 1280, 1536, 1792, 2048]),
          # "ResNeXt101_32" : ("ResNeXt101_32x8d",  "ResNeXt101_32x8d", "ResNeXt101_32",  [256, 512, 768, 1024]),
          "SENet154"      : ("SENet154",          "SENet154",         "SENet154",       [256, 512, 768, 1024, 1280, 1536]),
          "VIT"           : ("VIT",               "VIT",               "VIT",           [256, 512, 768, 1024, 1280, 1536, 1792, 2048]),
          "BERT"          : ("BERT_Base",         "BERT",             "BERT_Base",      [128, 256, 384, 512, 640, 768, 1024, 1280, 1536]),
          # "NeRF"          : ("NeRF",              "NeRF",             "NeRF",           [16])
          }
policies = ["lru", "prefetch_lru", "deepUM", "FlashNeuron"]  # "prefetch_tolerant"
cpu_policies = ["lru", "prefetch_lru", "deepUM"]
ssd_policies = ["lru", "prefetch_lru", "deepUM", "FlashNeuron"]
cpu_sizes = ["0", "16", "32", "64", "256"]
pcie_bws = ["32", "64", "128"]
ssd_bws = ["6.4", "12.8", "19.2", "24", "25.6", "27", "32", "48", "64"]
kernel_time_variations = ["0.05", "0.10", "0.15", "0.20", "0.25"]
kernel_speedup_variations = ["1.5", "2.0", "2.5", "3.0", "3.5", "4.0"]
kernel_speedup_policies = ["lru", "prefetch_lru", "deepUM", "FlashNeuron"]

import os
current_folder = os.path.dirname(os.path.realpath(__file__))
folder_basename = os.path.basename(current_folder)
if folder_basename != "configs":
  print(f"invalid current folder, <{current_folder}> is not <configs>")
  exit(1)

config_output_folders = set()

def get_str(model: str, netname: str, config_foldername: str, output_foldername: str, policy: str, batch_size: str, cpu_size: str, pcie_bw : str, ssd_bw : str, kernel_time_variation: str="0", kernel_speedup_variation: str="1"):
  characteristics_str = ""
  if cpu_size != "128":
    characteristics_str += f"-cpu{cpu_size.replace('.', '_')}"
  if ssd_bw != "3.2":
    characteristics_str += f"-ssd{ssd_bw.replace('.', '_')}"
  elif pcie_bw != "15.754":
    characteristics_str += f"-pcie{pcie_bw.replace('.', '_')}"
  if kernel_time_variation != "0":
    characteristics_str += f"-var{kernel_time_variation.replace('.', '_')}"
  if kernel_speedup_variation != "1":
    characteristics_str += f"-spd{kernel_speedup_variation.replace('.', '_')}"
  config_output_folder = f"results/{output_foldername}/{batch_size}-{policy}{characteristics_str}"
  assert config_output_folder not in config_output_folders
  config_output_folders.add(config_output_folder)
  return [f"""output_folder           {config_output_folder}
is_simulation           1

{"is_transformer          1" if model == "BERT" or model == "VIT" or model == "NeRF" else ""}
{"trans_borden            210" if model == "BERT" else "trans_borden            184" if model == "VIT" else "trans_borden            7" if model == "NeRF" else ""}
{"is_inception            1" if model == "Inceptionv3" else  "is_resnet               1" if model == "ResNet152" or model == "ResNeXt101_32" or model == "WResNet101" else "is_senet                1"}
batch_size              {batch_size}
input_H                 {299 if model == "Inceptionv3" else 224}
input_W                 {299 if model == "Inceptionv3" else 224}
num_iteration           2
num_threads             128

nn_model_input_file     ../frontend/Nets/{netname}.txt
orig_kernel_time_file   ./results/{output_foldername}/cudnn{batch_size}.txt
pf_kernel_time_file     ./results/{output_foldername}/cudnn{batch_size}PF.txt
input_pf_kernel_time_file ./results/{output_foldername}/cudnn{batch_size}InputPF.txt
workspace_size_file       ./results/{output_foldername}/cudnn{batch_size}Workspace.txt
stat_output_file        sim_result
is_UVM                  1
use_prefetch            {"1" if policy.startswith("prefetch") or policy.startswith("deepUM") or policy.startswith("FlashNeuron") else "0"}
eviction_policy         {policy.split("_")[-1].upper() if policy.split("_")[-1].upper()!="FLASHNEURON" else "LRU"}
{"migration_policy        DEEPUM" if policy.startswith("deepUM") else ""}
{"migration_policy        FLASHNEURON" if policy.startswith("FlashNeuron") else ""}
{"prefetch_degree         8" if policy.startswith("deepUM") else ""}
system_latency_us       45

CPU_PCIe_bandwidth_GBps {pcie_bw}
CPU_memory_line_GB      {cpu_size}

GPU_memory_size_GB      40
GPU_frequency_GHz       1.2
GPU_PCIe_bandwidth_GBps {pcie_bw}
GPU_malloc_uspB         0.000000814
GPU_free_uspB           0

SSD_PCIe_bandwidth_GBps {ssd_bw}
SSD_read_latency_us     12
SSD_write_latency_us    16
SSD_latency_us          20

PCIe_latency_us         5
PCIe_batch_size_page    50

delta_parameter         0.5
{f"kernel_time_std_dev     {kernel_time_variation}" if kernel_time_variation != "0" else ""}
{f"kernel_speedup          {kernel_speedup_variation}" if kernel_speedup_variation != "1" else ""}
""", f"{current_folder}/{config_foldername}/{batch_size}-sim_{policy}{characteristics_str}.config"]

def main_performance():
  for model, configs in models.items():
    netname = configs[0]
    config_foldername = configs[1]
    output_foldername = configs[2]
    batch_sizes = configs[3]
    try:
      os.mkdir(f"{current_folder}/{config_foldername}")
    except OSError as error:
      pass
    for policy in policies:
      for batch_size in batch_sizes:
        content, filename = get_str(model, netname, config_foldername, output_foldername, policy, batch_size, "128", "15.754", "3.2")
        with open(filename, "w") as f:
          f.write(content)

def cpu_varying():
  for model, configs in models.items():
    netname = configs[0]
    config_foldername = configs[1]
    output_foldername = configs[2]
    batch_sizes = configs[3]
    try:
      os.mkdir(f"{current_folder}/{config_foldername}")
    except OSError as error:
      pass
    for policy in cpu_policies:
      for batch_size in batch_sizes:
        if model.find("ResNet") != -1:  
          temp_cpu_sizes = [*cpu_sizes, "192"]
        elif model.find("SENet") != -1:  
          temp_cpu_sizes = [*cpu_sizes, "96"]
        else:
          temp_cpu_sizes = cpu_sizes
        for cpu_size in temp_cpu_sizes:
          content, filename = get_str(model, netname, config_foldername, output_foldername, policy, batch_size, cpu_size, "15.754", "3.2")
          with open(filename, "w") as f:
            f.write(content)

def pcie_varying():
  for model, configs in models.items():
    netname = configs[0]
    config_foldername = configs[1]
    output_foldername = configs[2]
    batch_sizes = configs[3]
    try:
      os.mkdir(f"{current_folder}/{config_foldername}")
    except OSError as error:
      pass
    for policy in cpu_policies:
      for batch_size in batch_sizes:
          for pcie_bw in pcie_bws:
            content, filename = get_str(model, netname, config_foldername, output_foldername, policy, batch_size, "128", pcie_bw, "3.2")
            with open(filename, "w") as f:
              f.write(content)

def ssd_varying():
  for model, configs in models.items():
    netname = configs[0]
    config_foldername = configs[1]
    output_foldername = configs[2]
    batch_sizes = configs[3]
    try:
      os.mkdir(f"{current_folder}/{config_foldername}")
    except OSError as error:
      pass
    for policy in ssd_policies:
      for batch_size in batch_sizes:
          for ssd_bw in [*ssd_bws, "12.4", "13.2"] if model == "Inceptionv3" and policy == "prefetch_lru" and batch_size == 1536 else ssd_bws:
            pcie_bw = "32" if float(ssd_bw) < 32 else ssd_bw
            content, filename = get_str(model, netname, config_foldername, output_foldername, policy, batch_size, "128", pcie_bw, ssd_bw)
            with open(filename, "w") as f:
              f.write(content)
              
def kernel_time_varying():
  for model, configs in models.items():
    netname = configs[0]
    config_foldername = configs[1]
    output_foldername = configs[2]
    batch_sizes = configs[3]
    try:
      os.mkdir(f"{current_folder}/{config_foldername}")
    except OSError as error:
      pass
    for batch_size in batch_sizes:
      for kernel_time_variation in kernel_time_variations:
        content, filename = get_str(model, netname, config_foldername, output_foldername, "prefetch_lru", batch_size, "128", "15.754", "3.2", kernel_time_variation=kernel_time_variation)
        with open(filename, "w") as f:
          f.write(content)
              
def kernel_speedup_varying():
  for model, configs in models.items():
    netname = configs[0]
    config_foldername = configs[1]
    output_foldername = configs[2]
    batch_sizes = configs[3]
    try:
      os.mkdir(f"{current_folder}/{config_foldername}")
    except OSError as error:
      pass
    for policy in kernel_speedup_policies:
      for batch_size in batch_sizes:
        for kernel_speedup_variation in kernel_speedup_variations:
          content, filename = get_str(model, netname, config_foldername, output_foldername, policy, batch_size, "128", "32", "6.4", kernel_speedup_variation=kernel_speedup_variation)
          with open(filename, "w") as f:
            f.write(content)

if __name__ == "__main__":
  ssd_varying()
  # pcie_varying()
  cpu_varying()
  kernel_time_varying()
  kernel_speedup_varying()
  main_performance()
