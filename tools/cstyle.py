#!/usr/bin/env python3
# cstyle.py — 将 C 代码批量整理为 Linux 内核编码风格
#
# 用法:
#   cstyle.py FILE...
#
# 脚本自动识别文件类型，无需任何选项：
#   - 寄存器定义头文件（#define 占代码行多数，如 drv_gmac_def.h）：
#     合并单行简单宏，跳过 clang-format（保留手工对齐与紧凑表格）
#   - 普通代码文件：执行完整管线（pre 文本规则 + clang-format + post 规则）
#
# clang-format 使用内嵌的内核官方配置（源自 ~/.clang-format，已集成）。
# 脚本幂等：对同一文件重复执行结果不变。

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CLANG_FORMAT_STYLE = r"""# SPDX-License-Identifier: GPL-2.0
#
# clang-format configuration file. Intended for clang-format >= 11.
#
# For more information, see:
#
#   Documentation/dev-tools/clang-format.rst
#   https://clang.llvm.org/docs/ClangFormat.html
#   https://clang.llvm.org/docs/ClangFormatStyleOptions.html
#
---
AccessModifierOffset: -4
AlignAfterOpenBracket: Align
AlignConsecutiveAssignments: false
AlignConsecutiveDeclarations: false
AlignEscapedNewlines: Left
AlignOperands: true
AlignTrailingComments: false
AllowAllParametersOfDeclarationOnNextLine: false
AllowShortBlocksOnASingleLine: false
AllowShortCaseLabelsOnASingleLine: false
AllowShortFunctionsOnASingleLine: None
AllowShortIfStatementsOnASingleLine: false
AllowShortLoopsOnASingleLine: false
AlwaysBreakAfterDefinitionReturnType: None
AlwaysBreakAfterReturnType: None
AlwaysBreakBeforeMultilineStrings: false
AlwaysBreakTemplateDeclarations: false
BinPackArguments: true
BinPackParameters: true
BraceWrapping:
  AfterClass: false
  AfterControlStatement: false
  AfterEnum: false
  AfterFunction: true
  AfterNamespace: true
  AfterObjCDeclaration: false
  AfterStruct: false
  AfterUnion: false
  AfterExternBlock: false
  BeforeCatch: false
  BeforeElse: false
  IndentBraces: false
  SplitEmptyFunction: true
  SplitEmptyRecord: true
  SplitEmptyNamespace: true
BreakBeforeBinaryOperators: None
BreakBeforeBraces: Custom
BreakBeforeInheritanceComma: false
BreakBeforeTernaryOperators: false
BreakConstructorInitializersBeforeComma: false
BreakConstructorInitializers: BeforeComma
BreakAfterJavaFieldAnnotations: false
BreakStringLiterals: false
ColumnLimit: 120
CommentPragmas: '^ IWYU pragma:'
CompactNamespaces: false
ConstructorInitializerAllOnOneLineOrOnePerLine: false
ConstructorInitializerIndentWidth: 8
ContinuationIndentWidth: 8
Cpp11BracedListStyle: true
DerivePointerAlignment: false
DisableFormat: false
ExperimentalAutoDetectBinPacking: false
FixNamespaceComments: false

# Taken from:
#   git grep -h '^#define [^[:space:]]*for_each[^[:space:]]*(' include/ tools/ \
#   | sed "s,^#define \([^[:space:]]*for_each[^[:space:]]*\)(.*$,  - '\1'," \
#   | LC_ALL=C sort -u
ForEachMacros:
  - '__ata_qc_for_each'
  - '__bio_for_each_bvec'
  - '__bio_for_each_segment'
  - '__evlist__for_each_entry'
  - '__evlist__for_each_entry_continue'
  - '__evlist__for_each_entry_from'
  - '__evlist__for_each_entry_reverse'
  - '__evlist__for_each_entry_safe'
  - '__for_each_mem_range'
  - '__for_each_mem_range_rev'
  - '__for_each_thread'
  - '__hlist_for_each_rcu'
  - '__map__for_each_symbol_by_name'
  - '__pci_bus_for_each_res0'
  - '__pci_bus_for_each_res1'
  - '__pci_dev_for_each_res0'
  - '__pci_dev_for_each_res1'
  - '__perf_evlist__for_each_entry'
  - '__perf_evlist__for_each_entry_reverse'
  - '__perf_evlist__for_each_entry_safe'
  - '__rq_for_each_bio'
  - '__shost_for_each_device'
  - '__sym_for_each'
  - '_for_each_counter'
  - 'apei_estatus_for_each_section'
  - 'ata_for_each_dev'
  - 'ata_for_each_link'
  - 'ata_qc_for_each'
  - 'ata_qc_for_each_raw'
  - 'ata_qc_for_each_with_internal'
  - 'ax25_for_each'
  - 'ax25_uid_for_each'
  - 'bio_for_each_bvec'
  - 'bio_for_each_bvec_all'
  - 'bio_for_each_folio_all'
  - 'bio_for_each_integrity_vec'
  - 'bio_for_each_segment'
  - 'bio_for_each_segment_all'
  - 'bio_list_for_each'
  - 'bip_for_each_vec'
  - 'bond_for_each_slave'
  - 'bond_for_each_slave_rcu'
  - 'bpf_for_each'
  - 'bpf_for_each_reg_in_vstate'
  - 'bpf_for_each_reg_in_vstate_mask'
  - 'bpf_for_each_spilled_reg'
  - 'bpf_object__for_each_map'
  - 'bpf_object__for_each_program'
  - 'btree_for_each_safe128'
  - 'btree_for_each_safe32'
  - 'btree_for_each_safe64'
  - 'btree_for_each_safel'
  - 'card_for_each_dev'
  - 'cgroup_taskset_for_each'
  - 'cgroup_taskset_for_each_leader'
  - 'cpu_aggr_map__for_each_idx'
  - 'cpufreq_for_each_efficient_entry_idx'
  - 'cpufreq_for_each_entry'
  - 'cpufreq_for_each_entry_idx'
  - 'cpufreq_for_each_valid_entry'
  - 'cpufreq_for_each_valid_entry_idx'
  - 'css_for_each_child'
  - 'css_for_each_descendant_post'
  - 'css_for_each_descendant_pre'
  - 'damon_for_each_region'
  - 'damon_for_each_region_from'
  - 'damon_for_each_region_safe'
  - 'damon_for_each_scheme'
  - 'damon_for_each_scheme_safe'
  - 'damon_for_each_target'
  - 'damon_for_each_target_safe'
  - 'damos_for_each_filter'
  - 'damos_for_each_filter_safe'
  - 'damos_for_each_ops_filter'
  - 'damos_for_each_ops_filter_safe'
  - 'damos_for_each_quota_goal'
  - 'damos_for_each_quota_goal_safe'
  - 'data__for_each_file'
  - 'data__for_each_file_new'
  - 'data__for_each_file_start'
  - 'def_for_each_cpu'
  - 'device_for_each_child_node'
  - 'device_for_each_child_node_scoped'
  - 'dma_fence_array_for_each'
  - 'dma_fence_chain_for_each'
  - 'dma_fence_unwrap_for_each'
  - 'dma_resv_for_each_fence'
  - 'dma_resv_for_each_fence_unlocked'
  - 'do_for_each_ftrace_op'
  - 'drm_atomic_crtc_for_each_plane'
  - 'drm_atomic_crtc_state_for_each_plane'
  - 'drm_atomic_crtc_state_for_each_plane_state'
  - 'drm_atomic_for_each_plane_damage'
  - 'drm_client_for_each_connector_iter'
  - 'drm_client_for_each_modeset'
  - 'drm_connector_for_each_possible_encoder'
  - 'drm_exec_for_each_locked_object'
  - 'drm_exec_for_each_locked_object_reverse'
  - 'drm_for_each_bridge_in_chain'
  - 'drm_for_each_connector_iter'
  - 'drm_for_each_crtc'
  - 'drm_for_each_crtc_reverse'
  - 'drm_for_each_encoder'
  - 'drm_for_each_encoder_mask'
  - 'drm_for_each_fb'
  - 'drm_for_each_legacy_plane'
  - 'drm_for_each_plane'
  - 'drm_for_each_plane_mask'
  - 'drm_for_each_privobj'
  - 'drm_gem_for_each_gpuvm_bo'
  - 'drm_gem_for_each_gpuvm_bo_safe'
  - 'drm_gpusvm_for_each_range'
  - 'drm_gpuva_for_each_op'
  - 'drm_gpuva_for_each_op_from_reverse'
  - 'drm_gpuva_for_each_op_reverse'
  - 'drm_gpuva_for_each_op_safe'
  - 'drm_gpuvm_bo_for_each_va'
  - 'drm_gpuvm_bo_for_each_va_safe'
  - 'drm_gpuvm_for_each_va'
  - 'drm_gpuvm_for_each_va_range'
  - 'drm_gpuvm_for_each_va_range_safe'
  - 'drm_gpuvm_for_each_va_safe'
  - 'drm_mm_for_each_hole'
  - 'drm_mm_for_each_node'
  - 'drm_mm_for_each_node_in_range'
  - 'drm_mm_for_each_node_safe'
  - 'dsa_switch_for_each_available_port'
  - 'dsa_switch_for_each_cpu_port'
  - 'dsa_switch_for_each_cpu_port_continue_reverse'
  - 'dsa_switch_for_each_port'
  - 'dsa_switch_for_each_port_continue_reverse'
  - 'dsa_switch_for_each_port_safe'
  - 'dsa_switch_for_each_user_port'
  - 'dsa_switch_for_each_user_port_continue_reverse'
  - 'dsa_tree_for_each_cpu_port'
  - 'dsa_tree_for_each_user_port'
  - 'dsa_tree_for_each_user_port_continue_reverse'
  - 'dso__for_each_symbol'
  - 'elf_hash_for_each_possible'
  - 'elf_symtab__for_each_symbol'
  - 'evlist__for_each_cpu'
  - 'evlist__for_each_entry'
  - 'evlist__for_each_entry_continue'
  - 'evlist__for_each_entry_from'
  - 'evlist__for_each_entry_reverse'
  - 'evlist__for_each_entry_safe'
  - 'flow_action_for_each'
  - 'for_each_acpi_consumer_dev'
  - 'for_each_acpi_dev_match'
  - 'for_each_active_dev_scope'
  - 'for_each_active_drhd_unit'
  - 'for_each_active_iommu'
  - 'for_each_active_irq'
  - 'for_each_active_route'
  - 'for_each_aggr_pgid'
  - 'for_each_alloc_capable_rdt_resource'
  - 'for_each_and_bit'
  - 'for_each_andnot_bit'
  - 'for_each_available_child_of_node'
  - 'for_each_available_child_of_node_scoped'
  - 'for_each_bench'
  - 'for_each_bio'
  - 'for_each_board_func_rsrc'
  - 'for_each_btf_ext_rec'
  - 'for_each_btf_ext_sec'
  - 'for_each_bvec'
  - 'for_each_capable_rdt_resource'
  - 'for_each_card_auxs'
  - 'for_each_card_auxs_safe'
  - 'for_each_card_components'
  - 'for_each_card_dapms'
  - 'for_each_card_pre_auxs'
  - 'for_each_card_prelinks'
  - 'for_each_card_rtds'
  - 'for_each_card_rtds_safe'
  - 'for_each_card_widgets'
  - 'for_each_card_widgets_safe'
  - 'for_each_cgroup_storage_type'
  - 'for_each_child_of_node'
  - 'for_each_child_of_node_scoped'
  - 'for_each_child_of_node_with_prefix'
  - 'for_each_clear_bit'
  - 'for_each_clear_bit_from'
  - 'for_each_clear_bitrange'
  - 'for_each_clear_bitrange_from'
  - 'for_each_cmd'
  - 'for_each_cmsghdr'
  - 'for_each_collection'
  - 'for_each_comp_order'
  - 'for_each_compatible_node'
  - 'for_each_component_dais'
  - 'for_each_component_dais_safe'
  - 'for_each_conduit'
  - 'for_each_console'
  - 'for_each_console_srcu'
  - 'for_each_cpu'
  - 'for_each_cpu_and'
  - 'for_each_cpu_andnot'
  - 'for_each_cpu_from'
  - 'for_each_cpu_or'
  - 'for_each_cpu_wrap'
  - 'for_each_dapm_widgets'
  - 'for_each_dedup_cand'
  - 'for_each_dev_addr'
  - 'for_each_dev_scope'
  - 'for_each_dma_cap_mask'
  - 'for_each_dpcm_be'
  - 'for_each_dpcm_be_rollback'
  - 'for_each_dpcm_be_safe'
  - 'for_each_dpcm_fe'
  - 'for_each_drhd_unit'
  - 'for_each_dss_dev'
  - 'for_each_efi_memory_desc'
  - 'for_each_efi_memory_desc_in_map'
  - 'for_each_element'
  - 'for_each_element_extid'
  - 'for_each_element_id'
  - 'for_each_enabled_cpu'
  - 'for_each_endpoint_of_node'
  - 'for_each_event'
  - 'for_each_event_tps'
  - 'for_each_evictable_lru'
  - 'for_each_fib6_node_rt_rcu'
  - 'for_each_fib6_walker_rt'
  - 'for_each_file_lock'
  - 'for_each_free_mem_range'
  - 'for_each_free_mem_range_reverse'
  - 'for_each_func_rsrc'
  - 'for_each_gpiochip_node'
  - 'for_each_group_evsel'
  - 'for_each_group_evsel_head'
  - 'for_each_group_member'
  - 'for_each_group_member_head'
  - 'for_each_hstate'
  - 'for_each_hwgpio'
  - 'for_each_hwgpio_in_range'
  - 'for_each_if'
  - 'for_each_inject_fn'
  - 'for_each_insn'
  - 'for_each_insn_op_loc'
  - 'for_each_insn_prefix'
  - 'for_each_intid'
  - 'for_each_iommu'
  - 'for_each_ip_tunnel_rcu'
  - 'for_each_irq_desc'
  - 'for_each_irq_nr'
  - 'for_each_lang'
  - 'for_each_link_ch_maps'
  - 'for_each_link_codecs'
  - 'for_each_link_cpus'
  - 'for_each_link_platforms'
  - 'for_each_lru'
  - 'for_each_matching_node'
  - 'for_each_matching_node_and_match'
  - 'for_each_media_entity_data_link'
  - 'for_each_mem_pfn_range'
  - 'for_each_mem_range'
  - 'for_each_mem_range_rev'
  - 'for_each_mem_region'
  - 'for_each_member'
  - 'for_each_memory'
  - 'for_each_migratetype_order'
  - 'for_each_missing_reg'
  - 'for_each_mle_subelement'
  - 'for_each_mod_mem_type'
  - 'for_each_mon_capable_rdt_resource'
  - 'for_each_mp_bvec'
  - 'for_each_net'
  - 'for_each_net_continue_reverse'
  - 'for_each_net_rcu'
  - 'for_each_netdev'
  - 'for_each_netdev_continue'
  - 'for_each_netdev_continue_rcu'
  - 'for_each_netdev_continue_reverse'
  - 'for_each_netdev_dump'
  - 'for_each_netdev_feature'
  - 'for_each_netdev_in_bond_rcu'
  - 'for_each_netdev_rcu'
  - 'for_each_netdev_reverse'
  - 'for_each_netdev_safe'
  - 'for_each_new_connector_in_state'
  - 'for_each_new_crtc_in_state'
  - 'for_each_new_mst_mgr_in_state'
  - 'for_each_new_plane_in_state'
  - 'for_each_new_plane_in_state_reverse'
  - 'for_each_new_private_obj_in_state'
  - 'for_each_new_reg'
  - 'for_each_nhlt_endpoint'
  - 'for_each_nhlt_endpoint_fmtcfg'
  - 'for_each_nhlt_fmtcfg'
  - 'for_each_node'
  - 'for_each_node_by_name'
  - 'for_each_node_by_type'
  - 'for_each_node_mask'
  - 'for_each_node_numadist'
  - 'for_each_node_state'
  - 'for_each_node_with_cpus'
  - 'for_each_node_with_property'
  - 'for_each_nonreserved_multicast_dest_pgid'
  - 'for_each_numa_hop_mask'
  - 'for_each_of_allnodes'
  - 'for_each_of_allnodes_from'
  - 'for_each_of_cpu_node'
  - 'for_each_of_graph_port'
  - 'for_each_of_graph_port_endpoint'
  - 'for_each_of_pci_range'
  - 'for_each_old_connector_in_state'
  - 'for_each_old_crtc_in_state'
  - 'for_each_old_mst_mgr_in_state'
  - 'for_each_old_plane_in_state'
  - 'for_each_old_private_obj_in_state'
  - 'for_each_oldnew_connector_in_state'
  - 'for_each_oldnew_crtc_in_state'
  - 'for_each_oldnew_mst_mgr_in_state'
  - 'for_each_oldnew_plane_in_state'
  - 'for_each_oldnew_plane_in_state_reverse'
  - 'for_each_oldnew_private_obj_in_state'
  - 'for_each_online_cpu'
  - 'for_each_online_cpu_wrap'
  - 'for_each_online_node'
  - 'for_each_online_pgdat'
  - 'for_each_or_bit'
  - 'for_each_page_ext'
  - 'for_each_path'
  - 'for_each_pci_bridge'
  - 'for_each_pci_dev'
  - 'for_each_pcm_streams'
  - 'for_each_physmem_range'
  - 'for_each_populated_zone'
  - 'for_each_possible_cpu'
  - 'for_each_possible_cpu_wrap'
  - 'for_each_present_blessed_reg'
  - 'for_each_present_cpu'
  - 'for_each_present_section_nr'
  - 'for_each_prime_number'
  - 'for_each_prime_number_from'
  - 'for_each_probe_cache_entry'
  - 'for_each_process'
  - 'for_each_process_thread'
  - 'for_each_prop_codec_conf'
  - 'for_each_prop_dai_codec'
  - 'for_each_prop_dai_cpu'
  - 'for_each_prop_dlc_codecs'
  - 'for_each_prop_dlc_cpus'
  - 'for_each_prop_dlc_platforms'
  - 'for_each_property_of_node'
  - 'for_each_rdt_resource'
  - 'for_each_reg'
  - 'for_each_reg_filtered'
  - 'for_each_reloc'
  - 'for_each_reloc_from'
  - 'for_each_requested_gpio'
  - 'for_each_requested_gpio_in_range'
  - 'for_each_reserved_child_of_node'
  - 'for_each_reserved_mem_range'
  - 'for_each_reserved_mem_region'
  - 'for_each_rtd_ch_maps'
  - 'for_each_rtd_codec_dais'
  - 'for_each_rtd_components'
  - 'for_each_rtd_cpu_dais'
  - 'for_each_rtd_dais'
  - 'for_each_rtd_dais_reverse'
  - 'for_each_sband_iftype_data'
  - 'for_each_script'
  - 'for_each_sec'
  - 'for_each_set_bit'
  - 'for_each_set_bit_from'
  - 'for_each_set_bit_wrap'
  - 'for_each_set_bitrange'
  - 'for_each_set_bitrange_from'
  - 'for_each_set_clump8'
  - 'for_each_sg'
  - 'for_each_sg_dma_page'
  - 'for_each_sg_page'
  - 'for_each_sgtable_dma_page'
  - 'for_each_sgtable_dma_sg'
  - 'for_each_sgtable_page'
  - 'for_each_sgtable_sg'
  - 'for_each_sibling_event'
  - 'for_each_sta_active_link'
  - 'for_each_subelement'
  - 'for_each_subelement_extid'
  - 'for_each_subelement_id'
  - 'for_each_sublist'
  - 'for_each_subsystem'
  - 'for_each_suite'
  - 'for_each_supported_activate_fn'
  - 'for_each_supported_inject_fn'
  - 'for_each_sym'
  - 'for_each_thread'
  - 'for_each_token'
  - 'for_each_unicast_dest_pgid'
  - 'for_each_valid_link'
  - 'for_each_vif_active_link'
  - 'for_each_vma'
  - 'for_each_vma_range'
  - 'for_each_vsi'
  - 'for_each_wakeup_source'
  - 'for_each_zone'
  - 'for_each_zone_zonelist'
  - 'for_each_zone_zonelist_nodemask'
  - 'func_for_each_insn'
  - 'fwnode_for_each_available_child_node'
  - 'fwnode_for_each_child_node'
  - 'fwnode_for_each_parent_node'
  - 'fwnode_graph_for_each_endpoint'
  - 'gadget_for_each_ep'
  - 'genradix_for_each'
  - 'genradix_for_each_from'
  - 'genradix_for_each_reverse'
  - 'hash_for_each'
  - 'hash_for_each_possible'
  - 'hash_for_each_possible_rcu'
  - 'hash_for_each_possible_rcu_notrace'
  - 'hash_for_each_possible_safe'
  - 'hash_for_each_rcu'
  - 'hash_for_each_safe'
  - 'hashmap__for_each_entry'
  - 'hashmap__for_each_entry_safe'
  - 'hashmap__for_each_key_entry'
  - 'hashmap__for_each_key_entry_safe'
  - 'hctx_for_each_ctx'
  - 'hists__for_each_format'
  - 'hists__for_each_sort_list'
  - 'hlist_bl_for_each_entry'
  - 'hlist_bl_for_each_entry_rcu'
  - 'hlist_bl_for_each_entry_safe'
  - 'hlist_for_each'
  - 'hlist_for_each_entry'
  - 'hlist_for_each_entry_continue'
  - 'hlist_for_each_entry_continue_rcu'
  - 'hlist_for_each_entry_continue_rcu_bh'
  - 'hlist_for_each_entry_from'
  - 'hlist_for_each_entry_from_rcu'
  - 'hlist_for_each_entry_rcu'
  - 'hlist_for_each_entry_rcu_bh'
  - 'hlist_for_each_entry_rcu_notrace'
  - 'hlist_for_each_entry_safe'
  - 'hlist_for_each_entry_srcu'
  - 'hlist_for_each_safe'
  - 'hlist_nulls_for_each_entry'
  - 'hlist_nulls_for_each_entry_from'
  - 'hlist_nulls_for_each_entry_rcu'
  - 'hlist_nulls_for_each_entry_safe'
  - 'i3c_bus_for_each_i2cdev'
  - 'i3c_bus_for_each_i3cdev'
  - 'idr_for_each_entry'
  - 'idr_for_each_entry_continue'
  - 'idr_for_each_entry_continue_ul'
  - 'idr_for_each_entry_ul'
  - 'iio_for_each_active_channel'
  - 'in_dev_for_each_ifa_rcu'
  - 'in_dev_for_each_ifa_rtnl'
  - 'in_dev_for_each_ifa_rtnl_net'
  - 'inet_bind_bucket_for_each'
  - 'interval_tree_for_each_span'
  - 'intlist__for_each_entry'
  - 'intlist__for_each_entry_safe'
  - 'kcore_copy__for_each_phdr'
  - 'key_for_each'
  - 'key_for_each_safe'
  - 'klp_for_each_func'
  - 'klp_for_each_func_safe'
  - 'klp_for_each_func_static'
  - 'klp_for_each_object'
  - 'klp_for_each_object_safe'
  - 'klp_for_each_object_static'
  - 'kunit_suite_for_each_test_case'
  - 'kvm_for_each_memslot'
  - 'kvm_for_each_memslot_in_gfn_range'
  - 'kvm_for_each_vcpu'
  - 'libbpf_nla_for_each_attr'
  - 'list_for_each'
  - 'list_for_each_codec'
  - 'list_for_each_codec_safe'
  - 'list_for_each_continue'
  - 'list_for_each_entry'
  - 'list_for_each_entry_continue'
  - 'list_for_each_entry_continue_rcu'
  - 'list_for_each_entry_continue_reverse'
  - 'list_for_each_entry_from'
  - 'list_for_each_entry_from_rcu'
  - 'list_for_each_entry_from_reverse'
  - 'list_for_each_entry_lockless'
  - 'list_for_each_entry_rcu'
  - 'list_for_each_entry_reverse'
  - 'list_for_each_entry_safe'
  - 'list_for_each_entry_safe_continue'
  - 'list_for_each_entry_safe_from'
  - 'list_for_each_entry_safe_reverse'
  - 'list_for_each_entry_srcu'
  - 'list_for_each_from'
  - 'list_for_each_prev'
  - 'list_for_each_prev_safe'
  - 'list_for_each_rcu'
  - 'list_for_each_safe'
  - 'llist_for_each'
  - 'llist_for_each_entry'
  - 'llist_for_each_entry_safe'
  - 'llist_for_each_safe'
  - 'lwq_for_each_safe'
  - 'map__for_each_symbol'
  - 'map__for_each_symbol_by_name'
  - 'mas_for_each'
  - 'mas_for_each_rev'
  - 'mci_for_each_dimm'
  - 'media_device_for_each_entity'
  - 'media_device_for_each_intf'
  - 'media_device_for_each_link'
  - 'media_device_for_each_pad'
  - 'media_entity_for_each_pad'
  - 'media_pipeline_for_each_entity'
  - 'media_pipeline_for_each_pad'
  - 'mlx5_lag_for_each_peer_mdev'
  - 'mptcp_for_each_subflow'
  - 'msi_domain_for_each_desc'
  - 'msi_for_each_desc'
  - 'mt_for_each'
  - 'nanddev_io_for_each_block'
  - 'nanddev_io_for_each_page'
  - 'neigh_for_each_in_bucket'
  - 'neigh_for_each_in_bucket_rcu'
  - 'neigh_for_each_in_bucket_safe'
  - 'netdev_for_each_lower_dev'
  - 'netdev_for_each_lower_private'
  - 'netdev_for_each_lower_private_rcu'
  - 'netdev_for_each_mc_addr'
  - 'netdev_for_each_synced_mc_addr'
  - 'netdev_for_each_synced_uc_addr'
  - 'netdev_for_each_uc_addr'
  - 'netdev_for_each_upper_dev_rcu'
  - 'netdev_hw_addr_list_for_each'
  - 'nft_rule_for_each_expr'
  - 'nla_for_each_attr'
  - 'nla_for_each_attr_type'
  - 'nla_for_each_nested'
  - 'nla_for_each_nested_type'
  - 'nlmsg_for_each_attr'
  - 'nlmsg_for_each_msg'
  - 'nr_neigh_for_each'
  - 'nr_neigh_for_each_safe'
  - 'nr_node_for_each'
  - 'nr_node_for_each_safe'
  - 'of_for_each_phandle'
  - 'of_property_for_each_string'
  - 'of_property_for_each_u32'
  - 'pci_bus_for_each_resource'
  - 'pci_dev_for_each_resource'
  - 'pcl_for_each_chunk'
  - 'pcl_for_each_segment'
  - 'pcm_for_each_format'
  - 'perf_config_items__for_each_entry'
  - 'perf_config_sections__for_each_entry'
  - 'perf_config_set__for_each_entry'
  - 'perf_cpu_map__for_each_cpu'
  - 'perf_cpu_map__for_each_cpu_skip_any'
  - 'perf_cpu_map__for_each_idx'
  - 'perf_evlist__for_each_entry'
  - 'perf_evlist__for_each_entry_reverse'
  - 'perf_evlist__for_each_entry_safe'
  - 'perf_evlist__for_each_evsel'
  - 'perf_evlist__for_each_mmap'
  - 'perf_evsel_for_each_per_thread_period_safe'
  - 'perf_hpp_list__for_each_format'
  - 'perf_hpp_list__for_each_format_safe'
  - 'perf_hpp_list__for_each_sort_list'
  - 'perf_hpp_list__for_each_sort_list_safe'
  - 'plist_for_each'
  - 'plist_for_each_continue'
  - 'plist_for_each_entry'
  - 'plist_for_each_entry_continue'
  - 'plist_for_each_entry_safe'
  - 'plist_for_each_safe'
  - 'pnp_for_each_card'
  - 'pnp_for_each_dev'
  - 'protocol_for_each_card'
  - 'protocol_for_each_dev'
  - 'queue_for_each_hw_ctx'
  - 'radix_tree_for_each_slot'
  - 'radix_tree_for_each_tagged'
  - 'rb_for_each'
  - 'rbtree_postorder_for_each_entry_safe'
  - 'rdma_for_each_block'
  - 'rdma_for_each_port'
  - 'rdma_umem_for_each_dma_block'
  - 'resource_list_for_each_entry'
  - 'resource_list_for_each_entry_safe'
  - 'rhl_for_each_entry_rcu'
  - 'rhl_for_each_rcu'
  - 'rht_for_each'
  - 'rht_for_each_entry'
  - 'rht_for_each_entry_from'
  - 'rht_for_each_entry_rcu'
  - 'rht_for_each_entry_rcu_from'
  - 'rht_for_each_entry_safe'
  - 'rht_for_each_from'
  - 'rht_for_each_rcu'
  - 'rht_for_each_rcu_from'
  - 'rq_for_each_bvec'
  - 'rq_for_each_segment'
  - 'rq_list_for_each'
  - 'rq_list_for_each_safe'
  - 'sample_read_group__for_each'
  - 'scsi_for_each_prot_sg'
  - 'scsi_for_each_sg'
  - 'sctp_for_each_hentry'
  - 'sctp_skb_for_each'
  - 'sec_for_each_insn'
  - 'sec_for_each_insn_continue'
  - 'sec_for_each_insn_from'
  - 'sec_for_each_sym'
  - 'shdma_for_each_chan'
  - 'shost_for_each_device'
  - 'sk_for_each'
  - 'sk_for_each_bound'
  - 'sk_for_each_bound_safe'
  - 'sk_for_each_entry_offset_rcu'
  - 'sk_for_each_from'
  - 'sk_for_each_rcu'
  - 'sk_for_each_safe'
  - 'sk_nulls_for_each'
  - 'sk_nulls_for_each_from'
  - 'sk_nulls_for_each_rcu'
  - 'snd_array_for_each'
  - 'snd_pcm_group_for_each_entry'
  - 'snd_soc_dapm_widget_for_each_path'
  - 'snd_soc_dapm_widget_for_each_path_safe'
  - 'snd_soc_dapm_widget_for_each_sink_path'
  - 'snd_soc_dapm_widget_for_each_source_path'
  - 'sparsebit_for_each_set_range'
  - 'strlist__for_each_entry'
  - 'strlist__for_each_entry_safe'
  - 'sym_for_each_insn'
  - 'sym_for_each_insn_continue_reverse'
  - 'symbols__for_each_entry'
  - 'tb_property_for_each'
  - 'tcf_act_for_each_action'
  - 'tcf_exts_for_each_action'
  - 'test_suite__for_each_test_case'
  - 'tool_pmu__for_each_event'
  - 'ttm_bo_lru_for_each_reserved_guarded'
  - 'ttm_resource_manager_for_each_res'
  - 'udp_lrpa_for_each_entry_rcu'
  - 'udp_portaddr_for_each_entry'
  - 'udp_portaddr_for_each_entry_rcu'
  - 'usb_hub_for_each_child'
  - 'v4l2_device_for_each_subdev'
  - 'v4l2_m2m_for_each_dst_buf'
  - 'v4l2_m2m_for_each_dst_buf_safe'
  - 'v4l2_m2m_for_each_src_buf'
  - 'v4l2_m2m_for_each_src_buf_safe'
  - 'virtio_device_for_each_vq'
  - 'vkms_config_for_each_connector'
  - 'vkms_config_for_each_crtc'
  - 'vkms_config_for_each_encoder'
  - 'vkms_config_for_each_plane'
  - 'vkms_config_connector_for_each_possible_encoder'
  - 'vkms_config_encoder_for_each_possible_crtc'
  - 'vkms_config_plane_for_each_possible_crtc'
  - 'while_for_each_ftrace_op'
  - 'workloads__for_each'
  - 'xa_for_each'
  - 'xa_for_each_marked'
  - 'xa_for_each_range'
  - 'xa_for_each_start'
  - 'xas_for_each'
  - 'xas_for_each_conflict'
  - 'xas_for_each_marked'
  - 'xbc_array_for_each_value'
  - 'xbc_for_each_key_value'
  - 'xbc_node_for_each_array_value'
  - 'xbc_node_for_each_child'
  - 'xbc_node_for_each_key_value'
  - 'xbc_node_for_each_subkey'
  - 'ynl_attr_for_each'
  - 'ynl_attr_for_each_nested'
  - 'ynl_attr_for_each_payload'
  - 'zorro_for_each_dev'

IncludeBlocks: Preserve
IncludeCategories:
  - Regex: '.*'
    Priority: 1
IncludeIsMainRegex: '(Test)?$'
IndentCaseLabels: false
IndentGotoLabels: false
IndentPPDirectives: None
IndentWidth: 8
IndentWrappedFunctionNames: false
JavaScriptQuotes: Leave
JavaScriptWrapImports: true
KeepEmptyLinesAtTheStartOfBlocks: false
MacroBlockBegin: ''
MacroBlockEnd: ''
MaxEmptyLinesToKeep: 1
NamespaceIndentation: None
ObjCBinPackProtocolList: Auto
ObjCBlockIndentWidth: 8
ObjCSpaceAfterProperty: true
ObjCSpaceBeforeProtocolList: true

# Taken from git's rules
PenaltyBreakAssignment: 10
PenaltyBreakBeforeFirstCallParameter: 30
PenaltyBreakComment: 10
PenaltyBreakFirstLessLess: 0
PenaltyBreakString: 10
PenaltyExcessCharacter: 100
PenaltyReturnTypeOnItsOwnLine: 60

PointerAlignment: Right
ReflowComments: false
SortIncludes: false
SortUsingDeclarations: false
SpaceAfterCStyleCast: false
SpaceAfterTemplateKeyword: true
SpaceBeforeAssignmentOperators: true
SpaceBeforeCtorInitializerColon: true
SpaceBeforeInheritanceColon: true
SpaceBeforeParens: ControlStatementsExceptForEachMacros
SpaceBeforeRangeBasedForLoopColon: true
SpaceInEmptyParentheses: false
SpacesBeforeTrailingComments: 1
SpacesInAngles: false
SpacesInContainerLiterals: false
SpacesInCStyleCastParentheses: false
SpacesInParentheses: false
SpacesInSquareBrackets: false
Standard: Cpp03
TabWidth: 8
UseTab: Always
InsertNewlineAtEOF: true
KeepEmptyLinesAtEOF: true
...
"""

