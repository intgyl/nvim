local opt = vim.opt

opt.number = true           -- 显示行号
opt.relativenumber = false  -- 相对行号
opt.tabstop = 8             -- Tab 显示宽度
opt.shiftwidth = 8          -- 自动缩进宽度
opt.expandtab = false       -- 将 Tab 转换为空格
opt.autoindent = true       -- 自动缩进
opt.mouse = ''              -- 启用鼠标支持
opt.ignorecase = true       -- 搜索忽略大小写
opt.smartcase = true        -- 智能大小写搜索
opt.termguicolors = true    -- 启用真彩色
opt.cursorline = true       -- 光标行
opt.wrap = true             -- 自动换行
opt.swapfile = false
opt.laststatus = 3
opt.scrolloff = 10

vim.g.c_syntax_for_h = 1

-- 默认新窗口右和下
opt.splitright = true
opt.splitbelow = true
opt.updatetime = 500

local is_ssh = os.getenv("SSH_TTY") ~= nil

if not is_ssh then
	vim.opt.clipboard = "unnamedplus"
else
	local augroup = vim.api.nvim_create_augroup("SSH_OSC52_YANK", { clear = true })
	vim.api.nvim_create_autocmd("TextYankPost", {
		group = augroup,
		pattern = "*",
		callback = function()
			local evt = vim.v.event
			if evt.operator == "y" and evt.regname ~= "_" then
				local text = vim.fn.getreg(evt.regname)
				local b64 = vim.base64.encode(text)
				-- OSC52 序列输出到终端
				io.write(string.format("\027]52;c;%s\027\\", b64))
				io.flush()
			end
		end,
	})
end

-- 记录上次退出时的位置
vim.api.nvim_create_autocmd("BufReadPost", {
	callback = function()
		local mark = vim.api.nvim_buf_get_mark(0, '"')
		local lcount = vim.api.nvim_buf_line_count(0)
		if mark[1] > 0 and mark[1] <= lcount then
			pcall(vim.api.nvim_win_set_cursor, 0, mark)
		end
	end
})

vim.keymap.set("n", "<leader>w", function()
	vim.wo.wrap = not vim.wo.wrap
	print("wrap: " .. tostring(vim.wo.wrap))
end, { desc = "Toggle line wrap" })

vim.api.nvim_create_autocmd({"BufNewFile", "BufRead"}, {
	pattern = "SConscript",
	callback = function()
		vim.opt_local.filetype = "python"
	end,
})

vim.api.nvim_create_autocmd("FileType", {
	command = "set formatoptions-=o",
})

