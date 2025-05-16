require("render-markdown").setup({
	-- 配置项可选，下面是默认配置
	style = {
		heading = {
			highlights = { "Title" },
		},
		code = {
			highlights = { "markdownCode" },
		},
		quote = {
			highlights = { "Comment" },
		},
		bullet = {
			-- "*" 或 "-" 等符号的高亮
			highlights = { "SpecialChar" },
		},
	},
})
