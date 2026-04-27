require('yazi').setup({
	open_for_directories = true,
	yazi_cmd = "yazi",
	open_multiple_tabs = false,
	floating_window_scaling_factor = 0.9,
	yazi_floating_window_border = "rounded",
	auto_close = true,
	keymaps = {
		show_help = "<f1>",
		open_file_in_vertical_split = "<c-v>",
		open_file_in_horizontal_split = "<c-x>",
		open_file_in_tab = "<c-t>",
		grep_in_directory = "<c-s>",
		replace_in_directory = "<c-g>",
		cycle_open_buffers = "<tab>",
		copy_relative_path_to_selected_files = "<c-y>",
		send_to_quickfix_list = "<c-q>",
		change_working_directory = "<c-\\>",
	},

	integrations = {
		grep_in_directory = "ripgrep",
		grep_in_selected_files = "ripgrep",
	},

	yazi_floating_window_winblend = 0,
	log_level = vim.log.levels.OFF,
})

vim.keymap.set("n", "<leader>e", "<cmd>Yazi<cr>", { desc = "Open Yazi" })
