local function wrap_strategy(orig)
	return {
		on_attach = function(bufnr, settings)
			settings.parser:parse()
			return orig.on_attach(bufnr, settings)
		end,
		on_detach = orig.on_detach,
		on_reset = function(bufnr, settings)
			settings.parser:parse()
			return orig.on_reset(bufnr, settings)
		end,
	}
end

require('rainbow-delimiters.setup').setup {
	strategy = {
		[''] = wrap_strategy(require('rainbow-delimiters.strategy.global')),
		vim = wrap_strategy(require('rainbow-delimiters.strategy.local')),
	},
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
