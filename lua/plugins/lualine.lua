require('lualine').setup({
	sections ={
		lualine_c = {
			{'filename', path = 3},
		},

		lualine_a = {
			{
				'searchcount',
				maxcount = 999,
				timeout = 500,
			}
		}
	}
})
