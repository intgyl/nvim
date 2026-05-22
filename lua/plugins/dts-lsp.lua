-- https://github.com/igor-prusov/dts-lsp
-- cargo install dts-lsp

vim.api.nvim_create_autocmd('FileType', {
    pattern = "dts",
    callback = function (ev)
        vim.lsp.start({
            name = 'dts-lsp',
            cmd = {'dts-lsp'},
	    root_dir = vim.fs.dirname(vim.fs.find({'.git'}, { upward = true })[1]),
        })
    end
})
