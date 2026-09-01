vim.api.nvim_create_autocmd({ "BufRead", "BufNewFile" }, {
	pattern = { "*.c", "*.cc", "*.cpp", "*.h", "*.hpp", "*.v" },
	callback = function()
		vim.keymap.set("n", "<F4>", function()
			local filepath = vim.fn.expand("%:p")
			vim.cmd("write")

			local ext = vim.fn.expand("%:e") -- 获取文件扩展名（不带 .）
			if ext == "v" then
				-- Verilog 使用 verible-verilog-format
				vim.fn.system({ "verible-verilog-format", "--inplace", "--column_limit=300",
					"--indentation_spaces=4", "--assignment_statement_alignment=align",
					"--named_port_alignment=align","--port_declarations_alignment=align",
					"--module_net_variable_alignment=align",
					filepath
				})
			else
				local clang_format_style = "file:" .. vim.fn.expand("$HOME") .. "/.clang-format"
				vim.fn.system({ "clang-format", "-style=" .. clang_format_style, "-i", filepath })
				local uncrustify_cfg = vim.fn.expand("$HOME") .. "/.uncrustify.cfg"
				vim.fn.system({ "uncrustify", "-c", uncrustify_cfg, "--replace", "--no-backup", filepath })
				vim.fn.system({ "perl", vim.fn.expand("$HOME") .. "/.vim/bin/tools/common/ast_post.pl", filepath })
				vim.fn.system({ vim.fn.expand("$HOME") .. "/.config/nvim/tools/cstyle.py", filepath })
			end

			vim.cmd("edit") -- 重新加载格式化后的文件
		end, { buffer = true, desc = "Format source (F4)" })
	end,
})

