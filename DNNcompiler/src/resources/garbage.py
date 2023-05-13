import os, subprocess

if __name__ == "__main__":
  stat_to_gather = { "exe_time" : 0, "cpu_pf" : 0, "ssd_pf" : 0, "unalloc_pf" : 0, "total_evc" : 0 }
  all_stats = {}

  script_path = os.path.dirname(os.path.realpath(__file__))
  config_path = os.path.abspath(os.path.join(script_path, os.path.pardir, "configs"))
  result_path = os.path.abspath(os.path.join(script_path, os.path.pardir, "results"))
  output_path = os.path.abspath(os.path.join(script_path, "output"))
  if not os.path.exists(output_path):
    os.makedirs(output_path)

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
    line, err = subprocess.Popen(
        ["tail", "-1", final_stat],
        stdout=subprocess.PIPE).communicate()
    if line.decode().strip() != "-1" and experiment_config.lower().find("flash") == -1:
      continue
    # print(model_config, experiment_config)

    for key in stat_to_gather.keys():
      stat_to_gather[key] = 0
    with open(final_stat, "r") as f:
      for line in f.readlines():
        if line.find("total_exe_time") != -1:
          line_split = line.split("=")
          if len(line_split) != 2:
            continue
          stat_to_gather['exe_time'] = float(line_split[1]) / 1000 * 1200 * 10 ** 6
        elif line.find("iter1") != -1:
          line_split = line.split("=")
          if len(line_split) != 2:
            continue
          stat_name, stat_val = line_split
          stat_split = stat_name.strip().split(".")
          stat_val = stat_val.strip()
          assert len(stat_split) == 3
          stat_name = f"{stat_split[2].strip()}"
          if stat_name in stat_to_gather:
            stat_to_gather[stat_name] = int(stat_val)
    iter0_line, err = subprocess.Popen(
        ["grep", "0\] run ends @ ", f"{os.path.dirname(final_stat)}/run.log"],
        stdout=subprocess.PIPE).communicate()
    iter1_line, err = subprocess.Popen(
        ["grep", "1\] run ends @ ", f"{os.path.dirname(final_stat)}/run.log"],
        stdout=subprocess.PIPE).communicate()
    result0 = iter0_line.decode().split("@")
    result1 = iter1_line.decode().split("@")
    if len(result0) != 2 or len(result1) != 2:
      continue
    # print(model_config, experiment_config, int(result1[1].strip()), int(result0[1].strip()), int(result1[1].strip()) - int(result0[1].strip()))
    stat_to_gather['exe_time'] = int(result1[1].strip()) - int(result0[1].strip())
    all_stats[f"{model_config}.{experiment_config}"] = stat_to_gather.copy()
  result = dict(sorted(all_stats.items()))
  for config, stat_to_gather in result.items():
    print(config)
    print(f"  Execution time:       {stat_to_gather['exe_time']}")
    print(f"  Total page fault num: {stat_to_gather['cpu_pf'] + stat_to_gather['ssd_pf'] + stat_to_gather['unalloc_pf']}")
    print(f"  Total eviction num:   {stat_to_gather['total_evc']}")
    print()

