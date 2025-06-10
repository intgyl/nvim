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
	end,
})

vim.cmd("colorscheme tokyonight")

vim.cmd[[colorscheme tokyonight]]
vim.cmd[[hi Normal guibg=NONE ctermbg=NONE]]
-- vim.cmd[[highlight NonText guibg=NONE ctermbg=NONE]]
-- vim.cmd[[highlight LineNr guibg=NONE ctermbg=NONE]]


-- 高亮显示行尾空格
vim.cmd([[highlight ExtraWhitespace ctermbg=lightred guibg=#FF7777]])

local function highlight_trailing_whitespace()
	vim.cmd([[match ExtraWhitespace /\s\+$/]])
end

-- 自动在进入 buffer 和离开插入模式时设置高亮
vim.api.nvim_create_autocmd({ "BufEnter", "InsertLeave" }, {
	callback = highlight_trailing_whitespace,
})

vim.api.nvim_set_hl(0, 'MatchParen', { fg = '#ff79c6', bg = 'NONE', bold = true })
