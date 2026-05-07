require("render-markdown").setup({
	-- 支持 markdown 和 Avante 文件类型
	file_types = { "markdown", "Avante" },

	-- 标题样式配置
	heading = {
		enabled = true,
		sign = false,
		icons = { "# ", "## ", "### ", "#### ", "##### ", "###### " },
		foregrounds = {
			"@markup.heading.1.markdown",
			"@markup.heading.2.markdown",
			"@markup.heading.3.markdown",
			"@markup.heading.4.markdown",
			"@markup.heading.5.markdown",
			"@markup.heading.6.markdown",
		},
	},

	-- 代码块样式配置
	code = {
		enabled = true,
		sign = false,
		style = "full",
		position = "left",
		language_pad = 0,
		language_name = true,
		disable_background = false,
		width = "full",
		left_pad = 0,
		right_pad = 0,
		min_width = 0,
		border = "thin",
		above = "▄",
		below = "▀",
		highlight = "RenderMarkdownCode",
		highlight_inline = "RenderMarkdownCodeInline",
	},

	-- 引用块样式配置
	quote = {
		enabled = true,
		icon = "▋",
		repeat_linebreak = false,
		highlight = "RenderMarkdownQuote",
	},

	-- 列表符号样式配置
	bullet = {
		enabled = true,
		icons = { "●", "○", "◆", "◇" },
		highlight = "RenderMarkdownBullet",
	},

	-- 复选框样式配置
	checkbox = {
		enabled = true,
		unchecked = {
			icon = "✘ ",
			highlight = "RenderMarkdownUnchecked",
		},
		checked = {
			icon = "✔ ",
			highlight = "RenderMarkdownChecked",
		},
	},

	-- 分隔线样式配置
	dash = {
		enabled = true,
		icon = "─",
		width = "full",
		highlight = "RenderMarkdownDash",
	},


	-- 链接样式配置
	link = {
		enabled = true,
		image = "🖼 ",
		hyperlink = "🔗 ",
		highlight = "RenderMarkdownLink",
	},

	-- 管道表格样式配置
	pipe_table = {
		enabled = true,
		preset = "none",
		style = "full",
		cell = "padded",
		alignment_indicator = "none",
		border = {
			"┌", "┬", "┐",
			"├", "┼", "┤",
			"└", "┴", "┘",
			"│", "─",
		},
		head = "RenderMarkdownTableHead",
		row = "RenderMarkdownTableRow",
	},

	-- LaTeX 数学公式样式配置
	latex = {
		enabled = true,
		render_modes = true,
		highlight = "RenderMarkdownMath",
		top_pad = 0,
		bottom_pad = 0,
	},
})
