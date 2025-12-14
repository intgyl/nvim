require('lualine').setup({
	sections ={
		lualine_c = {
			{'filename', path = 3},
		},

		lualine_a = {
			{
				'filesize',
			},

			{
				'searchcount',
				maxcount = 999,
				timeout = 500,
			},
		},
	}
})
