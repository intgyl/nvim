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

vim.lsp.enable('pylsp')
vim.lsp.enable('lua_ls')
vim.lsp.enable('jdtls')
vim.lsp.enable('verible')

vim.lsp.config.clangd = {
	cmd = {
		'clangd',
		'--clang-tidy',
		'--background-index',
		'--offset-encoding=utf-8',

		"--completion-style=detailed",
		"--header-insertion=never",
		"--header-insertion-decorators=0",
		"--cross-file-rename",
		"--fallback-style=llvm",
	},

	root_markers = {
		"compile_commands.json",
		"compile_flags.txt",
		"configure.ac", -- AutoTools
		"Makefile",
		"configure.ac",
		"configure.in",
		"config.h.in",
		"meson.build",
		"meson_options.txt",
		"build.ninja",
		".git",
	},

	capabilities = {
		offsetEncoding = { "utf-8" },
	},

}
