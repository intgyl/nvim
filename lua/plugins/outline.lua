require("outline").setup({
	outline_window = {
		position = "left",
		width = 15,
	},

	preview_window = {
		auto_preview = true,
	},
})

vim.api.nvim_create_autocmd("VimEnter", {
	callback = function(args)
		local ft = vim.bo[args.buf].filetype

		-- 跳过不需要的 filetype
		local ignore = { "NvimTree", "TelescopePrompt", "help", "lazy", "terminal", "Outline" }
		if vim.tbl_contains(ignore, ft) then
			return
		end

		-- 检查 Treesitter 是否支持该 filetype
		local has_lang, _ = pcall(vim.treesitter.language.inspect, ft)
		if not has_lang then
			return    -- Treesitter 没有该语言的 parser
		end

		vim.defer_fn(function()
			vim.cmd("silent! Outline!")
		end, 10)
	end,
})

local function outline_exit(cmd)
	local normal_win_count = 0
	local outline_open = false

	for _, win in ipairs(vim.api.nvim_list_wins()) do
		local buf = vim.api.nvim_win_get_buf(win)
		local bt = vim.bo[buf].buftype
		local ft = vim.bo[buf].filetype

		if ft == "Outline" then
			outline_open = true
		elseif bt == "" then
			normal_win_count = normal_win_count + 1
		end
	end

	if normal_win_count == 1 and outline_open then
		pcall(vim.cmd, "OutlineClose")
	end

	if cmd == "q" then
		vim.cmd("q")

	elseif cmd == "wq" then
		vim.cmd("wq")
	end
end

vim.keymap.set("n", "q", function() outline_exit("q") end, { desc = "Quit buffer (close outline first if last file)" })
vim.keymap.set("n", "wq", function() outline_exit("wq") end, { desc = "Save and quit buffer (close outline first if last file)" })


_G.outline_safe_quit = function(cmd)
	local normal_win_count = 0
	local outline_open = false

	for _, win in ipairs(vim.api.nvim_list_wins()) do
		local buf = vim.api.nvim_win_get_buf(win)
		local bt = vim.bo[buf].buftype
		local ft = vim.bo[buf].filetype

		if ft:lower() == "outline" then
			outline_open = true
		elseif bt == "" then
			normal_win_count = normal_win_count + 1
		end
	end

	if normal_win_count == 1 and outline_open then
		pcall(vim.cmd, "OutlineClose")
	end

	if cmd == "q" then
		vim.cmd("q")

	elseif cmd == "q!" then
		vim.cmd("q!")

	elseif cmd == "wq" then
		vim.cmd("wq")

	elseif cmd == "wq!" then
		vim.cmd("wq!")
	end

end

vim.keymap.set("c", "<CR>", function()
	local cmd = vim.fn.getcmdline()
	local cmdtype = vim.fn.getcmdtype()

	if cmdtype == ":" then
		if cmd == "q" then
			return "<C-c>:lua outline_safe_quit('q')<CR>"

		elseif cmd == "q!" then
			return "<C-c>:lua outline_safe_quit('q!')<CR>"

		elseif cmd == "wq" then
			return "<C-c>:lua outline_safe_quit('wq')<CR>"

		elseif cmd == "wq!" then
			return "<C-c>:lua outline_safe_quit('wq!')<CR>"
		end
	end

	return "<CR>"
end, { expr = true })

-- Toggle Outline: F2
vim.keymap.set("n", "<F2>", function()
	local wins = vim.api.nvim_tabpage_list_wins(0)
	for _, win in ipairs(wins) do
		local buf = vim.api.nvim_win_get_buf(win)
		local bt = vim.bo[buf].buftype
		local ft = vim.bo[buf].filetype
		-- Outline 已打开，则关闭它
		if bt == "nofile" and ft == "Outline" then
			vim.cmd("OutlineClose")
			return
		end
	end
	-- 否则打开 Outline
	vim.cmd("Outline!")
end, {desc = "Toggle Outline" })
