vim.opt.termguicolors = true

require("bufferline").setup {
	options = {
		-- 使用 nvim 内置lsp
		diagnostics = "nvim_lsp",
		-- 左侧让出 nvim-tree 的位置
		offsets = {{
			filetype = "NvimTree",
			text = "File Explorer",
			highlight = "Directory",
			text_align = "left"
		}},
		numbers = "ordinal",
	}
}

local function toggle_bufferline()
	local buffers = vim.fn.getbufinfo({buflisted = 1})
	if #buffers > 1 then
		vim.o.showtabline = 2
	else
		vim.o.showtabline = 0
	end
end

vim.api.nvim_create_autocmd(
	{"BufAdd", "BufDelete", "BufEnter", "BufWinEnter", "BufWinLeave"},
	{
		callback = toggle_bufferline
	}
)

for i = 1,9 do
	vim.api.nvim_set_keymap('n', '<leader>'..i, ':BufferLineGoToBuffer '..i..'<CR>', { noremap = true, silent = true })
end

toggle_bufferline()
