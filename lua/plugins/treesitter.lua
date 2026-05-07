require("nvim-treesitter").setup({
	-- 添加不同语言
	ensure_installed = { "vim", "vimdoc", "bash", "c", "cpp", "java", "javascript", "json", "lua", "python", "typescript", "tsx", "css", "rust", "markdown", "markdown_inline", "verilog", "comment", "diff", "toml", "yaml", "html", "printf", "regex", "latex" },

	highlight = {
		enable = true,
		-- 禁用 markdown 的 treesitter 高亮，避免与 render-markdown 冲突
		disable = { "markdown" },
	},
	indent = {
		enable = true,
		disable = { "c", "cpp", "verilog" },
	},
})

