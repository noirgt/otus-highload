-- dialogs-api.lua --
local httpd
local json = require('json')

local function validate(cfg)
    if cfg.host then
        assert(type(cfg.host) == "string", "'host' should be a string containing a valid IP address")
    end
    if cfg.port then
        assert(type(cfg.port) == "number", "'port' should be a number")
        assert(cfg.port >= 1 and cfg.port <= 65535, "'port' should be between 1 and 65535")
    end
end

local function apply(cfg)
    if httpd then
        httpd:stop()
    end
    httpd = require('http.server').new(cfg.host, cfg.port)
    local response_headers = { ['content-type'] = 'application/json' }

    httpd:route({ path = '/dialog/:id/list', method = 'GET' }, function(req)
        local user_id = req:stash('id')
        local dialog_tuple =  box.space.dialogs.index.user_id_idx:select { tonumber(user_id) }

        if not dialog_tuple then
            return { status = 404, body = 'User not found' }
        else
            return { status = 200, headers = response_headers, body = json.encode(dialog_tuple) }
        end
    end)

    httpd:route({ path = '/dialog/:id/send', method = 'POST' }, function(req)
        local user_id = tonumber(req:stash('id'))
        local data = req:json()
        local text = data['text']

        box.space.dialogs:insert { box.sequence.dialog_seq:next(), user_id, text }
        return req:render({ json = { status = 'success', data = { user_id = user_id, text = text } } })
    end)

    httpd:start()
end

local function stop()
    httpd:stop()
end

local function init()
    require('data'):add_sample_data()
end

init()

return {
    validate = validate,
    apply = apply,
    stop = stop,
}
