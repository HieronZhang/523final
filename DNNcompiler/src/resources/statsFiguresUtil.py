INCEPTION, RESNET, SENET, BERT, VIT, RESNEXT = range(6)

# define all dimensions script need to gather, and their corresponding sording rules
post_processed_stats = [
  "ideal_exe_time", 
  "exe_time", 
  "pf_num", 
  "evc_num",
  "ssd2gpu_traffic",
  "gpu2ssd_traffic",
  "cpu2gpu_traffic",
  "gpu2cpu_traffic",
  "stall_percentage",
  "overlap_percentage",
  "compute_percentage"
]

all_dimensions = { 
  "model":      lambda x : ["resnet152", "resnext101_32", "senet154", "inceptionv3", "bert_base", "vit"].index(x.lower()), 
  "batch_size": lambda x : float(x), 
  "setting":    lambda x : ["lru", "flashneuron", "deepum", "prefetch_lru"].index(x.lower()), 
  "cpu_mem":    lambda x : float(x), 
  "ssd_bw":     lambda x : float(x), 
  "pcie_bw":    lambda x : float(x),
  "stat":       lambda x : post_processed_stats.index(x.lower())
}

setting_translation = {
  "lru"          : "Base UVM",
  "FlashNeuron"  : "FlashNeuron",
  "deepUM"       : "DeepUM+",
  "prefetch_lru" : "G10",
  "ideal"        : "Ideal"
}

x_label_translation = {
  "256"  : "B = 256\nM = 100%",
  "512"  : "B = 512\nM = 100%",
  "768"  : "B = 768\nM = 100%",
  "1024" : "B = 1024\nM = 100%",
  "1280" : "B = 1280\nM = 100%",
  "1536" : "B = 1536\nM = 100%"
}

# keep this EXACTLY THE SAME ORDER as specified above
net_name_translation = {
  "inception"  : "Inceptionv3",
  "resnet"     : "ResNet152",
  "senet"      : "SENet154",
  "bert"       : "BERT_Base",
  "vit"        : "VIT",
  "resnext"    : "ResNeXt101_32",
}