# ---------------------------------------------------------------------------
# 通用小工具
# ---------------------------------------------------------------------------

RE_WS = re.compile(r"[ \t]+$")


def read_lines(path: Path):
	"""读文件，统一 CRLF -> LF，返回 (不带换行符的行列表, 编码)。
	编码按 utf-8 -> gbk -> latin-1 探测，写回时保持原编码。"""
	data = path.read_bytes()
	encoding = "latin-1"
	for enc in ("utf-8", "gbk"):
		try:
			text = data.decode(enc)
			encoding = enc
			break
		except UnicodeDecodeError:
			continue
	else:
		text = data.decode("latin-1")
	text = text.replace("\r\n", "\n").replace("\r", "\n")
	return text.split("\n"), encoding


def write_lines(path: Path, lines, encoding="utf-8"):
	"""行列表写回，文件末尾保留恰好一个空行。"""
	while lines and lines[-1] == "":
		lines.pop()
	path.write_text("\n".join(lines) + "\n\n", encoding=encoding)


def collapse_blanks(lines, keep=1):
	out, run = [], 0
	for line in lines:
		if line.strip() == "":
			run += 1
			if run > keep:
				continue
			out.append("")
		else:
			run = 0
			out.append(line)
	while out and out[0] == "":
		out.pop(0)
	while out and out[-1] == "":
		out.pop()
	return out


