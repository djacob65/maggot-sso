local cjson = require "cjson"
local resty_random = require "resty.random"
local str = require "resty.string"

-- Fonction pour générer un ID de session unique
local function generate_session_id()
    local random = resty_random.bytes(16)
    return str.to_hex(random)
end

-- Fonction pour gérer les sessions dans lua_shared_dict
function shared_dict_session_store(cache_name)
    local cache = ngx.shared[cache_name]

    return {
        get = function(_, session_id)
            local session_data = cache:get(session_id)
            if session_data then
                return cjson.decode(session_data)
            end
            return nil
        end,

        set = function(_, session_id, session_data, ttl)
            local encoded_data = cjson.encode(session_data)
            cache:set(session_id, encoded_data, ttl)
        end,

        destroy = function(_, session_id)
            cache:delete(session_id)
        end
    }
end
