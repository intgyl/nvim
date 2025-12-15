-- 默认不开启nvim-tree
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

require("nvim-tree").setup({
	git = {
		enable = true,
	},
	sort = {
		sorter = "case_sensitive",
	},
	view = {
		side = "right",
		width = 30,
	},
	renderer = {
		group_empty = true,
	},
	filters = {
		dotfiles = true,
	},

	on_attach = function(bufnr)
		local api = require("nvim-tree.api")

		local function opts(desc)
			return {
				desc = "nvim-tree: " .. desc,
				buffer = bufnr,
				noremap = true,
				silent = true,
				nowait = true,
			}
		end

		api.config.mappings.default_on_attach(bufnr)

		vim.keymap.set('n', 'v', api.node.open.horizontal_no_picker, opts('Open: Horizontal Split'))
		vim.keymap.set("n", "s", api.node.open.vertical_no_picker, opts("Open: Vertical Split"))
		vim.keymap.set("n", "<CR>", api.node.open.edit, opts("Open: Vertical Split"))
	end,
})

vim.api.nvim_create_autocmd("BufEnter", {
	group = vim.api.nvim_create_augroup("NvimTreeClose", {clear = true}),
	pattern = "NvimTree_*",
	callback = function()
		local layout = vim.api.nvim_call_function("winlayout", {})
		if layout[1] == "leaf" and vim.api.nvim_buf_get_option(vim.api.nvim_win_get_buf(layout[2]), "filetype") == "NvimTree" and layout[3] == nil then vim.cmd("confirm quit") end
	end
})