RE_PP_INDENTED = re.compile(r"^\s+#\s*(?:if|ifdef|ifndef|endif|else|elif)\b")
RE_PP_COND_CODE = re.compile(r"^(\s*)#\s*(ifdef|ifndef)\s+(\S+)\s+(\S.*)$")
RE_PP_IF_CODE = re.compile(r"^(\s*)#\s*if\s+((?:defined\s*\(\s*\w+\s*\)|\w+))\s+(\S.*)$")
RE_COND_OP = re.compile(r"^(?:\|\||&&|==|!=|<=|>=|[|&)])")


def normalize_pp_lines(lines):
	"""#if/#ifdef/#endif 等预处理指令顶行（去缩进）；
	#ifdef/#if 条件后跟随的代码拆到下一行（保持原缩进）。
	条件以 ||/&&/比较运算符延续的不拆。"""
	out = []
	for line in lines:
		m = RE_PP_COND_CODE.match(line)
		if m and not RE_COND_OP.match(m.group(4)):
			ind, kw, cond, code = m.groups()
			out.append(f"#{kw} {cond}")
			out.append(f"{ind}{code}")
			continue
		m = RE_PP_IF_CODE.match(line)
		if m and not RE_COND_OP.match(m.group(3)):
			ind, cond, code = m.groups()
			out.append(f"#if {cond}")
			out.append(f"{ind}{code}")
			continue
		if RE_PP_INDENTED.match(line):
			out.append(line.lstrip())
			continue
		out.append(line)
	return out


