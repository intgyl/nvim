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

		vim.keymap.set('n', 's', api.node.open.horizontal_no_picker, opts('Open: Horizontal Split'))
		vim.keymap.set("n", "v", api.node.open.vertical_no_picker, opts("Open: Vertical Split"))
		vim.keymap.set("n", "<CR>", api.node.open.edit, opts("Open: Vertical Split"))
	end,
})
