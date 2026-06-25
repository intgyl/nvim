require("tokyonight").setup({
	style = "storm",
	transparent = true,
	on_colors = function(colors)
		colors.hint = colors.orange
		colors.error = "#ff0000"
	end,
	on_highlights = function(highlights, colors)
		-- 传统 highlight groups
		highlights.Function = { fg = colors.blue }
		highlights.Method = { fg = colors.blue }
		highlights.Constructor = { fg = colors.blue }

		-- Treesitter groups
		highlights["@function"] = { fg = colors.blue }
		highlights["@method"] = { fg = colors.blue }
		highlights["@constructor"] = { fg = colors.blue }
		-- highlights["@string"] = { fg = "#e5e5e5" }

		 -- LSP Semantic Token
		highlights["@lsp.type.function"] = { fg = colors.blue }
		highlights["@lsp.typemod.function.defaultLibrary"] = { fg = colors.blue }

		-- 宏定义颜色
		highlights.PreProc = { fg = "#4c82b4" }
		highlights["@lsp.type.macro"] = { fg = colors.cyan }
		highlights["@lsp.type.macro.c"] = { fg = colors.cyan }

		highlights.Comment  = { fg = "#7f7f7f", italic = true }
		highlights.Type     = { fg = colors.green }

		-- 行号
		highlights.LineNr = { fg = colors.fg }

		-- 当前行号
		-- highlights.CursorLineNr = { fg = colors.fg, bold = true }

		-- 取消nvim-tree背景色
		highlights.NvimTreeNormal = { bg = "NONE" }
		highlights.NvimTreeNormalNC = { bg = "NONE" }
		highlights.NvimTreeEndOfBuffer = { bg = "NONE" }

		-- 取消 diffview 文件面板状态/增删数字的背景色
		highlights.DiffviewStatusAdded = { fg = colors.green, bg = "NONE" }
		highlights.DiffviewStatusModified = { fg = colors.yellow, bg = "NONE" }
		highlights.DiffviewStatusDeleted = { fg = colors.red, bg = "NONE" }
		highlights.DiffviewFilePanelInsertions = { fg = colors.green, bg = "NONE" }
		highlights.DiffviewFilePanelDeletions = { fg = colors.red, bg = "NONE" }

		-- 窗口分割线高亮
		highlights.WinSeparator = { fg = "#565f89", bg = "NONE" }
	end,
})

vim.cmd("colorscheme tokyonight")

vim.cmd[[colorscheme tokyonight]]
vim.cmd[[hi Normal guibg=NONE ctermbg=NONE]]
-- vim.cmd[[highlight NonText guibg=NONE ctermbg=NONE]]
-- vim.cmd[[highlight LineNr guibg=NONE ctermbg=NONE]]


vim.api.nvim_set_hl(0, 'MatchParen', { fg = '#ff79c6', bg = 'NONE', bold = true })