# ---------------------------------------------------------------------------
# pre 阶段
# ---------------------------------------------------------------------------



def _has_open_quote(text: str) -> bool:
	"""代码文本是否以未闭合的引号结尾（用于判断行尾 /* 是否在字符串外）。"""
	i, n = 0, len(text)
	while i < n:
		ch = text[i]
		if ch in "\"'":
			q = ch
			i += 1
			while i < n:
				if text[i] == "\\":
					i += 1
				elif text[i] == q:
					break
				i += 1
			if i >= n:
				return True
		i += 1
	return False

def _code_paren_delta(text: str) -> int:
	"""粗略统计代码文本的圆括号净增量（忽略字符串/字符/注释内容）。"""
	depth = 0
	i = 0
	n = len(text)
	while i < n:
		ch = text[i]
		if ch in "\"'":
			q = ch
			i += 1
			while i < n and text[i] != q:
				if text[i] == "\\":
					i += 1
				i += 1
		elif text.startswith("/*", i):
			end = text.find("*/", i + 2)
			i = n if end < 0 else end + 2
		elif text.startswith("//", i):
			break
		elif ch == "(":
			depth += 1
		elif ch == ")":
			depth -= 1
		i += 1
	return depth

RE_BANNER_HEAD = re.compile(
	r"^(\s*)/\*(?:\*{3,}|-{3,}|={3,})\s*([^\-*=][^*]*?[^\-*=\s])\s*(?:\*{2,}|-{2,}|={2,})\s*\*/\s*$"
)
RE_BANNER_TAIL = re.compile(r"^(\s*)/\*\s*([^*/]*?\S)\s*[-=]{3,}\s*\*/\s*$")
RE_STAR_PAD = re.compile(r"^(\s*/\*\s*[^*]*?\S)[ \t]*\*{2,}[ \t]*\*/[ \t]*$")
RE_SLASH_FULL = re.compile(r"^(\s*)//\s?(.*)$")
RE_SLASH_TAIL = re.compile(r"^(\s*)(\S.*?)\s*//\s?(.*)$")
RE_BLOCK_TAIL = re.compile(r"^(\s*)(\S(?:.*?\S)?)\s*/\*(?:!(?=[<\s])|<(?=\s))?\s*(.*?)\s*\*/\s*$")
RE_ONELINE = re.compile(r"^(\s*)/\*\s*(\S(?:.*?\S)?)\s*\*/(\s*)$")
RE_CONT_OP = re.compile(r"[|&,(+\-=]\s*$")


RE_SIMPLE_MACRO_BODY = re.compile(r"[;{}]|\b(?:do|while|if|for|else|switch)\b")


def merge_multiline_defines(lines):
	"""--def 模式：多行 #define 先合并为单行（再处理行尾注释，防续行注释被抽走）。

	只合并寄存器地址、位或运算等单表达式简单宏；含语句的复杂宏
	（do-while、if、多条语句）按规范保持多行格式，不合并。
	"""
	out, i = [], 0
	while i < len(lines):
		line = lines[i]
		if line.startswith("#define ") and re.search(r"\\\s*$", line):
			start = i
			merged = re.sub(r"\\\s*$", "", line)
			while i + 1 < len(lines):
				i += 1
				cont = lines[i]
				more = bool(re.search(r"\\\s*$", cont))
				cont = re.sub(r"\\\s*$", "", cont).lstrip()
				merged += " " + cont
				if not more:
					break
			if RE_SIMPLE_MACRO_BODY.search(merged):
				out.extend(lines[start : i + 1])
			else:
				out.append(re.sub(r"\s+", " ", merged))
		else:
			out.append(line)
		i += 1
	return out


def pre_transform(lines, def_mode):
	out = []
	in_comment = False
	pending_doxy = False
	paren_depth = 0

	for raw in lines:
		line = RE_WS.sub("", raw)

		# 块注释内空 `*` 行删除
		if in_comment and re.match(r"^\s*\*\s*$", line):
			continue

		# Doxygen 分组标记整块移除
		if re.search(r"@(addtogroup|defgroup)\b", line):
			if "*/" not in line:
				in_comment = True
				pending_doxy = True
			continue
		if pending_doxy:
			if "*/" in line:
				in_comment = False
				pending_doxy = False
			continue
		if re.match(r"^\s*(/\*\*?|\*)\s*@\{\s*(\*/\s*)?$", line):
			if "*/" in line:
				in_comment = False
			continue
		if re.match(r"^\s*(/\*\*?|\*)\s*@\}\s*(\*/\s*)?$", line):
			continue

		# 带标题的装饰线 -> /* title */
		m = RE_BANNER_HEAD.match(line)
		if m and m.group(2).strip():
			title = m.group(2).strip("-*= ")
			if title:
				line = f"{m.group(1)}/* {title} */"
		else:
			m = RE_BANNER_TAIL.match(line)
			if m:
				line = f"{m.group(1)}/* {m.group(2)} */"

		# 长星号填充: /* Title **********/ -> /* Title */
		# 捕获的标题必须含非装饰字符，纯 /****/ 行交给 remove_decorative_lines
		m = RE_STAR_PAD.match(line)
		if m and re.search(r"[^*=\/\s-]", m.group(1)):
			line = m.group(1) + " */"

		# 整行 // -> /* */
		if not in_comment:
			m = RE_SLASH_FULL.match(line)
			if m:
				c = m.group(2).strip()
				if "/*" in c or "*/" in c:
					c = c.replace("/*", "").replace("*/", "").rstrip()
				line = f"{m.group(1)}/* {c} */" if c else f"{m.group(1)}/* */"

		# 行尾 // 注释 -> 移到上一行（续行语句则原地转 /* */）
		inlined = False
		if not in_comment:
			m = RE_SLASH_TAIL.match(line)
			if (
				m
				and not _has_open_quote(m.group(2))
				and "/*" not in m.group(2)
				and "*/" not in m.group(2)
			):
				ind, code, c = m.group(1), m.group(2), m.group(3).strip()
				if "/*" in c or "*/" in c:
					c = c.replace("/*", "").replace("*/", "").rstrip()
				c = re.sub(r"^<-+\s*", "", c)
				complete = (
					bool(re.search(r"[;{}:]\s*$", code))
					or code.startswith("#")
					or bool(RE_CONTROL.match(code))
				)
				cont = bool(out and RE_CONT_OP.search(out[-1]))
				if (
					not code.rstrip().endswith("\\")
					and not code.rstrip().endswith(":")
					and complete
					and not cont
					and paren_depth == 0
					and _code_paren_delta(code) == 0
				):
					if out and out[-1].strip() and not def_mode:
						out.append("")
					out.append(f"{ind}/* {c} */")
					line = ind + code
				else:
					line = f"{ind}{code} /* {c} */"
					inlined = True

		# 行尾 /* */ 注释（含 /*!< /*! /* !）-> 移到上一行
		if not in_comment and not inlined:
			m = RE_BLOCK_TAIL.match(line)
			if m and not _has_open_quote(m.group(2)):
				ind, code, c = m.group(1), m.group(2), m.group(3).strip()
				complete = (
					bool(re.search(r"[;{}:,]\s*$", code))
					or code.startswith("#")
					or bool(RE_CONTROL.match(code))
				)
				cont = bool(out and RE_CONT_OP.search(out[-1]))
				if (
					"/*" not in code
					and not code.rstrip().endswith("\\")
					and not code.rstrip().endswith(":")
					and not code.startswith("*")
					and complete
					and not cont
					and paren_depth == 0
					and _code_paren_delta(code) == 0
				):
					if c:
						if out and out[-1].strip() and not def_mode:
							out.append("")
						out.append(f"{ind}/* {c} */")
					line = ind + code

		# 单行 /*foo*/ 间距规范化（纯装饰行不动）
		m = RE_ONELINE.match(line)
		if m and not re.match(r"^[*= -]*$", m.group(2)):
			c = re.sub(r"^\*\s+", "", m.group(2))
			c = re.sub(r"^!(?=[<\s])", "", c)
			c = re.sub(r"^<(?=\s)", "", c)
			line = f"{m.group(1)}/* {c} */"

		out.append(line)
		paren_depth = max(0, paren_depth + _code_paren_delta(line))

		# 块注释状态跟踪
		if not in_comment and "/*" in line and "*/" not in line:
			in_comment = True
		elif in_comment and "*/" in line:
			in_comment = False

	return out


