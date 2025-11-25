require('hlslens').setup({
	override_lens = function(render, posList, nearest, idx, relIdx)

		local lnum, col = unpack(posList[idx])
		local cnt = #posList

		local text = ('[%d/%d]'):format(idx, cnt)
		local chunks

		if nearest then
			chunks = { { ' ' }, { text, 'HlSearchLensNear' } }
		else
			chunks = { { ' ' }, { text, 'HlSearchLens' } }
		end

		render.setVirt(0, lnum - 1, col - 1, chunks, nearest)
	end,
})
local kopts = {noremap = true, silent = true}

vim.api.nvim_set_keymap('n', 'n',
	[[<Cmd>execute('normal! ' . v:count1 . 'n')<CR><Cmd>lua require('hlslens').start()<CR>]], kopts)
vim.api.nvim_set_keymap('n', 'N',
    [[<Cmd>execute('normal! ' . v:count1 . 'N')<CR><Cmd>lua require('hlslens').start()<CR>]], kopts)
vim.api.nvim_set_keymap('n', '*', [[*<Cmd>lua require('hlslens').start()<CR>]], kopts)
vim.api.nvim_set_keymap('n', ';', [[*<Cmd>lua require('hlslens').start()<CR>]], kopts)
vim.api.nvim_set_keymap('n', '#', [[#<Cmd>lua require('hlslens').start()<CR>]], kopts)
vim.api.nvim_set_keymap('n', '<Leader>l', '<Cmd>noh<CR>', kopts)

