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
	-- "navarasu/onedark.nvim",
	-- "vim/colorschemes", -- 主题
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
	"shellRaining/hlchunk.nvim",
	"akinsho/toggleterm.nvim",
	"hedyhli/outline.nvim",
	"Mr-LLLLL/cool-chunk.nvim",
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
	"stevearc/oil.nvim",

	"preservim/nerdcommenter",
	"windwp/nvim-autopairs", -- 自动补全括号
	"folke/noice.nvim",
	"rcarriga/nvim-notify",
	"kevinhwang91/nvim-hlslens",
	"karb94/neoscroll.nvim",

	"akinsho/bufferline.nvim", -- buffer分割线
	"lewis6991/gitsigns.nvim", -- 左则git提示
	"MeanderingProgrammer/render-markdown.nvim",
	"3rd/image.nvim",
	"sindrets/diffview.nvim",

	{
		'nvim-telescope/telescope.nvim',
		dependencies = { 'nvim-lua/plenary.nvim' },
	},

	{
		"yetone/avante.nvim",
		dependencies = {
			"nvim-lua/plenary.nvim",
			"MunifTanjim/nui.nvim",
			--- 以下依赖项是可选的，
			"echasnovski/mini.pick", -- 用于文件选择器提供者 mini.pick
			"nvim-telescope/telescope.nvim", -- 用于文件选择器提供者 telescope
			"hrsh7th/nvim-cmp", -- avante 命令和提及的自动完成
			"ibhagwan/fzf-lua", -- 用于文件选择器提供者 fzf
			"nvim-tree/nvim-web-devicons", -- 或 echasnovski/mini.icons
			"HakonHarnes/img-clip.nvim",
		},
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
