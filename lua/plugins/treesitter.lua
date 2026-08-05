require("nvim-treesitter").setup()

vim.treesitter.language.register("systemverilog", { "verilog" })

local parsers = {
	"vim", "vimdoc", "bash", "c", "cpp", "java", "javascript", "json", "lua",
	"python", "typescript", "tsx", "css", "rust", "markdown", "markdown_inline",
	"systemverilog", "comment", "diff", "toml", "yaml", "html", "printf", "regex", "latex",
}
require("nvim-treesitter").install(parsers)

vim.api.nvim_create_autocmd("FileType", {
	callback = function(args)
		if args.match == "markdown" then
			vim.treesitter.stop(args.buf)
		else
			pcall(vim.treesitter.start, args.buf)
		end
	end,
})
