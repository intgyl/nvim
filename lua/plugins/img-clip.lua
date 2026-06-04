require('img-clip').setup({
	default = {
		embed_image_as_base64 = false,
		prompt_for_file_name = true,
		file_name = "%Y-%m-%d-%H-%M-%S",
		-- SSH 环境下使用绝对路径
		use_absolute_path = true,
		relative_to_current_file = false,
		drag_and_drop = {
			insert_mode = true,
		},
		-- 自定义粘贴逻辑，支持 SSH 环境
		process_cmd = "convert - -quality 85 png:-",
	},
	filetypes = {
		markdown = {
			url_encode_path = true,
			template = "![$CURSOR]($FILE_PATH)",
		},
		avante = {
			url_encode_path = true,
			template = "[$CURSOR]($FILE_PATH)",
			prompt_for_file_name = false,
		},
	},
})
