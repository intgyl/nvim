require("mini.trailspace").setup({
})

vim.keymap.set("n", "<leader>d", function()
	MiniTrailspace.trim()
end, { desc = "Trim trailing whitespace", silent = true, noremap = true })
