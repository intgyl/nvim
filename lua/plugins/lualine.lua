require('lualine').setup({
	sections = {
		lualine_a = {
			{
				"mode",
				color = { fg = "#1f2335", bg = "#7aa2f7" },
				separator = { right = "" },
			},

			{
				'filesize',
				color = { fg = "#1f2335", bg = "#7dcfff" },
				separator = { right = "" },
			},

		},

		lualine_b = {
			{
				"diff",
				symbols = {
					added    = " ",
					modified = " ",
					removed  = " ",
				},
				separator = { right = "" },
			},

			{
				"branch",
				icon = "",
				color = { fg = "#1f2335", bg = "#9ece6a" },
				separator = { right = "" },
			},

			{
				"searchcount",
				color = { fg = "#1f2335", bg = "#e0af68" },
				separator = { right = "" },
			},

		},

		lualine_c = {
			{
				'filename', path = 3,
				color = { fg = "#c0caf5", bg = "#3b4261" },
			},

		},

		lualine_x = {
			-- gitblame,
			{
				"encoding",
				color = { fg = "#c0caf5", bg = "#414868" },
				separator = { left = "" },
			},
			{
				"fileformat",
				color = { fg = "#c0caf5", bg = "#414868" },
			},
			{
				"filetype",
				color = { fg = "#c0caf5", bg = "#414868" },
			},
		},

		lualine_y = {
			{
				"progress",
				color = { fg = "#1f2335", bg = "#e0af68" },
			},
		},

		lualine_z = {
			{
				"location",
				color = { fg = "#c0caf5", bg = "#3b4261" },
			},
		},
	},

})
