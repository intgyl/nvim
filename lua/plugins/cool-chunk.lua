require("cool-chunk").setup({
	chunk = {
		enable = true,
		notify = false,
		use_treesitter = true,
		chars = {
			horizontal_line = "─",
			vertical_line = "│",
			left_top = "╭",
			left_bottom = "╰",
			bottom_arrow = "▼",
			right_arrow = "▶",
		},
		style = {
			{ fg = "#D19A66" }, -- 更改为你喜欢的颜色
		},
		support_filetypes = { "*" }, -- 作用于所有文件类型
	},

	blank = {
		enable = false,
	},
	line_num = {
		enable = true,
	},

    })

vim.g.plugin_visible = true

vim.keymap.set("n", "<F7>", function()
	local ok, gitsigns = pcall(require, "gitsigns")
	if not ok then
		vim.notify("gitsigns.nvim is not loaded", vim.log.levels.ERROR)
		return
	end

	if vim.g.plugin_visible then
		vim.cmd("IBLDisable")
		vim.cmd("DisableCC")
		gitsigns.toggle_current_line_blame(false)
		vim.g.plugin_visible = false
		vim.notify("Disable cool-chunk indent-blankline gitsigns")
	else
		vim.cmd("IBLEnable")
		vim.cmd("EnableCC")
		gitsigns.toggle_current_line_blame(true)
		vim.g.plugin_visible = true
		vim.notify("Enable cool-chunk indent-blankline gitsigns")
	end
end, { desc = "Toggle HLChunk & Gitsigns", silent = true })
