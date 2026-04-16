local highlightLines = {
	"RainbowYellow",
	"RainbowBlue",
	"RainbowOrange",
	"RainbowGreen",
	"RainbowViolet",
	"RainbowCyan",
	"RainbowRed",

}
local highlightDimLines = {
	"RainbowYellow",
	"RainbowBlue",
	"RainbowOrange",
	"RainbowGreen",
	"RainbowViolet",
	"RainbowCyan",
	"RainbowRed",
}

local hooks = require 'ibl.hooks'

hooks.register(hooks.type.HIGHLIGHT_SETUP, function()
	vim.api.nvim_set_hl(0, "RainbowYellow", { fg = "#7a7345" })
	vim.api.nvim_set_hl(0, "RainbowBlue", { fg = "#5f7358" })
	vim.api.nvim_set_hl(0, "RainbowOrange", { fg = "#456f73" })
	vim.api.nvim_set_hl(0, "RainbowGreen", { fg = "#45637a" })
	vim.api.nvim_set_hl(0, "RainbowViolet", { fg = "#6a4f73" })
	vim.api.nvim_set_hl(0, "RainbowCyan", { fg = "#56B6C2" })
	vim.api.nvim_set_hl(0, "RainbowRed", { fg = "#6f3f3f" })
end)

require('ibl').setup ({
	indent = {
		highlight = highlightDimLines,
		char = '╎',
		tab_char = '┊',
	},
	scope = {
		highlight = highlightLines,
		char = '▏',

		show_start = true,
		show_end = false,
	}
})

vim.g.plugin_visible = true

vim.keymap.set("n", "<F10>", function()
	local ok, gitsigns = pcall(require, "gitsigns")
	if not ok then
		vim.notify("gitsigns.nvim is not loaded", vim.log.levels.ERROR)
		return
	end

	if vim.g.plugin_visible then
		vim.cmd("IBLDisable")
		gitsigns.toggle_current_line_blame(false)
		vim.g.plugin_visible = false
		vim.notify("Disable indent-blankline gitsigns")
	else
		vim.cmd("IBLEnable")
		gitsigns.toggle_current_line_blame(true)
		vim.g.plugin_visible = true
		vim.notify("Enable indent-blankline gitsigns")
	end
end, { desc = "Toggle HLChunk & Gitsigns", silent = true })

