function Class(eq_function)
    local Class = {}
    if eq_function ~= nil then
        Class.__eq = eq_function
    end
    Class.__index = Class
    setmetatable(Class, {
        __call =
            function(self, ...)
                local Object = {}
                setmetatable(Object, self)
                Object:New(...)
                return Object
            end
    })
    return Class
end
