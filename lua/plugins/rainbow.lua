local max_lines = 50000

local function wrap_strategy(orig)
	return {
		on_attach = function(bufnr, settings)
			settings.parser:parse()
			return orig.on_attach(bufnr, settings)
		end,
		on_detach = orig.on_detach,
		on_reset = orig.on_reset,
	}
end

require('rainbow-delimiters.setup').setup {
	strategy = {
		[''] = wrap_strategy(require('rainbow-delimiters.strategy.global')),
		vim = wrap_strategy(require('rainbow-delimiters.strategy.local')),
	},
	condition = function(bufnr)
		return vim.api.nvim_buf_line_count(bufnr) <= max_lines
	end,
	query = {
		[''] = 'rainbow-delimiters',
		latex = 'rainbow-blocks',
	},
	highlight = {
		'RainbowDelimiterRed',
		'RainbowDelimiterYellow',
		'RainbowDelimiterBlue',
		'RainbowDelimiterOrange',
		'RainbowDelimiterGreen',
		'RainbowDelimiterViolet',
		'RainbowDelimiterCyan',
	},
}
