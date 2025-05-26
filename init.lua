vim.g.tagbar_left = 1
vim.g.mapleader = ","
vim.g.maplocalleader = ","
vim.opt.termguicolors = true

local largefile = require("core.largefile")
largefile.check_argv()

require("plugins.plugins-setup")

require("core.options")
require("core.keymaps")

-- 插件
require("plugins.lualine")
require("plugins/nvim-tree")
require("plugins/treesitter")
require("plugins/lsp")
require("plugins/nvim-cmp")
-- require("plugins/comment")
require("plugins/autopairs")
-- require("plugins/bufferline")
require("plugins/gitsigns")
require("plugins/oil")
require("plugins/telescope")
require("plugins/lsp-clangd")
require("plugins/luasnip")
require("plugins/colorscheme")
require("plugins/toggleterm")
require("plugins/nerdcommenter")
require("plugins/copilot-chat")
require("plugins/astyle")
require("plugins/markdown")
--require("plugins/gtags_telscope")

if not vim.g.is_large_file then
	require("plugins/hlchunk")
end
