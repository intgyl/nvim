local M = {}

vim.g.current_filetype = ""

local function get_filetype(file)
	local ft = vim.filetype.match({ filename = file }) or ""
	vim.g.current_filetype = ft
end

function M.check_argv()
	local argv = vim.fn.argv()
	if #argv > 0 then
		get_filetype(argv[1])
	end
end

return M

