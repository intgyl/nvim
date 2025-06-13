local M = {}

M.large_file_threshold = 1024 * 512
vim.g.is_large_file = false

local function check_large_file(file)
	local stat = vim.loop.fs_stat(file)
	if stat and stat.size > M.large_file_threshold then
		vim.g.is_large_file = true
	end
end

function M.check_argv()
	local argv = vim.fn.argv()
	if #argv > 0 then
		check_large_file(argv[1])
	end
end

return M