def collapse_single_line_block_comments(lines):
	"""/* \\n * foo \\n */ 三行单内容块注释合并为一行。"""
	out, i = [], 0
	while i < len(lines):
		m_open = re.match(r"^(\s*)/\*\s*$", lines[i]) if i + 2 < len(lines) else None
		m_body = re.match(r"^\s*\*\s+(\S.*?)\s*$", lines[i + 1]) if m_open else None
		m_close = re.match(r"^\s*\*/\s*$", lines[i + 2]) if m_body else None
		if m_open and m_body and m_close:
			out.append(f"{m_open.group(1)}/* {m_body.group(1)} */")
			i += 3
		else:
			out.append(lines[i])
			i += 1
	return out


RE_DECO_RUN = re.compile(r"([\*=\-])\1{3,}")
RE_PURE_DECO = re.compile(r"^\s*/?[\s*/=\-]*$")


def remove_decorative_lines(lines):
	"""清理纯装饰注释行（只含 / * - = 空格且含 4+ 连续装饰字符）。

	按块注释状态分类处理：
	- 块外单行完整装饰注释 /****/：直接删除
	- 块外开工行 /****...：规范为 /*，进入块注释状态
	- 块内闭工行（含 /****/ 形式）：规范为 */，退出块注释状态
	- 块中间装饰行（如 * ----）：删除
	前后行含 `|` 的视为 ASCII 表格边框（文档内容），一律保留。
	"""
	out = []
	in_comment = False
	for i, line in enumerate(lines):
		if RE_PURE_DECO.match(line) and RE_DECO_RUN.search(line):
			prev = lines[i - 1] if i > 0 else ""
			nxt = lines[i + 1] if i + 1 < len(lines) else ""
			if "|" in prev or "|" in nxt:
				out.append(line)
				continue
			ind = line[: len(line) - len(line.lstrip())]
			has_open = "/*" in line
			has_close = "*/" in line
			if in_comment:
				if has_close:
					out.append(ind + " */")
					in_comment = False
			elif has_open and has_close:
				continue
			elif has_open:
				out.append(ind + "/*")
				in_comment = True
			elif has_close:
				out.append(ind + " */")
		else:
			out.append(line)
			if not in_comment and "/*" in line and "*/" not in line:
				in_comment = True
			elif in_comment and "*/" in line:
				in_comment = False
	return out


RE_BARE_TAG = re.compile(r"^\s*\*?\s*@[A-Za-z]+(\[[^\]]*\])?\s*(\*/)?\s*$")
RE_STAR_ONLY = re.compile(r"^\s*\*+\s*$")


def remove_contentless_comments(lines):
	"""删除无实际内容的注释：
	- 单行空标签注释 /* @brief */
	- 每一行都是空行或空标签（@brief/@param[in]/@return 后无文字）的块注释
	"""
	out = []
	i = 0
	while i < len(lines):
		if RE_BARE_TAG.match(lines[i]) and "/*" in lines[i] and "*/" in lines[i]:
			i += 1
			continue
		if re.match(r"^\s*/\*+", lines[i]) and "*/" not in lines[i]:
			j = i + 1
			while j < len(lines) and "*/" not in lines[j]:
				j += 1
			if j < len(lines):
				opener = re.sub(r"^\s*/\*+\s*", "", lines[i]).strip()
				inner = lines[i + 1 : j]
				contentless = (
					not opener
					and all(
						RE_STAR_ONLY.match(l) or RE_BARE_TAG.match(l)
						for l in inner
					)
				)
				if contentless:
					i = j + 1
					continue
			out.extend(lines[i : j + 1])
			i = j + 1
		else:
			out.append(lines[i])
			i += 1
	return out


def remove_empty_comment_blocks(lines):
	"""删除空注释：单行 /* */ 及 /** \\n */ 形式的空块。"""
	out, i = [], 0
	while i < len(lines):
		if re.match(r"^\s*/\*\s*\*/\s*$", lines[i]):
			i += 1
		elif (
			i + 1 < len(lines)
			and re.match(r"^\s*/\*+\s*$", lines[i])
			and re.match(r"^\s*\*/\s*$", lines[i + 1])
		):
			i += 2
		else:
			out.append(lines[i])
			i += 1
	return out


# ---------------------------------------------------------------------------
# clang-format 阶段
# ---------------------------------------------------------------------------

def is_register_def_file(lines):
	"""#define 占代码行多数时判定为寄存器定义头文件（def 模式）。"""
	code = [
		l for l in lines
		if l.strip() and not l.lstrip().startswith(("/*", "*", "//"))
	]
	if not code:
		return False
	defs = sum(1 for l in code if l.startswith("#define"))
	return defs * 2 > len(code)


def run_clang_format(path: Path, style_path: Path):
	clang = shutil.which("clang-format")
	if not clang:
		sys.exit("error: clang-format 不在 PATH 中")
	subprocess.run(
		[clang, f"-style=file:{style_path}", "-i", str(path)],
		check=True,
	)


# ---------------------------------------------------------------------------
# post 阶段
# ---------------------------------------------------------------------------

RE_EMPTY_LOOP = re.compile(r"^(\s*(?:while|for)\s*\(.*\))\s*$")
RE_ELSE = re.compile(r"^\s*\}\s*else\b")
RE_DEFINE = re.compile(r"^#define\s+(\S+)\s+(\S.*)$")
RE_COMMENT_LINE = re.compile(r"^\s*/\*.*\*/\s*$")


def tab_pad(name: str, target: int) -> str:
	col, pad = len(name), ""
	while True:
		pad += "\t"
		col = (col + 8) - (col % 8)
		if col >= target:
			return pad


def align_defines(lines):
	"""同一区域（允许注释行穿插，空行分隔）的 #define 值用 Tab 对齐。"""
	out, region = [], []

	def flush():
		nonlocal region
		matches = {}
		for i, line in enumerate(region):
			m = RE_DEFINE.match(line)
			if m:
				matches[i] = m
		obj = {i: m for i, m in matches.items() if "(" not in m.group(1)}
		if len(matches) >= 2 and obj:
			target = max(len(m.group(1)) for m in obj.values()) + 1
			if target % 8:
				target += 8 - target % 8
			for i, m in obj.items():
				name = m.group(1)
				region[i] = "#define " + name + tab_pad(name, target) + m.group(2)
		out.extend(region)
		region = []

	for line in lines:
		if RE_DEFINE.match(line) and not line.rstrip().endswith("\\"):
			region.append(line)
		elif RE_COMMENT_LINE.match(line) and region:
			region.append(line)
		else:
			flush()
			out.append(line)
	flush()
	return out


RE_COMMENT_START = re.compile(r"^\s*/\*")


def _zone_of(lines, i):
	"""顶层声明区域分类：include / define / decl（全局变量、类型、原型）/ func。"""
	line = lines[i]
	if line.startswith("#include"):
		return "include"
	if line.startswith("#define"):
		return "define"
	if line.startswith("#"):
		return None
	if _is_func_def(lines, i):
		return "func"
	if line.rstrip().endswith(":") or line.rstrip() in ("}", "{"):
		return None
	return "decl"


def normalize_comment_blanks(lines):
	"""注释行与前一行代码之间空一行；前一行也是注释则不空。
	顶层声明区域（include/define/全局变量/函数）转换处空一行。"""
	out = []
	in_comment = False
	prev_kind = None  # 'code' | 'comment' | None
	prev_zone = None

	for idx, line in enumerate(lines):
		if line.strip() == "":
			out.append(line)
			continue

		comment_start = (not in_comment) and bool(RE_COMMENT_START.match(line))
		if comment_start:
			if out and out[-1].strip() == "":
				# 前一行非空行是注释：去掉中间的空行
				if prev_kind == "comment":
					while out and out[-1].strip() == "":
						out.pop()
			elif prev_kind == "code" and not out[-1].rstrip().endswith("\\"):
				# 前一行是代码且没有空行：补一个空行（宏续行内不插）
				out.append("")
		elif not line.startswith((" ", "\t")):
			zone = _zone_of(lines, idx)
			if (
				zone
				and prev_zone
				and zone != prev_zone
				and prev_kind == "code"
				and out
				and out[-1].strip() != ""
				and not out[-1].rstrip().endswith("\\")
				and not (
					out[-1].startswith("#")
					and not out[-1].startswith(("#include", "#define"))
				)
			):
				out.append("")
			if zone:
				prev_zone = zone

		out.append(line)

		line_is_comment = in_comment or comment_start
		if comment_start and "*/" not in line:
			in_comment = True
		elif in_comment and "*/" in line:
			in_comment = False
		prev_kind = "comment" if line_is_comment else "code"

	return collapse_blanks(out)


RE_DEFINE_OBJ = re.compile(r"^#define\s+(\w+)\s+(\S.*)$")
RE_DEFINE_FUNC = re.compile(r"^#define\s+(\w+\([^)]*\))\s+(\S.*)$")


def align_defines_reference_groups(lines):
	"""def 模式：#define 分两组规则成组，组内值 Tab 对齐到统一列。

	成组条件（满足其一）：
	  1. 宏值引用了组内已有宏名（引用链，注释/空行不打断）
	  2. 与上一个组内宏物理相邻（连续两个以上宏定义）
	函数式单行宏以 NAME(params) 整体参与对齐；多行宏跳过。
	"""
	out = list(lines)
	group = []
	names = set()
	last_member = -10

	def flush():
		if len(group) >= 2:
			target = max(len(disp) for _, disp, _, _ in group) + 1
			if target % 8:
				target += 8 - target % 8
			for idx, disp, _, value in group:
				out[idx] = "#define " + disp + tab_pad(disp, target) + value
		group.clear()
		names.clear()

	for idx, line in enumerate(out):
		if line.rstrip().endswith("\\"):
			continue
		m = RE_DEFINE_FUNC.match(line) or RE_DEFINE_OBJ.match(line)
		if not m:
			continue
		disp, value = m.group(1), m.group(2)
		bare = disp.split("(")[0]
		if group and idx != last_member + 1 and not any(
			re.search(r"\b" + re.escape(n) + r"\b", value) for n in names
		):
			flush()
		group.append((idx, disp, bare, value))
		names.add(bare)
		last_member = idx
	flush()
	return out


RE_ARRAY_DECL = re.compile(
	r"^(\s*)((?:(?:static|const|volatile)\s+)*"
	r"(?:u?int(?:8|16|32|64)_t|rt_u?int(?:8|16|32|64)_t|unsigned\s+(?:char|short|int|long)|char|short|int|long)"
	r"\s+\w+(?:\s*\[[^\]]*\])+\s*=\s*)(?:\{(.*))?$"
)
RE_NUMERIC = re.compile(r"^[-+]?(?:0[xX][0-9a-fA-F]+|\d+)[uUlL]*$")


def _array_per_line(decl_text: str) -> int:
	"""1/2 字节元素每行 8 个，4/8 字节每行 4 个。"""
	m = re.search(r"(?:u?int(8|16|32|64)_t|char|short|int|long)", decl_text)
	width = m.group(1) if m and m.group(1) else ""
	if width in ("8", "16"):
		return 8
	if width:
		return 4
	return 8 if re.search(r"\b(char|short)\b", decl_text) else 4


