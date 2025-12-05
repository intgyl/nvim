local highlight = {
    "RainbowRed",
    "RainbowYellow",
    "RainbowBlue",
    "RainbowOrange",
    "RainbowGreen",
    "RainbowViolet",
    "RainbowCyan",
}

local hooks = require "ibl.hooks"
-- create the highlight groups in the highlight setup hook, so they are reset
-- every time the colorscheme changes
hooks.register(hooks.type.HIGHLIGHT_SETUP, function()
    vim.api.nvim_set_hl(0, "RainbowRed", { fg = "#6f3f3f" })
    vim.api.nvim_set_hl(0, "RainbowYellow", { fg = "#7a7345" })
    vim.api.nvim_set_hl(0, "RainbowBlue", { fg = "#5f7358" })
    vim.api.nvim_set_hl(0, "RainbowOrange", { fg = "#456f73" })
    vim.api.nvim_set_hl(0, "RainbowGreen", { fg = "#45637a" })
    vim.api.nvim_set_hl(0, "RainbowViolet", { fg = "#6a4f73" })
    vim.api.nvim_set_hl(0, "RainbowCyan", { fg = "#56B6C2" })
end)

require("ibl").setup ({
	indent = {
		highlight = highlight,
		char = "┊",

	},

	scope = {
		show_start = false,
		show_end = false,
	},
})
