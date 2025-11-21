require("mason").setup({
	ui = {
		icons = {
			package_installed = "✓",
			package_pending = "➜",
			package_uninstalled = "✗"
		}
	}
})

require("mason-lspconfig").setup({
	-- 确保安装，根据需要填写
	ensure_installed = {
		"lua_ls",
		"pyright",
		"clangd",
		"bashls",
		"jdtls",
	},
})

vim.lsp.enable('pyls')
vim.lsp.enable('clangd')
vim.lsp.enable('lua_ls')
vim.lsp.enable('jdtls')