def format_numeric_arrays(lines):
	"""纯数字常量数组统一排版：
	- 左花括号跟声明行，右花括号单独一行
	- 元素从声明下一行开始，按元素宽度每行 8 个（1/2 字节）或 4 个（4/8 字节）
	- 含注释、嵌套括号、非数字元素、元素数不超过每行数量的，保持原样
	"""
	out, i = [], 0
	while i < len(lines):
		m = RE_ARRAY_DECL.match(lines[i])
		if not m:
			out.append(lines[i])
			i += 1
			continue

		indent, decl, tail = m.group(1), m.group(2), m.group(3)
		if tail is None:
			if i + 1 < len(lines) and lines[i + 1].strip() == "{":
				tail = ""
				j = i + 2
			else:
				out.append(lines[i])
				i += 1
				continue
		else:
			j = i + 1

		body = tail
		while "}" not in body and j < len(lines):
			body += " " + lines[j].strip()
			j += 1
		if "}" not in body:
			out.append(lines[i])
			i += 1
			continue

		head, _, rest = body.partition("}")
		if not re.match(r"^\s*;?\s*$", rest):
			out.append(lines[i])
			i += 1
			continue
		if "/*" in head or "{" in head:
			out.append(lines[i])
			i += 1
			continue

		elements = [e.strip() for e in head.split(",") if e.strip()]
		per_line = _array_per_line(decl)
		if (
			len(elements) <= per_line
			or not all(RE_NUMERIC.match(e) for e in elements)
		):
			out.append(lines[i])
			i += 1
			continue

		out.append(f"{indent}{decl}{{")
		for k in range(0, len(elements), per_line):
			chunk = elements[k : k + per_line]
			last = k + per_line >= len(elements)
			out.append(f"{indent}\t{', '.join(chunk)}{'' if last else ','}")
		out.append(f"{indent}}};")
		i = j

	return out


RE_FUNC_DEF_LINE = re.compile(r"^(?:[A-Za-z_]\w*[\s\*]+)+\*?[A-Za-z_]\w*\s*\([^;]*$")
RE_TOPLEVEL_CLOSE = re.compile(r"^\}\s*$")


def _is_func_def(lines, i):
	"""Allman 风格函数定义首行（多行签名最多向后看 10 行）。"""
	if not RE_FUNC_DEF_LINE.match(lines[i]):
		return False
	j = i + 1
	while j < len(lines) and j < i + 10:
		s = lines[j].strip()
		if s == "{":
			return True
		if s.endswith(";") or s == "}":
			return False
		j += 1
	return False


def normalize_function_gaps(lines):
	"""函数定义与前一函数的 } 之间保持恰好一个空行；函数签名行与 { 之间不留空行。"""
	out = []
	for i, line in enumerate(lines):
		if not line.startswith((" ", "\t")) and _is_func_def(lines, i):
			k = len(out) - 1
			while k >= 0 and out[k].strip() == "":
				k -= 1
			if (
				k >= 0
				and RE_TOPLEVEL_CLOSE.match(out[k])
				and out[-1].strip() != ""
				and not out[-1].rstrip().endswith("\\")
			):
				out.append("")
		out.append(line)

	res = []
	i = 0
	while i < len(out):
		res.append(out[i])
		if _is_func_def(out, i):
			j = i + 1
			while j < len(out) and out[j].strip() == "":
				j += 1
			if j < len(out) and out[j].strip() == "{":
				i = j
			else:
				i += 1
		else:
			i += 1
	return res


RE_LOCAL_DECL = re.compile(
	r"^\s+(?!(?:return|if|else|for|while|switch|do|goto|break|continue|sizeof|case)\b)"
	r"(?:[A-Za-z_]\w*[\s\*]+)+\*?\s*[A-Za-z_]\w*"
	r"(?:\s*\[[^\]]*\])?"
	r"(?:\s*=\s*[^;]*)?"
	r"(?:\s*,\s*\*?\s*[A-Za-z_]\w*(?:\s*\[[^\]]*\])?(?:\s*=\s*[^,]*)?)*"
	r"\s*;\s*(?:/\*.*\*/\s*)?$"
)
RE_LABEL = re.compile(r"^\s*\w+:\s*(?:/\*.*\*/\s*)?$")


def normalize_decl_gaps(lines):
	"""函数内最后一个局部变量定义与执行代码之间空一行。"""
	out = []
	in_comment = False
	for line in lines:
		cs = (not in_comment) and bool(RE_COMMENT_START.match(line))
		is_other = (
			line.strip() == ""
			or cs
			or in_comment
			or line.strip() in ("{", "}", "};")
			or line.lstrip().startswith("#")
			or bool(RE_LABEL.match(line))
			or not line.startswith((" ", "\t"))
		)
		if not is_other and not RE_LOCAL_DECL.match(line):
			k = len(out) - 1
			while k >= 0 and out[k].strip() == "":
				k -= 1
			if (
				k >= 0
				and RE_LOCAL_DECL.match(out[k])
				and out[-1].strip() != ""
				and not out[-1].rstrip().endswith("\\")
			):
				out.append("")
		out.append(line)
		if cs and "*/" not in line:
			in_comment = True
		elif in_comment and "*/" in line:
			in_comment = False
	return out


RE_CONTROL = re.compile(r"^\s*(?:if|while|for|switch)\s*\(")
RE_JUMP = re.compile(r"^\s*(?:return\b|break\s*;|continue\s*;|goto\s)")


def normalize_statement_gaps(lines):
	"""if/while/for/switch 与前一行代码之间空一行；
	continue/break/return/goto 前一行不是控制行或块开始行时也要空一行
	（紧贴控制行/块开始行作为附属语句体时不空）。"""
	out = []
	in_comment = False
	prev_kind = None

	for line in lines:
		cs = (not in_comment) and bool(RE_COMMENT_START.match(line))
		indented = line.startswith((" ", "\t"))
		if indented and not cs and not in_comment and line.strip():
			if RE_CONTROL.match(line) or RE_JUMP.match(line):
				k = len(out) - 1
				while k >= 0 and out[k].strip() == "":
					k -= 1
				if k >= 0 and out[-1].strip() != "" and not out[-1].rstrip().endswith("\\"):
					prev = out[k]
					attached = (
						prev.rstrip().endswith("{")
						or prev.strip() == "else"
						or prev_kind == "comment"
						or bool(RE_LABEL.match(prev))
						or (
							bool(RE_CONTROL.match(prev))
							and not prev.rstrip().endswith(";")
						)
					)
					if not attached:
						out.append("")
		out.append(line)

		if cs and "*/" not in line:
			in_comment = True
		elif in_comment and "*/" in line:
			in_comment = False
		if line.strip():
			prev_kind = "comment" if (in_comment or cs) else "code"

	return out


RE_TYPE_ONELINE = re.compile(
	r"^(\s*)(enum|struct|union)\s+(\w*)\s*\{\s*(.*?)\s*\}\s*(\w*)\s*;\s*$"
)


def _split_top_level(body: str, sep: str):
	"""按顶层分隔符切分（括号/方括号内、字符串/字符字面量内的分隔符不算）。"""
	parts, depth, cur = [], 0, ""
	quote = None
	escaped = False
	for ch in body:
		if quote:
			cur += ch
			if ch == quote and not escaped:
				quote = None
			escaped = (ch == "\\" and not escaped)
			continue
		if ch in "\"'":
			quote = ch
			cur += ch
		elif ch in "([":
			depth += 1
			cur += ch
		elif ch in ")]":
			depth -= 1
			cur += ch
		elif ch == sep and depth == 0:
			parts.append(cur)
			cur = ""
		else:
			cur += ch
	parts.append(cur)
	return parts


def expand_single_line_types(lines):
	"""单行的 enum/struct/union 定义展开：每个枚举值/成员单独一行，
	{ 跟声明行，} 单独一行。空定义和含嵌套花括号的跳过。"""
	out = []
	for line in lines:
		m = RE_TYPE_ONELINE.match(line)
		if not m or not m.group(4) or "{" in m.group(4) or "}" in m.group(4):
			out.append(line)
			continue
		ind, kind, name, body, alias = m.groups()
		sep = "," if kind == "enum" else ";"
		parts = [p.strip() for p in _split_top_level(body, sep) if p.strip()]
		head = f"{ind}{kind} {name} {{" if name else f"{ind}{kind} {{"
		out.append(head)
		for k, part in enumerate(parts):
			last = k == len(parts) - 1
			if kind == "enum":
				out.append(f"{ind}\t{part}{'' if last else ','}")
			else:
				out.append(f"{ind}\t{part};")
		tail = f"{ind}}}"
		if alias:
			tail += f" {alias}"
		out.append(tail + ";")
	return out


RE_MEMBER_CONT = re.compile(r"^\s*(?:->|\.[A-Za-z_]|\[)")
RE_DESIGNATED_INIT = re.compile(r"^\s*\.\w[\w\[\].]*\s*=")
RE_DESIGNATED_INDEX = re.compile(r"^\s*\[[^\]]*\][\w.\[\]]*\s*=")


def join_member_breaks(lines):
	"""指针 ->、结构体 .、数组 [] 的成员访问不换行：
	被换到下一行的成员访问片段并回上一行（允许超出列宽限制）。
	指定初始化器 .field = 与 [IDX] = 行、宏续行、块注释内部不处理。"""
	out = []
	in_comment = False
	for line in lines:
		cs = (not in_comment) and bool(RE_COMMENT_START.match(line))
		if (
			out
			and not in_comment
			and not cs
			and not out[-1].rstrip().endswith("\\")
			and RE_MEMBER_CONT.match(line)
			and not RE_DESIGNATED_INIT.match(line)
			and not RE_DESIGNATED_INDEX.match(line)
		):
			out[-1] = out[-1] + line.strip()
			continue
		out.append(line)
		if not in_comment and "/*" in line and "*/" not in line:
			in_comment = True
		elif in_comment and "*/" in line:
			in_comment = False
	return out


TINY_TAIL = 8
RE_TINY_SKIP = re.compile(r"^\s*[}{]")


def _top_level_assign_pos(text: str) -> int:
	depth = 0
	quote = None
	escaped = False
	for idx, ch in enumerate(text):
		if quote:
			if ch == quote and not escaped:
				quote = None
			escaped = (ch == "\\" and not escaped)
			continue
		if ch in "\"'":
			quote = ch
		elif ch == "(":
			depth += 1
		elif ch == ")":
			depth -= 1
		elif ch == "=" and depth == 0:
			if text[idx - 1] in "=!<>" or text[idx + 1] == "=":
				continue
			return idx
	return -1


