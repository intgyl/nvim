local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
	vim.fn.system({
		"git",
		"clone",
		"--filter=blob:none",
		"https://github.com/folke/lazy.nvim.git",
		"--branch=stable", -- latest stable release
		lazypath,
	})
end
vim.opt.rtp:prepend(lazypath)


local plugins = {
	"folke/tokyonight.nvim", -- 主题
	{
		"folke/todo-comments.nvim",
		dependencies = { "nvim-lua/plenary.nvim" },
	},

	"nvim-lualine/lualine.nvim",  -- 状态栏
	"nvim-tree/nvim-tree.lua",  -- 文档树
	"nvim-tree/nvim-web-devicons", -- 文档树图标
	"mikavilpas/yazi.nvim",
	"catgoose/nvim-colorizer.lua",
	'nvim-mini/mini.trailspace',

	"nvim-treesitter/nvim-treesitter", -- 语法高亮
	"HiPhish/rainbow-delimiters.nvim", -- 彩色括号
	'preservim/tagbar',
	-- "shellRaining/hlchunk.nvim",
	"akinsho/toggleterm.nvim",
	"hedyhli/outline.nvim",
	-- "Mr-LLLLL/cool-chunk.nvim",
	"lukas-reineke/indent-blankline.nvim",

	{
		"williamboman/mason.nvim",
		"williamboman/mason-lspconfig.nvim", -- 这个相当于mason.nvim和lspconfig的桥梁
		"neovim/nvim-lspconfig"
	},

	-- 自动补全
	'neovim/nvim-lspconfig',
	'hrsh7th/cmp-nvim-lsp',
	'hrsh7th/cmp-buffer',
	'hrsh7th/cmp-path',
	'hrsh7th/cmp-cmdline',
	'hrsh7th/nvim-cmp',
	'saadparwaiz1/cmp_luasnip',

	"L3MON4D3/LuaSnip",
	"rafamadriz/friendly-snippets",

	"preservim/nerdcommenter",
	"windwp/nvim-autopairs", -- 自动补全括号
	-- "folke/noice.nvim",
	-- "rcarriga/nvim-notify",
	-- "kevinhwang91/nvim-hlslens",
	-- "karb94/neoscroll.nvim",

	-- "akinsho/bufferline.nvim", -- buffer分割线
	"lewis6991/gitsigns.nvim", -- 左则git提示
	"MeanderingProgrammer/render-markdown.nvim",
	"3rd/image.nvim",
	"sindrets/diffview.nvim",
	"HakonHarnes/img-clip.nvim",

	{
		'nvim-telescope/telescope.nvim',
		dependencies = { 'nvim-lua/plenary.nvim' },
	},

	{
		"milanglacier/minuet-ai.nvim",
		dependencies = {
			"nvim-lua/plenary.nvim",
			"hrsh7th/nvim-cmp",
		},
	},

--	"github/copilot.vim",
--	{
--		"CopilotC-Nvim/CopilotChat.nvim",
--		dependencies = {
--			{ "github/copilot.vim" },
--			{ "nvim-lua/plenary.nvim"},
--		},
--	},

	{
		"Exafunction/windsurf.nvim",
		dependencies = {
			"nvim-lua/plenary.nvim",
			"hrsh7th/nvim-cmp",
		},
	},

	"dhananjaylatkar/cscope_maps.nvim"

}

local opts = {
	rocks = {
		hererocks = true,
	},
}

require("lazy").setup(plugins, opts)
