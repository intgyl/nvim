local lspconfig = require('lspconfig')

lspconfig.clangd.setup {
	cmd = {
		"clangd",
		"--background-index",
		"--clang-tidy",
		"--completion-style=detailed",
		"--header-insertion=iwyu",
		"--cross-file-rename",
	},
	on_attach = function(client, bufnr)
		local opts = { noremap = true, silent = true, buffer = bufnr }

		-- 使用 telescope 进行异步跳转
		vim.keymap.set('n', '<C-k>', require('telescope.builtin').lsp_definitions, opts)

		-- 快速跳回原处
		-- vim.keymap.set('n', '<C-t>', '<C-o>', opts)
	end,
}

local jump_stack = {}

local function push_jump()
	table.insert(jump_stack, {
		bufnr = vim.api.nvim_get_current_buf(),
		pos = vim.api.nvim_win_get_cursor(0),
	})
end

local function smart_jump_back()
	if #jump_stack == 0 then
		print("No more jumps recorded")
		return
	end

	local jump = table.remove(jump_stack)
	if not vim.api.nvim_buf_is_loaded(jump.bufnr) then
		vim.cmd("edit " .. vim.api.nvim_buf_get_name(jump.bufnr))
	else
		vim.api.nvim_set_current_buf(jump.bufnr)
	end
	vim.api.nvim_win_set_cursor(0, jump.pos)
end