def rebalance_tiny_tails(lines):
	"""续行只剩极小碎尾（如单个 0;）时重新平衡换行：
	重组整句后能放一行（含缩进 <= 120）就并成一行，
	否则在顶层 = 处断开，避免单行只挂一个 token 的丑态。
	初始化器列表（= { ... }）内部不处理。"""
	out = list(lines)
	init_depth = 0
	i = 0
	while i < len(out):
		line = out[i]
		if init_depth == 0 and re.search(r"=\s*\{", line):
			d = line.count("{") - line.count("}")
			if d > 0:
				init_depth += d
				i += 1
				continue
		elif init_depth > 0:
			init_depth += line.count("{") - line.count("}")
			i += 1
			continue
		stripped = line.strip()
		if (
			not stripped
			or len(stripped) > TINY_TAIL
			or not out[i].startswith((" ", "\t"))
			or RE_TINY_SKIP.match(out[i])
			or stripped.startswith(("/*", "*", "//", "#"))
		):
			i += 1
			continue

		s = i - 1
		bound = max(0, i - 20)
		while s >= bound:
			p = out[s].strip()
			if (
				p == ""
				or p.startswith("#")
				or p.startswith(("/*", "*"))
				or p.endswith((";", "{", "}"))
				or p.startswith("case ")
				or p.startswith("default:")
				or re.match(r"(?:if|while|for|switch)\s*\(", p)
				or p.startswith("else")
			):
				break
			s -= 1
		s += 1
		if s >= i or not out[s].strip() or out[s].strip().endswith(";"):
			i += 1
			continue
		# 语句首行紧跟裸 { 且该 { 属于初始化器（前行是 = { / },），跳过
		if s > 0 and out[s - 1].strip() == "{":
			k = s - 2
			while k >= 0 and out[k].strip() == "":
				k -= 1
			prev2 = out[k].strip() if k >= 0 else ""
			if prev2.endswith("{") or prev2.endswith("},"):
				i += 1
				continue

		statement = " ".join(l.strip() for l in out[s : i + 1])
		statement = statement.replace("( ", "(").replace(" )", ")")
		if '"' in statement:
			i += 1
			continue
		ind = out[s][: len(out[s]) - len(out[s].lstrip())]

		if len(ind.expandtabs(8)) + len(statement) <= 120:
			out[s : i + 1] = [ind + statement]
			i = s + 1
			continue

		pos = _top_level_assign_pos(statement)
		if pos > 0:
			head = statement[: pos + 1].rstrip()
			rest = statement[pos + 1 :].strip()
			if len(rest) > TINY_TAIL:
				out[s : i + 1] = [f"{ind}{head}", f"{ind}\t{rest}"]
				i = s + 2
				continue
		i += 1
	return out


RE_CASE_STMT = re.compile(r"^(\s*(?:case\b[^:]*|default)\s*:)\s*(\S.*?)\s*$")


def split_case_statements(lines):
	"""case/default 标签后的语句单独一行（default: break; 拆开）。"""
	out = []
	for line in lines:
		m = RE_CASE_STMT.match(line)
		if (
			m
			and not line.rstrip().endswith("\\")
			and not m.group(2).startswith(("{", "case", "default", "/*"))
		):
			ind = line[: len(line) - len(line.lstrip())]
			out.append(m.group(1))
			out.append(f"{ind}\t{m.group(2)}")
		else:
			out.append(line)
	return out


RE_CONTROL_HEAD = re.compile(r"^(\s*(?:\}\s*)?(?:else\s+)?)(if|for|while|switch)(\s*\()")


def split_single_line_controls(lines):
	"""if/for/while/switch 的语句体不与控制行同一行
	（while (x); 空循环、后跟 { 的保持原样；嵌套控制递归拆分）。"""
	out = []
	for line in lines:
		m = RE_CONTROL_HEAD.match(line)
		if m and not line.rstrip().endswith("\\"):
			j = m.end()
			depth = 1
			while j < len(line) and depth:
				if line[j] == "(":
					depth += 1
				elif line[j] == ")":
					depth -= 1
				j += 1
			rest = line[j:].strip()
			if rest and rest != ";" and not rest.startswith("{"):
				ind = line[: len(line) - len(line.lstrip())]
				out.append(line[:j].rstrip())
				out.extend(split_single_line_controls([f"{ind}\t{rest}"]))
				continue
		out.append(line)
	return out


RE_IF_OPEN = re.compile(r"^#(?:if|ifdef|ifndef)\b")
RE_IF_MID = re.compile(r"^#(?:else|elif)\b")
RE_IF_CLOSE = re.compile(r"^#endif\b")


def normalize_pp_gaps(lines):
	"""#if/#ifdef/#ifndef 前空一行，#endif 后空一行；
	与相邻条件指令（嵌套 #if、#else、连续 #endif）之间不加。"""
	out = []
	in_comment = False
	for i, line in enumerate(lines):
		cs = (not in_comment) and bool(RE_COMMENT_START.match(line))
		if RE_IF_OPEN.match(line) and out and out[-1].strip() != "":
			k = len(out) - 1
			while k >= 0 and out[k].strip() == "":
				k -= 1
			if (
				k >= 0
				and not RE_IF_OPEN.match(out[k])
				and not RE_IF_MID.match(out[k])
				and not out[k].lstrip().startswith(("/*", "*"))
				and not out[-1].rstrip().endswith("\\")
			):
				out.append("")
		out.append(line)
		if RE_IF_CLOSE.match(line):
			j = i + 1
			while j < len(lines) and lines[j].strip() == "":
				j += 1
			if (
				j < len(lines)
				and not RE_IF_CLOSE.match(lines[j])
				and not RE_IF_MID.match(lines[j])
				and not lines[j].rstrip().endswith("\\")
			):
				out.append("")
		if cs and "*/" not in line:
			in_comment = True
		elif in_comment and "*/" in line:
			in_comment = False
	return out



def _norm_comment(text: str) -> str:
	"""规范 /*foo*/ 为 /* foo */（多空格压缩为单空格；多行注释、/** 文档注释不动）。"""
	if "\n" in text or text.startswith("/**"):
		return text
	m = re.match(r"^/\*\s*(.*?)\s*\*/$", text, re.S)
	if m and m.group(1):
		return "/* " + re.sub(r"\s+", " ", m.group(1)).strip() + " */"
	return text

def _split_top_commas(text: str):
	"""按顶层逗号切分结构体元素内部字段（花括号/括号/字符串内的逗号不算），
	每个字段内部空白归一化为单空格。"""
	parts, depth_brace, depth_paren, cur = [], 0, 0, ""
	quote = None
	escaped = False
	for ch in text:
		if quote:
			cur += ch
			if ch == quote and not escaped:
				quote = None
			escaped = (ch == "\\" and not escaped)
			continue
		if ch in "\"'":
			quote = ch
			cur += ch
		elif ch == "{":
			depth_brace += 1
			cur += ch
		elif ch == "}":
			depth_brace -= 1
			cur += ch
		elif ch == "(":
			depth_paren += 1
			cur += ch
		elif ch == ")":
			depth_paren -= 1
			cur += ch
		elif ch == "," and depth_brace == 0 and depth_paren == 0:
			parts.append(cur)
			cur = ""
		else:
			cur += ch
	parts.append(cur)
	return [
		re.sub(r"\s+", " ", part).strip() for part in parts if part.strip()
	]


def format_struct_arrays(lines):
	"""结构体数组初始化器：
	- 元素的 { 和 } 各自单独一行（Allman）
	- 每个成员单独占一行（按顶层逗号分割）
	- }, 与下一个元素的 { 之间空一行
	含注释、嵌套深度超过一层、元素不是花括号组的，保持原样。"""
	out = []
	i = 0
	while i < len(lines):
		m = re.match(r"^(\s*.*?=\s*)\{(.*)$", lines[i])
		if not m:
			out.append(lines[i])
			i += 1
			continue
		decl, body = m.group(1), m.group(2)
		decl_braced = False
		ind = decl[: len(decl) - len(decl.lstrip())]

		depth = 1 + body.count("{") - body.count("}")
		j = i + 1
		while depth > 0 and j < len(lines):
			body += "\n" + lines[j]
			depth += lines[j].count("{") - lines[j].count("}")
			j += 1
		if depth != 0 or re.search(r"^\s*#", body, re.M):
			out.append(lines[i])
			i += 1
			continue

		# 解析 {elem}, /* c */ {elem}, ... };
		# 尾随元素的注释归属前一个元素，独占一行的注释归属后一个元素，
		# 元素内部的注释则放弃处理
		elements = []
		pre_comments = []
		pos, ok = 0, True
		text = body
		while True:
			while pos < len(text) and text[pos] in " \t\n,":
				pos += 1
			if pos >= len(text) or text[pos] == "}":
				break
			if text.startswith("/*", pos):
				end = text.find("*/", pos)
				if end < 0:
					ok = False
					break
				line_start = text.rfind("\n", 0, pos) + 1
				if text[line_start:pos].strip() == "":
					pre_comments.append(_norm_comment(text[pos : end + 2]))
				elif elements:
					prefix0, inner0, _, pre0 = elements[-1]
					elements[-1] = (prefix0, inner0, _norm_comment(text[pos : end + 2]), pre0)
				else:
					ok = False
					break
				pos = end + 2
				continue
			prefix = None
			if text[pos] == "[":
				end_b = text.find("]", pos)
				if end_b < 0:
					ok = False
					break
				m_eq = re.match(r"\s*=\s*", text[end_b + 1 :])
				if not m_eq:
					ok = False
					break
				prefix = text[pos : end_b + 1 + m_eq.end()]
				pos = end_b + 1 + m_eq.end()
			if text[pos] != "{":
				ok = False
				break
			d = 1
			start = pos
			pos += 1
			while pos < len(text) and d > 0:
				if text[pos] == "{":
					d += 1
				elif text[pos] == "}":
					d -= 1
				pos += 1
			if d != 0:
				ok = False
				break
			elem = text[start:pos]
			inner = elem[1:-1]
			if "{" in inner:
				ok = False
				break
			# 元素内部只允许完整单行注释，保留在成员文本中
			tmp = inner
			while "/*" in tmp:
				s0 = tmp.find("/*")
				e0 = tmp.find("*/", s0)
				if e0 < 0:
					ok = False
					break
				tmp = tmp[:s0] + tmp[e0 + 2 :]
			if not ok:
				break
			elements.append((prefix, inner, None, pre_comments))
			pre_comments = []
		if pre_comments:
			ok = False
		tail = text[pos:].strip()
		if not ok or not elements or not re.match(r"^\}\s*;?\s*$", tail):
			out.append(lines[i])
			i += 1
			continue

		out.append(decl if decl_braced else f"{decl}{{")
		rendered = []
		for prefix, inner, post_c, pre_cs in elements:
			parts = _split_top_commas(inner)
			has_dot = any(p.lstrip().startswith(".") for p in parts)
			elem_ind = ind + "\t"
			head_prefix = prefix or ""
			# 行尾注释移到元素前一行（与 pre 注释合并）
			if post_c:
				pre_cs = pre_cs + [post_c]
				post_c = None
			if not has_dot:
				flat = f"{head_prefix}{{{', '.join(parts)}}}"
				if len(elem_ind.expandtabs(8)) + len(flat) + 1 <= 120:
					line = f"{elem_ind}{flat},"
					if post_c:
						line += " " + post_c
					rendered.append((False, [line], pre_cs))
					continue
			# 展开形态：{ 单独一行，数字/宏成员打包，. 开头成员各占一行
			elem_lines = [f"{elem_ind}{head_prefix}{{"]
			run = ""
			member_ind = ind + "\t\t"
			member_cols = len(member_ind.expandtabs(8))

			def flush_run():
				nonlocal run
				if run:
					elem_lines.append(f"{member_ind}{run}")
					run = ""

			for k, part in enumerate(parts):
				is_last = k == len(parts) - 1
				if part.lstrip().startswith("."):
					flush_run()
					elem_lines.append(f"{member_ind}{part}{'' if is_last else ','}")
				else:
					piece = part + ("" if is_last else ",")
					if not run:
						run = piece
					elif member_cols + len(run) + 1 + len(piece) <= 120:
						run += " " + piece
					else:
						flush_run()
						run = piece
			flush_run()
			close = f"{elem_ind}}},"
			if post_c:
				close += " " + post_c
			elem_lines.append(close)
			rendered.append((True, elem_lines, pre_cs))

		for idx, (is_exp, elem_lines, pre_cs) in enumerate(rendered):
			for pre_c in pre_cs:
				out.append(f"{ind}\t{pre_c}")
			out.extend(elem_lines)
			if idx != len(rendered) - 1 and (
				is_exp
				or rendered[idx + 1][0]
				or rendered[idx + 1][2]
			):
				out.append("")
		out.append(f"{ind}}};")
		i = j

	return out


