# requirement before running the script
# python3 -m pip install matplotlib pandas openpyxl

import os, subprocess, itertools
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import pandas as pd
import numpy as np

if __name__ == "__main__":
  # predefined sequence of all experiment configurations
  # predef_experiment_config_seq_arr = ["lru", "random", "guided3", "guided5", "guided7",
  #     "prefetch_lru", "prefetch_random", "prefetch_guided3", "prefetch_guided5", "prefetch_guided7"]
  predef_experiment_config_seq_arr = ["lru", "random", "guided7",
      "prefetch_lru", "prefetch_random", "prefetch_guided7"]
  # predef_experiment_config_seq_arr = [
  #     "prefetch_guided7_delta0.1", "prefetch_guided7_delta0.2", "prefetch_guided7_delta0.3", "prefetch_guided7_delta0.4",
  #     "prefetch_guided7_delta0.5", "prefetch_guided7_delta0.6", "prefetch_guided7_delta0.7", "prefetch_guided7_delta0.8",
  #     "prefetch_guided7_delta0.9",
  #     "prefetch_lru_delta0.1", "prefetch_lru_delta0.2", "prefetch_lru_delta0.3", "prefetch_lru_delta0.4",
  #     "prefetch_lru_delta0.5", "prefetch_lru_delta0.6", "prefetch_lru_delta0.7", "prefetch_lru_delta0.8",
  #     "prefetch_lru_delta0.9",
  #     "prefetch_random_delta0.1", "prefetch_random_delta0.2", "prefetch_random_delta0.3", "prefetch_random_delta0.4",
  #     "prefetch_random_delta0.5", "prefetch_random_delta0.6", "prefetch_random_delta0.7", "prefetch_random_delta0.8",
  #     "prefetch_random_delta0.9"]
  # predef_experiment_config_seq_arr = [
  #     "prefetch_guided7_delta0.01", "prefetch_guided7_delta0.02", "prefetch_guided7_delta0.03", "prefetch_guided7_delta0.04",
  #     "prefetch_guided7_delta0.05", "prefetch_guided7_delta0.06", "prefetch_guided7_delta0.07", "prefetch_guided7_delta0.08",
  #     "prefetch_guided7_delta0.09", "prefetch_guided7_delta0.1",
  #     "prefetch_lru_delta0.01", "prefetch_lru_delta0.02", "prefetch_lru_delta0.03", "prefetch_lru_delta0.04",
  #     "prefetch_lru_delta0.05", "prefetch_lru_delta0.06", "prefetch_lru_delta0.07", "prefetch_lru_delta0.08",
  #     "prefetch_lru_delta0.09", "prefetch_lru_delta0.1",
  #     "prefetch_random_delta0.01", "prefetch_random_delta0.02", "prefetch_random_delta0.03", "prefetch_random_delta0.04",
  #     "prefetch_random_delta0.05", "prefetch_random_delta0.06", "prefetch_random_delta0.07", "prefetch_random_delta0.08",
  #     "prefetch_random_delta0.09",  "prefetch_random_delta0.1"]
  # predef_experiment_config_seq_arr = [
  #     "prefetch_guided7_delta0.01", "prefetch_guided7_delta0.02", "prefetch_guided7_delta0.03", "prefetch_guided7_delta0.04",
  #     "prefetch_guided7_delta0.05", "prefetch_guided7_delta0.06", "prefetch_guided7_delta0.07", "prefetch_guided7_delta0.08",
  #     "prefetch_guided7_delta0.09", 
  #     "prefetch_guided7_delta0.1", "prefetch_guided7_delta0.2", "prefetch_guided7_delta0.3", "prefetch_guided7_delta0.4",
  #     "prefetch_guided7_delta0.5", "prefetch_guided7_delta0.6", "prefetch_guided7_delta0.7", "prefetch_guided7_delta0.8",
  #     "prefetch_guided7_delta0.9",
  #     "prefetch_lru_delta0.01", "prefetch_lru_delta0.02", "prefetch_lru_delta0.03", "prefetch_lru_delta0.04",
  #     "prefetch_lru_delta0.05", "prefetch_lru_delta0.06", "prefetch_lru_delta0.07", "prefetch_lru_delta0.08",
  #     "prefetch_lru_delta0.09", 
  #     "prefetch_lru_delta0.1", "prefetch_lru_delta0.2", "prefetch_lru_delta0.3", "prefetch_lru_delta0.4",
  #     "prefetch_lru_delta0.5", "prefetch_lru_delta0.6", "prefetch_lru_delta0.7", "prefetch_lru_delta0.8",
  #     "prefetch_lru_delta0.9",
  #     "prefetch_random_delta0.01", "prefetch_random_delta0.02", "prefetch_random_delta0.03", "prefetch_random_delta0.04",
  #     "prefetch_random_delta0.05", "prefetch_random_delta0.06", "prefetch_random_delta0.07", "prefetch_random_delta0.08",
  #     "prefetch_random_delta0.09",
  #     "prefetch_random_delta0.1", "prefetch_random_delta0.2", "prefetch_random_delta0.3", "prefetch_random_delta0.4",
  #     "prefetch_random_delta0.5", "prefetch_random_delta0.6", "prefetch_random_delta0.7", "prefetch_random_delta0.8",
  #     "prefetch_random_delta0.9"]

  # predefined sequence of all model configurations
  predef_model_config_seq_arr = ["ResNet152.256", "WResNet101.256", "ResNeXt101_32.256",
      "Inceptionv3.1024", "SENet154.256"]
  # predef_model_config_seq_arr = ["ResNet152.256"]
  # predef_model_config_seq_arr = ["WResNet101.256"]
  # predef_model_config_seq_arr = ["ResNeXt101_32.256"]
  # predef_model_config_seq_arr = ["Inceptionv3.1024"]
  # predef_model_config_seq_arr = ["SENet154.256"]

  # predefined sequence of all the statistics to be gathered
  # kernel statistics
  predef_kernel_stat_seq_arr = ["cpu_pf", "ssd_pf", "unalloc_pf",
      "exe_time", "ideal_exe_time", "pf_exe_time", "slowdown", "speedup"]

  # eviction statistics
  predef_evc_stat_seq_arr = ["total_evc", "hot", "medium", "cold", "dead"]
  
  # figure drawing options
  horiz = False
  pf_num_normalize = True
  evc_num_normalize = True

  # plot font size options
  plt.rc('font', size=11)
  plt.rc('axes', titlesize=20)
  # plt.rc('xtick', labelsize=8)
  if horiz:
    plt.rc('ytick', labelsize=8)
  else:
    plt.rc('ytick', labelsize=12)
  plt.rc('legend', fontsize=20)

  fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(20, 30))
  # fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(20, 20))
  plt.subplots_adjust(left=0.1, right=0.9, bottom=1, top=5, wspace=5, hspace=5)

  # generate positional dict
  predef_experiment_config_seq = { item : i for i, item in enumerate(predef_experiment_config_seq_arr) }
  predef_model_config_seq = { item : i for i, item in enumerate(predef_model_config_seq_arr) }
  predef_kernel_stat_seq = { item : i for i, item in enumerate(predef_kernel_stat_seq_arr) }
  predef_evc_stat_seq = { item : i for i, item in enumerate(predef_evc_stat_seq_arr) }

  # get all the paths
  script_path = os.path.dirname(os.path.realpath(__file__))
  config_path = os.path.abspath(os.path.join(script_path, os.path.pardir, "configs"))
  result_path = os.path.abspath(os.path.join(script_path, os.path.pardir, "results"))
  output_path = os.path.abspath(os.path.join(script_path, "output"))
  if not os.path.exists(output_path):
    os.makedirs(output_path)

  # array to store the statistics
  kernel_stats = [[[0 for _ in predef_experiment_config_seq] for _ in predef_model_config_seq] for _ in predef_kernel_stat_seq]
  evc_stats = [[[0 for _ in predef_experiment_config_seq] for _ in predef_model_config_seq] for _ in predef_evc_stat_seq]

  # get all the stat files using system find
  final_stats, err = subprocess.Popen(
      ["find", result_path, "-name", "*.final", "-type", "f"],
      stdout=subprocess.PIPE).communicate()
  final_stats = final_stats.decode().strip().split("\n")
  for final_stat in final_stats:
    model = os.path.basename(os.path.dirname(os.path.dirname(final_stat)))
    config = os.path.basename(os.path.dirname(final_stat))
    config_split = config.split("-")
    assert len(config_split) == 2
    model_config = f"{model}.{config_split[0]}"
    experiment_config = config_split[1]
    if experiment_config not in predef_experiment_config_seq:
      continue
    line, err = subprocess.Popen(
        ["tail", "-1", final_stat],
        stdout=subprocess.PIPE).communicate()
    if (model_config not in predef_model_config_seq):
      continue
    if line.decode().strip() != "-1":
      print(model_config, experiment_config, "\033[0;31mInvalid\033[0m")
      continue
    print(model_config, experiment_config, "\033[0;32mValid\033[0m")
    with open(final_stat, "r") as f:
      for line in f.readlines():
        if line.find("iter1") != -1:
          line_split = line.split("=")
          if len(line_split) != 2:
            continue
          stat_name, stat_val = line_split
          stat_split = stat_name.strip().split(".")
          stat_val = stat_val.strip()
          assert len(stat_split) == 3
          stat_name = f"{stat_split[2].strip()}"
          if stat_name in predef_evc_stat_seq:
            evc_stats[predef_evc_stat_seq[stat_name]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]] = stat_val
          elif stat_name in predef_kernel_stat_seq:
            kernel_stats[predef_kernel_stat_seq[stat_name]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]] = stat_val

  # write csv file
  # kernel stat
  with open(f"{output_path}/kernel_stat.csv", "w") as f:
    for kernel_stat in predef_kernel_stat_seq:
        f.write(f",{kernel_stat}")
    f.write("\n")
    for model_config in predef_model_config_seq:
      for experiment_config in predef_experiment_config_seq:
        model_idx = predef_model_config_seq[model_config]
        exp_idx = predef_experiment_config_seq[experiment_config]
        f.write(f"{model_config}.{experiment_config}")
        for kernel_stat in predef_kernel_stat_seq:
          stat_idx = predef_kernel_stat_seq[kernel_stat]
          f.write(f",{kernel_stats[stat_idx][model_idx][exp_idx]}")
        f.write("\n")

  # eviction stat
  with open(f"{output_path}/evc_stat.csv", "w") as f:
    for evc_stat in predef_evc_stat_seq:
        f.write(f",{evc_stat}")
    f.write("\n")
    for model_config in predef_model_config_seq:
      for experiment_config in predef_experiment_config_seq:
        model_idx = predef_model_config_seq[model_config]
        exp_idx = predef_experiment_config_seq[experiment_config]
        f.write(f"{model_config}.{experiment_config}")
        for evc_stat in predef_evc_stat_seq:
          stat_idx = predef_evc_stat_seq[evc_stat]
          f.write(f",{evc_stats[stat_idx][model_idx][exp_idx]}")
        f.write("\n")

  # write xlsx file
  # kernel stat
  df = pd.read_csv(f"{output_path}/kernel_stat.csv")
  df.to_excel(f"{output_path}/kernel_stat.xlsx")

  # eviction stat
  df = pd.read_csv(f"{output_path}/evc_stat.csv")
  df.to_excel(f"{output_path}/evc_stat.xlsx")

  labels = predef_model_config_seq.keys()
  total_col = len(predef_experiment_config_seq)
  width = 0.1  # the width of the bars
  x = np.arange(len(labels)) * (width * (total_col + 1))  # the label locations
  xticks = np.array([xx + (col - total_col / 2) * width for xx, col in itertools.product(x, range(total_col))])
  xtick_labels = [i for i in predef_experiment_config_seq.keys()] * len(predef_model_config_seq)

  cpu_pf_num = np.array([[int(kernel_stats[predef_kernel_stat_seq["cpu_pf"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()])
  ssd_pf_num = np.array([[int(kernel_stats[predef_kernel_stat_seq["ssd_pf"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()])
  unalloc_pf_num = np.array([[int(kernel_stats[predef_kernel_stat_seq["unalloc_pf"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()])

  for col in range(total_col):
    if pf_num_normalize:
      plot_cpu_pf_arr = cpu_pf_num[:, col] / (cpu_pf_num[:, predef_experiment_config_seq["lru"]] + ssd_pf_num[:, predef_experiment_config_seq["lru"]] + unalloc_pf_num[:, predef_experiment_config_seq["lru"]])
      plot_ssd_pf_arr = ssd_pf_num[:, col] / (cpu_pf_num[:, predef_experiment_config_seq["lru"]] + ssd_pf_num[:, predef_experiment_config_seq["lru"]] + unalloc_pf_num[:, predef_experiment_config_seq["lru"]])
      plot_unalloc_pf_arr = unalloc_pf_num[:, col] / (cpu_pf_num[:, predef_experiment_config_seq["lru"]] + ssd_pf_num[:, predef_experiment_config_seq["lru"]] + unalloc_pf_num[:, predef_experiment_config_seq["lru"]])
    else:
      plot_cpu_pf_arr = cpu_pf_num[:, col]
      plot_ssd_pf_arr = ssd_pf_num[:, col]
      plot_unalloc_pf_arr = unalloc_pf_num[:, col]

    # if (col < 5):
    #   plot_cpu_pf_arr = np.zeros(plot_cpu_pf_arr.shape)
    #   plot_ssd_pf_arr = np.zeros(plot_ssd_pf_arr.shape)
    #   plot_unalloc_pf_arr = np.zeros(plot_unalloc_pf_arr.shape)

    # ax1.barh(x + (col - total_col / 2) * width, plot_cpu_pf_arr, width, label='CPU', color=(0.2, 0.9 - 0.1 * col, 0.1 + 0.1 * col, 0.9), edgecolor = "white")
    # ax1.barh(x + (col - total_col / 2) * width, plot_ssd_pf_arr, width, left=plot_cpu_pf_arr, label='SSD', color=(0.2, 0.9 - 0.1 * col, 0.1 + 0.1 * col, 0.7), edgecolor = "white")
    # ax1.barh(x + (col - total_col / 2) * width, plot_unalloc_pf_arr, width, left=plot_cpu_pf_arr+plot_ssd_pf_arr, label='Unalloc', color=(0.2, 0.9 - 0.1 * col, 0.1 + 0.1 * col, 0.5), edgecolor = "white")
    if horiz:
      ax1.barh(x + (col - total_col / 2) * width, plot_cpu_pf_arr, width, label='CPU', color="aliceblue", edgecolor = "dodgerblue", hatch="////")
      ax1.barh(x + (col - total_col / 2) * width, plot_ssd_pf_arr, width, left=plot_cpu_pf_arr, label='SSD', color="honeydew", edgecolor = "olivedrab", hatch="\\\\\\\\")
      ax1.barh(x + (col - total_col / 2) * width, plot_unalloc_pf_arr, width, left=plot_cpu_pf_arr+plot_ssd_pf_arr, label='Unalloc', color="lavenderblush", edgecolor = "mediumvioletred", hatch="...")
    else:
      ax1.bar(x + (col - total_col / 2) * width, plot_cpu_pf_arr, width, label='CPU', color="aliceblue", edgecolor = "dodgerblue", hatch="////")
      ax1.bar(x + (col - total_col / 2) * width, plot_ssd_pf_arr, width, bottom=plot_cpu_pf_arr, label='SSD', color="honeydew", edgecolor = "olivedrab", hatch="\\\\\\\\")
      ax1.bar(x + (col - total_col / 2) * width, plot_unalloc_pf_arr, width, bottom=plot_cpu_pf_arr+plot_ssd_pf_arr, label='Unalloc', color="lavenderblush", edgecolor = "mediumvioletred", hatch="...")

  # Add some text for labels, title and custom x-axis tick labels, etc.
  if horiz:
    ax1.set_ylabel('Policy')
    ax1.yaxis.set_label_coords(1.05, 0.5)
    if pf_num_normalize:
      ax1.set_xlabel("Normalized Number of Page Faults")
      ax1.plot([1, 1], ax1.get_ylim(), linestyle="--", color=(0, 0, 0, 1), linewidth=0.8)
      ax1.set_xlim([0, 1.5])
    else:
      ax1.set_xlabel("Number of Page Faults")
    for i in range(len(predef_model_config_seq)):
      x_coord = x[i]
      y_coord = ax1.get_xlim()[0] + (ax1.get_xlim()[1] - ax1.get_xlim()[0]) * -0.085
      ax1.annotate(predef_model_config_seq_arr[i], xy=(ax1.get_xlim()[0], x_coord), xytext=(y_coord, x_coord), rotation=90, va='center', ha='center')
    ax1.set_yticks(xticks)
    ax1.set_yticklabels(xtick_labels)
    ax1.set_ylim(ax1.get_ylim())
    ax1.invert_yaxis()
    ax1.legend(("CPU", "SSD", "Unalloc"), loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3)
  else:
    if pf_num_normalize:
      ax1.set_ylabel("Normalized Number of Page Faults")
      ax1.plot(ax1.get_xlim(), [1, 1], linestyle="--", color=(0, 0, 0, 1), linewidth=0.8)
      ax1.set_ylim([0, 1.5])
    else:
      ax1.set_ylabel("Number of Page Faults")
    for i in range(len(predef_model_config_seq)):
      x_coord = x[i]
      y_coord = ax1.get_ylim()[0] + (ax1.get_ylim()[1] - ax1.get_ylim()[0]) * -0.215
      ax1.annotate(predef_model_config_seq_arr[i], xy=(x_coord, ax1.get_ylim()[0]), xytext=(x_coord, y_coord), rotation=0, va='center', ha='center')
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xtick_labels, rotation=90)
    ax1.legend(("CPU", "SSD", "Unalloc"), loc='upper center', bbox_to_anchor=(0.3, 1.05), ncol=3)
  ax1.set_title("")
  ax1.spines["right"].set_visible(False)
  ax1.spines["top"].set_visible(False)


  freq = 3.2e9
  exe_times = np.array([[int(kernel_stats[predef_kernel_stat_seq["exe_time"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()]) / freq
  ideal_exe_times = np.array([[int(kernel_stats[predef_kernel_stat_seq["ideal_exe_time"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()]) / freq
  pf_exe_times = np.array([[int(kernel_stats[predef_kernel_stat_seq["pf_exe_time"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()]) / freq

  base = exe_times[0][0]
  for col in range(total_col):
    plot_exe_times_arr = exe_times[:, col]
    plot_ideal_exe_times_arr = ideal_exe_times[:, col]
    plot_pf_exe_times_arr = pf_exe_times[:, col]

    # plot_exe_times_arr = exe_times[:, col] / pf_exe_times[:, col]
    # plot_ideal_exe_times_arr = ideal_exe_times[:, col] / pf_exe_times[:, col]
    # plot_pf_exe_times_arr = pf_exe_times[:, col] / pf_exe_times[:, col]
    base = min([base, *plot_exe_times_arr, *plot_ideal_exe_times_arr, *plot_pf_exe_times_arr])

    if horiz:
      ax2.barh(x + (col - total_col / 2) * width, plot_exe_times_arr, width, label='CPU', color="aliceblue", edgecolor = "dodgerblue", hatch="////")
      ax2.errorbar(plot_exe_times_arr, x + (col - total_col / 2) * width, xerr=[plot_exe_times_arr - plot_ideal_exe_times_arr, plot_pf_exe_times_arr - plot_exe_times_arr], color="olivedrab", elinewidth=0.001, capsize=10, fmt=" ")
    else:
      ax2.bar(x + (col - total_col / 2) * width, plot_exe_times_arr, width, label='CPU', color="aliceblue", edgecolor = "dodgerblue", hatch="////")
      ax2.errorbar(x + (col - total_col / 2) * width, plot_exe_times_arr, yerr=[plot_exe_times_arr - plot_ideal_exe_times_arr, plot_pf_exe_times_arr - plot_exe_times_arr], color="olivedrab", elinewidth=0.001, capsize=25, fmt=" ")


  if horiz:
    ax2.set_xlim([base * 0.95, ax2.get_xlim()[1]])
    for i in range(len(predef_model_config_seq)):
      x_coord = x[i]
      y_coord = ax2.get_xlim()[0] + (ax2.get_xlim()[1] - ax2.get_xlim()[0]) * -0.085
      ax2.annotate(predef_model_config_seq_arr[i], xy=(ax2.get_xlim()[0], x_coord), xytext=(y_coord, x_coord), rotation=90, va='center', ha='center')
    ax2.set_ylabel("Policy")
    ax2.yaxis.set_label_coords(1.05, 0.5)
    ax2.set_xlabel("Execution time (s)")
    ax2.set_yticks(xticks)
    ax2.set_yticklabels(xtick_labels)
    ax2.invert_yaxis()
  else:
    ax2.set_ylabel("Execution time (s)")
    for i in range(len(predef_model_config_seq)):
      x_coord = x[i]
      y_coord = ax2.get_ylim()[0] + (ax2.get_ylim()[1] - ax2.get_ylim()[0]) * -0.215
      ax2.annotate(predef_model_config_seq_arr[i], xy=(x_coord, ax2.get_ylim()[0]), xytext=(x_coord, y_coord), rotation=0, va='center', ha='center')
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xtick_labels, rotation=90)
  ax2.set_title("")
  ax2.legend(("Exe time", "Execution time range (ideal to all PF)"), loc='upper center', bbox_to_anchor=(0.5, 1), ncol=3)
  ax2.spines["right"].set_visible(False)
  ax2.spines["top"].set_visible(False)


  dead_num = np.array([[int(evc_stats[predef_evc_stat_seq["dead"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()])
  hot_num = np.array([[int(evc_stats[predef_evc_stat_seq["hot"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()])
  medium_num = np.array([[int(evc_stats[predef_evc_stat_seq["medium"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()])
  cold_num = np.array([[int(evc_stats[predef_evc_stat_seq["cold"]][predef_model_config_seq[model_config]][predef_experiment_config_seq[experiment_config]]) for experiment_config in predef_experiment_config_seq] for model_config in predef_model_config_seq.keys()])

  total_evc_num = dead_num + hot_num + medium_num + cold_num
  for col in range(total_col):
    if evc_num_normalize:
      plot_dead_num_arr = dead_num[:, col] / total_evc_num[:, predef_experiment_config_seq["lru"]]
      plot_hot_num_arr = hot_num[:, col] / total_evc_num[:, predef_experiment_config_seq["lru"]]
      plot_medium_num_arr = medium_num[:, col] / total_evc_num[:, predef_experiment_config_seq["lru"]]
      plot_cold_num_arr = cold_num[:, col] / total_evc_num[:, predef_experiment_config_seq["lru"]]
    else:
      plot_dead_num_arr = dead_num[:, col]
      plot_hot_num_arr = hot_num[:, col]
      plot_medium_num_arr = medium_num[:, col]
      plot_cold_num_arr = cold_num[:, col]

    if horiz:
      ax3.barh(x + (col - total_col / 2) * width, plot_dead_num_arr, width, label='CPU', color="oldlace", edgecolor = "darkorange", hatch="////")
      ax3.barh(x + (col - total_col / 2) * width, plot_hot_num_arr, width, left=plot_dead_num_arr, label='CPU', color="aliceblue", edgecolor = "dodgerblue", hatch="\\\\\\\\")
      ax3.barh(x + (col - total_col / 2) * width, plot_medium_num_arr, width, left=plot_dead_num_arr+plot_hot_num_arr, label='CPU', color="honeydew", edgecolor = "olivedrab", hatch="....")
      ax3.barh(x + (col - total_col / 2) * width, plot_cold_num_arr, width, left=plot_dead_num_arr+plot_hot_num_arr+plot_medium_num_arr, label='CPU', color="lavenderblush", edgecolor = "mediumvioletred", hatch="++")
    else:
      ax3.bar(x + (col - total_col / 2) * width, plot_dead_num_arr, width, label='CPU', color="oldlace", edgecolor = "darkorange", hatch="////")
      ax3.bar(x + (col - total_col / 2) * width, plot_hot_num_arr, width, bottom=plot_dead_num_arr, label='CPU', color="aliceblue", edgecolor = "dodgerblue", hatch="\\\\\\\\")
      ax3.bar(x + (col - total_col / 2) * width, plot_medium_num_arr, width, bottom=plot_dead_num_arr+plot_hot_num_arr, label='CPU', color="honeydew", edgecolor = "olivedrab", hatch="....")
      ax3.bar(x + (col - total_col / 2) * width, plot_cold_num_arr, width, bottom=plot_dead_num_arr+plot_hot_num_arr+plot_medium_num_arr, label='CPU', color="lavenderblush", edgecolor = "mediumvioletred", hatch="++")
      

  if horiz:
    if pf_num_normalize:
      ax3.plot([1, 1], ax3.get_ylim(), linestyle="--", color=(0, 0, 0, 1), linewidth=0.8)
      ax3.set_xlabel("Normalized Eviction Number")
      ax3.set_xlim([0, 1.5])
    else:
      ax3.set_xlabel("Eviction Number")
    for i in range(len(predef_model_config_seq)):
      x_coord = x[i]
      y_coord = ax3.get_xlim()[0] + (ax3.get_xlim()[1] - ax3.get_xlim()[0]) * -0.085
      ax3.annotate(predef_model_config_seq_arr[i], xy=(ax3.get_xlim()[0], x_coord), xytext=(y_coord, x_coord), rotation=90, va='center', ha='center')
    ax3.set_ylabel("Policy")
    ax3.yaxis.set_label_coords(1.05, 0.5)
    ax3.set_yticks(xticks)
    ax3.set_yticklabels(xtick_labels)
    ax3.invert_yaxis()
    ax3.legend(("Dead", "Hot", "Medium", "Cold"), loc='upper center', bbox_to_anchor=(0.7, 1), ncol=4)
  else:
    if pf_num_normalize:
      ax3.set_ylabel("Normalized Eviction Number")
      ax3.plot(ax3.get_xlim(), [1, 1], linestyle="--", color=(0, 0, 0, 1), linewidth=0.8)
      ax3.set_ylim([0, 1.5])
    else:
      ax3.set_ylabel("Eviction Number")
    for i in range(len(predef_model_config_seq)):
      x_coord = x[i]
      y_coord = ax3.get_ylim()[0] + (ax3.get_ylim()[1] - ax3.get_ylim()[0]) * -0.215
      ax3.annotate(predef_model_config_seq_arr[i], xy=(x_coord, ax3.get_ylim()[0]), xytext=(x_coord, y_coord), rotation=0, va='center', ha='center')
    ax3.set_xticks(xticks)
    ax3.set_xticklabels(xtick_labels, rotation=90)
    ax3.legend(("Dead", "Hot", "Medium", "Cold"), loc='upper center', bbox_to_anchor=(0.3, 1), ncol=4)
  ax3.set_title("")
  ax3.spines["right"].set_visible(False)
  ax3.spines["top"].set_visible(False)

  fig.tight_layout()

  # plt.show()
  plt.savefig(f"{output_path}/out.png")

  extent = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(1.1, 1.1)
  extent.y0 -= (extent.y1 - extent.y0) * 0.2
  fig.savefig(f"{output_path}/out_ax1.png", bbox_inches=extent)

  extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(1.1, 1.1)
  extent.y0 -= (extent.y1 - extent.y0) * 0.2
  fig.savefig(f"{output_path}/out_ax2.png", bbox_inches=extent)

  extent = ax3.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(1.1, 1.1)
  extent.y0 -= (extent.y1 - extent.y0) * 0.2
  fig.savefig(f"{output_path}/out_ax3.png", bbox_inches=extent)

