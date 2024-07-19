local data = {}

data.add_sample_data =  function()
    box.watch('box.status', function()
        if box.info.ro then
            return
        end

        box.schema.sequence.create('dialog_seq', { if_not_exists = true })
        box.schema.space.create('dialogs', { if_not_exists = true })
        box.space.dialogs:format({
            { name = 'id', type = 'unsigned' },
            { name = 'user_id', type = 'unsigned' },
            { name = 'dialog', type = 'string' }
        })
        box.space.dialogs:create_index('primary_idx', { parts = { 'id' } })
        box.space.dialogs:create_index('user_id_idx', { parts = { 'user_id' }, unique = false })
    end)
end

return data
