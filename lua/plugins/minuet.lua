vim.api.nvim_set_hl(0, "MinuetVirtualText", { fg = "#6c7086", italic = true, default = true })

-- 使用 minuet 官方配置
require('minuet').setup {
	provider = 'openai_fim_compatible',
	n_completions = 1,
	context_window = 512,
	provider_options = {
		openai_fim_compatible = {
			api_key = 'TERM',
			name = 'Ollama',
			end_point = (vim.env.OLLAMA_HOST or 'http://localhost:11434') .. '/v1/completions',
			model = 'qwen2.5-coder:7b',
			optional = {
				max_tokens = 30,
				top_p = 0.9,
				stop = { '\n' },
			},
		},
	},
	virtualtext = {
		enabled = true,
		auto_trigger_ft = {'*'},
		keymap = {
			-- accept = '<Tab>',
			accept_line = '<Tab>',
			-- dismiss = '<A-e>',
		},
	},
	request_timeout = 60000,
	throttle = 1000,
	debounce = 500,
}
