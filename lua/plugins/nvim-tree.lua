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

		-- 自定义 vertical split 打开文件
		vim.keymap.set("n", "v", function()
			local node = api.tree.get_node_under_cursor()
			if not node then return end

			if node.type == "file" then
				api.tree.close()
				vim.cmd("vsplit " .. vim.fn.fnameescape(node.absolute_path))
				api.tree.open()
			end
		end, opts("Open: Vertical Split"))

		-- 自定义 horizontal split 打开文件
		vim.keymap.set("n", "s", function()
			local node = api.tree.get_node_under_cursor()
			if not node then return end

			if node.type == "file" then
				api.tree.close()
				vim.cmd("split " .. vim.fn.fnameescape(node.absolute_path))
				api.tree.open()
			end
		end, opts("Open: Horizontal Split"))

	end,
})
