require('avante').setup ({
	provider = "kimi-cli",
	mappings = {
		submit = {
			normal = "<C-CR>",
			insert = "<C-CR>",
		},

		sidebar = {
			apply_all = "A",
			apply_cursor = "a",
			retry_user_request = "r",
			edit_user_request = "e",
			switch_windows = "<C-j>",
			reverse_switch_windows = "<C-k>",
			remove_file = "d",
			add_file = "@",
			-- 取消 ESC 关闭窗口，只保留 q
			close = "q",
			close_from_input = nil,
		},
	},
	acp_providers = {
		["kimi-cli"] = {
			command = "kimi",
			args = { "acp" },
		},
	},

	-- 自动滚动到最新消息
	auto_scroll = true,

	windows = {
		---@type "right" | "left" | "top" | "bottom"
		position = "right", -- the position of the sidebar
		wrap = true, -- similar to vim.o.wrap
		width = 50, -- default % based on available width
		sidebar_header = {
			enabled = true, -- true, false to enable/disable the header
			align = "center", -- left, center, right for title
			rounded = true,
		},
		spinner = {
			editing = { "⡀", "⠄", "⠂", "⠁", "⠈", "⠐", "⠠", "⢀", "⣀", "⢄", "⢂", "⢁", "⢈", "⢐", "⢠", "⣠", "⢤", "⢢", "⢡", "⢨", "⢰", "⣰", "⢴", "⢲", "⢱", "⢸", "⣸", "⢼", "⢺", "⢹", "⣹", "⢽", "⢻", "⣻", "⢿", "⣿" },
			generating = { "·", "✢", "✳", "∗", "✻", "✽" }, -- Spinner characters for the 'generating' state
			thinking = { "🤯", "🙄" }, -- Spinner characters for the 'thinking' state
		},
		input = {
			prefix = "> ",
			height = 8, -- Height of the input window in vertical layout
		},
		edit = {
			border = "rounded",
			start_insert = true, -- Start insert mode when opening the edit window
		},
		ask = {
			floating = false, -- Open the 'AvanteAsk' prompt in a floating window
			start_insert = true, -- Start insert mode when opening the ask window
			border = "rounded",
			---@type "ours" | "theirs"
			focus_on_apply = "ours", -- which diff to focus after applying
		},
	},
})
