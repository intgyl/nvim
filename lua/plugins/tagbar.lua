-- tagbar
if vim.fn.has('win32') == 1 or vim.fn.has('win64') == 1 then
	vim.opt.shell = 'cmd.exe'
	vim.opt.shellcmdflag = '/c'
	vim.opt.shellquote = '"'
	vim.opt.shellxquote = ''
	vim.g.tagbar_ctags_bin = 'C:\\Windows\\System32\\ctags.exe'
end

vim.cmd([[
	autocmd FileType * if &filetype !=# 'go' | let g:tagbar_width = 35 | let g:tagbar_left = 1 | endif

	if !exists('g:tagbar_keymap_set')
		let g:tagbar_keymap_set = 1
		nnoremap <silent> <F2> :TagbarToggle<CR>
	endif

	autocmd VimEnter * if &filetype !=# 'go' | call tagbar#autoopen(1) | endif
]])

vim.cmd([[let g:tagbar_silent = 1]])