RE_TYPE_DEF_INLINE = re.compile(r"^\s*(?:typedef\s+)?(?:struct|enum|union)\b[^;{]*\{")
RE_TYPE_DEF_HDR = re.compile(r"^\s*(?:typedef\s+)?(?:struct|enum|union)(?:\s+\w+)?\s*$")
RE_BLOCK_END = re.compile(r"^\s*(?:\{\s*\})?\s*\}\s*;")


def normalize_typedef_gaps(lines):
	"""struct/enum/union（含 typedef 形式）的定义开始行与前一行代码之间空一行；
	顶层 };（类型/数组定义结束）与下一条顶层声明之间空一行。"""
	out = []
	in_comment = False
	prev_kind = None
	for line in lines:
		cs = (not in_comment) and bool(RE_COMMENT_START.match(line))
		is_top_code = (
			not cs
			and not in_comment
			and line.strip()
			and not line.startswith((" ", "\t"))
			and not line.startswith("#")
			and line.strip() not in ("{", "}")
		)
		if (
			is_top_code
			and out
			and out[-1].strip() != ""
			and RE_BLOCK_END.match(out[-1])
			and not out[-1].rstrip().endswith("\\")
		):
			out.append("")
		if (
			(RE_TYPE_DEF_INLINE.match(line) or RE_TYPE_DEF_HDR.match(line))
			and out
			and out[-1].strip() != ""
			and prev_kind == "code"
			and not out[-1].rstrip().endswith("\\")
		):
			out.append("")
		out.append(line)
		if cs and "*/" not in line:
			in_comment = True
		elif in_comment and "*/" in line:
			in_comment = False
		if line.strip():
			prev_kind = "comment" if (in_comment or cs) else "code"
	return out


def format_designated_inits(lines):
	"""单结构体对象的指定成员初始化器：
	{ 跟声明行，每个 .成员 独占一行，}; 单独一行。
	成员后的行尾注释跟随成员，独占一行的注释与组间空行保留。"""
	out = []
	i = 0
	while i < len(lines):
		m = re.match(r"^(\s*.*?=\s*)\{(.*)$", lines[i])
		if not m:
			out.append(lines[i])
			i += 1
			continue
		decl, body = m.group(1), m.group(2)
		ind = decl[: len(decl) - len(decl.lstrip())]
		depth = 1 + body.count("{") - body.count("}")
		j = i + 1
		while depth > 0 and j < len(lines):
			body += "\n" + lines[j]
			depth += lines[j].count("{") - lines[j].count("}")
			j += 1
		if depth != 0 or re.search(r"^\s*#", body, re.M):
			out.append(lines[i])
			i += 1
			continue
		inner_all, _, tail = body.rpartition("}")
		if re.search(r"\{[ \t\n]*[^\s}]", inner_all) or not re.match(r"^\s*;?\s*$", tail):
			out.append(lines[i])
			i += 1
			continue

		segments = []
		pre = []
		ok = True
		for raw in _split_top_level(inner_all, ","):
			if not raw.strip():
				continue
			s = raw
			pre_cs = []
			blank_before = False
			while True:
				lead = s[: len(s) - len(s.lstrip())]
				if lead.count("\n") >= 2:
					blank_before = True
				s2 = s.lstrip()
				if not s2.startswith("/*"):
					s = s2
					break
				end = s2.find("*/")
				if end < 0:
					ok = False
					break
				comment = s2[: end + 2]
				if "\n" in lead:
					pre_cs.append(comment)
				elif segments:
					segments[-1][1] = comment
				else:
					pre_cs.append(comment)
				s = s2[end + 2 :]
			if not ok:
				break
			part = re.sub(r"\s+", " ", s).strip()
			if part:
				segments.append([part, None, pre_cs, blank_before])
			pre = pre_cs = []
		if (
			not ok
			or not segments
			or not any(
				seg[0].startswith((".", "[")) for seg in segments
			)
		):
			out.append(lines[i])
			i += 1
			continue

		out.append(f"{decl}{{")
		for idx, (part, post_c, pre_cs, blank_before) in enumerate(segments):
			if blank_before:
				out.append("")
			for c in pre_cs:
				out.append(f"{ind}\t{c}")
			line = f"{ind}\t{part}"
			if idx != len(segments) - 1:
				line += ","
			if post_c:
				line += " " + post_c
			out.append(line)
		out.append(f"{ind}}};")
		i = j

	return out


def format_commented_arrays(lines):
	"""带逐元素注释的数组初始化器（函数指针表等）：
	每个元素独占一行；行尾注释移到所注解元素的前一行（注释独占一行），
	注释与前一行代码之间空一行。"""
	out = []
	i = 0
	while i < len(lines):
		m = re.match(r"^(\s*.*?=\s*)\{(.*)$", lines[i])
		if m:
			decl, body = m.group(1), m.group(2)
			decl_braced = False
			# [IDX] = { 指定下标元素属于结构体数组的元素，归 format_struct_arrays
			if decl.strip().startswith("["):
				out.append(lines[i])
				i += 1
				continue
		else:
			m2 = re.match(r"^(\s*)\{(.*)$", lines[i])
			if not m2:
				out.append(lines[i])
				i += 1
				continue
			# 裸 { 仅在初始化语境（前一行是 = { , 或注释）时视为初始化器，
			# 函数/控制块的 {（前一行以 ) 结尾）不处理
			prev = lines[i - 1].strip() if i > 0 else ""
			if not (
				prev.endswith(("=", "{", ","))
				or (
					prev.startswith(("/*", "*"))
					and "(" not in prev
					and ";" not in prev
				)
			):
				out.append(lines[i])
				i += 1
				continue
			decl, body = m2.group(1) + "{", m2.group(2)
			decl_braced = True
		ind = decl[: len(decl) - len(decl.lstrip())]
		depth = 1 + body.count("{") - body.count("}")
		j = i + 1
		while depth > 0 and j < len(lines):
			body += "\n" + lines[j]
			depth += lines[j].count("{") - lines[j].count("}")
			j += 1
		if depth != 0 or re.search(r"^\s*#", body, re.M) or "/*" not in body:
			out.append(lines[i])
			i += 1
			continue
		inner_all, _, tail = body.rpartition("}")
		if re.search(r"\{[ \t\n]*[^\s}]", inner_all) or not re.match(r"^\s*[,;]?\s*$", tail):
			out.append(lines[i])
			i += 1
			continue

		items = []
		pre = []
		ok = True
		for raw in _split_top_level(inner_all, ","):
			if not raw.strip():
				continue
			s = raw
			pre_cs = list(pre)
			pre = []
			while True:
				lead = s[: len(s) - len(s.lstrip())]
				s2 = s.lstrip()
				if not s2.startswith("/*"):
					s = s2
					break
				end = s2.find("*/")
				if end < 0:
					ok = False
					break
				comment = _norm_comment(s2[: end + 2])
				if "\n" in lead:
					pre_cs.append(comment)
				elif items:
					items[-1][1].append(comment)
				else:
					pre_cs.append(comment)
				s = s2[end + 2 :]
			if not ok:
				break
			elem = re.sub(r"\s+", " ", s).strip()
			m2 = re.match(r"^(.*?)\s*(/\*.*\*/)\s*$", elem, re.S)
			if m2 and m2.group(1).strip():
				elem = m2.group(1).strip()
				items.append((elem, pre_cs + [_norm_comment(m2.group(2))]))
				continue
			if m2 and not m2.group(1).strip():
				pre = pre_cs + [_norm_comment(m2.group(2))]
				continue
			if elem:
				items.append((elem, pre_cs))
			elif pre_cs:
				pre = pre_cs
		if not ok or not items:
			out.append(lines[i])
			i += 1
			continue

		out.append(decl if decl_braced else f"{decl}{{")
		for elem, pre_cs in items:
			if pre_cs:
				out.append("")
				for c in pre_cs:
					out.append(f"{ind}\t{c}")
			out.append(f"{ind}\t{elem},")
		out.append(f"{ind}}};")
		i = j

	return out


def post_transform(lines, def_mode=False):
	# 续行符 \ 后面的空行会使宏定义中断，一律删除
	lines = [
		line
		for i, line in enumerate(lines)
		if not (
			line.strip() == ""
			and i > 0
			and lines[i - 1].rstrip().endswith("\\")
		)
	]

	# 空循环体分号并回控制行
	out, i = [], 0
	while i < len(lines):
		m = RE_EMPTY_LOOP.match(lines[i])
		if m and i + 1 < len(lines) and re.match(r"^\s*;\s*$", lines[i + 1]):
			out.append(m.group(1) + ";")
			i += 2
		else:
			out.append(lines[i])
			i += 1
	lines = out

	# } else 前插空行
	out = []
	for line in lines:
		if RE_ELSE.match(line) and out and out[-1].strip():
			out.append("")
		out.append(line)
	lines = out

	lines = normalize_comment_blanks(lines)
	lines = normalize_function_gaps(lines)
	lines = normalize_decl_gaps(lines)
	lines = normalize_statement_gaps(lines)
	lines = format_numeric_arrays(lines)
	lines = format_commented_arrays(lines)
	lines = format_struct_arrays(lines)
	lines = format_designated_inits(lines)
	lines = normalize_typedef_gaps(lines)
	lines = expand_single_line_types(lines)
	lines = join_member_breaks(lines)
	lines = rebalance_tiny_tails(lines)
	lines = split_case_statements(lines)
	lines = split_single_line_controls(lines)
	lines = normalize_pp_gaps(lines)
	if def_mode:
		lines = align_defines_reference_groups(lines)
	else:
		lines = align_defines(lines)
	lines = [RE_WS.sub("", l) for l in lines]
	return lines


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def process(path: Path, style_path: Path):
	lines, encoding = read_lines(path)
	def_mode = is_register_def_file(lines)

	if def_mode:
		lines = merge_multiline_defines(lines)
	lines = pre_transform(lines, def_mode)
	lines = normalize_pp_lines(lines)
	lines = remove_decorative_lines(lines)
	lines = collapse_single_line_block_comments(lines)
	lines = remove_contentless_comments(lines)
	lines = remove_empty_comment_blocks(lines)
	lines = collapse_blanks(lines)
	write_lines(path, lines, encoding)

	if not def_mode:
		run_clang_format(path, style_path)
		lines, encoding = read_lines(path)

	lines = post_transform(lines, def_mode)
	lines = collapse_blanks(lines)
	write_lines(path, lines, encoding)
	print(f"done: {path}{' (register-def)' if def_mode else ''}")


def main():
	ap = argparse.ArgumentParser(description="Linux 内核编码风格批量整理")
	ap.add_argument("files", nargs="+", type=Path)
	args = ap.parse_args()

	with tempfile.NamedTemporaryFile("w", suffix=".clang-format", delete=False) as tf:
		tf.write(CLANG_FORMAT_STYLE)
		style_path = Path(tf.name)

	try:
		for f in args.files:
			if not f.is_file():
				print(f"skip: {f} 不存在", file=sys.stderr)
				continue
			process(f, style_path)
	finally:
		style_path.unlink(missing_ok=True)


if __name__ == "__main__":
	main()
