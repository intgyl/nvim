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
		local ok, parsers = pcall(require, "nvim-treesitter.parsers")
		if not ok then
			return    -- Treesitter 未加载
		end

		local configs = parsers.get_parser_configs()
		if not configs[ft] then
			return    -- Treesitter 没有该语言的 parser
		end

		vim.defer_fn(function()
			vim.cmd("silent! Outline!")
		end, 10)
	end,
})

vim.api.nvim_create_autocmd("BufEnter", {
	callback = function()
		local function count_normal_windows()
			local count = 0
			for _, win in ipairs(vim.api.nvim_list_wins()) do
				local config = vim.api.nvim_win_get_config(win)
				if config.relative == "" then -- Non-floating windows
					count = count + 1
				end
			end
			return count
		end

		if vim.bo.filetype == "Outline" and count_normal_windows() == 1 then
			vim.cmd "q"
		end
	end,
})

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

