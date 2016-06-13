md.recipe.luarocks
==================

This is a zc.buildout recipe that installs luarocks dependencies.

You'll need to have lua and luarocks installed, with the luarocks executable
available on your PATH environment variable.

How to use
----------

Here's an example buildout.cfg configuration ::

    [buildout]
        parts += luarocks

    [luarocks]
    recipe = md.recipe.luarocks
    rocks = 
        lua-cjson
        lua-zlib
        luadbi

Specifying the luarock version number
*************************************

You can specify the luarock version number by adding it after the luarock's
name passed to `rocks`.

**NOTE**: Contrary to when specifying python `eggs` for a recipe, the `rocks` don't
take an assignment operator when version numbers are specified.

For example::

    [buildout]
        parts += luarocks

    [luarocks]
    recipe = md.recipe.luarocks
    rocks = 
        lua-cjson 2.1.0-1
        lua-zlib 0.4-1
        luadbi 0.5-1

Specifying the PATH variables
*****************************

Sometimes, on systems where OS dependencies are installed to an alternative path
to what `luarocks` expects, it's necessary to provide the PATH variables as
well. This is done as follows::

    [buildout]
        parts += luarocks

    [luarocks]
    recipe = md.recipe.luarocks
    rocks = 
        lua-zlib 0.4-1 ZLIB_DIR=$ZLIB_DIR
        luadbi-sqlite3 0.5-1 SQLITE_DIR=$SQLITE_DIR

Specfying the luarocks executable
*********************************

By default the recipe will try to run `luarocks`, expecting it to be an
executable in your PATH. You can specify an alternative exectuable, like so::

    [buildout]
        parts += luarocks

    [luarocks]
    recipe = md.recipe.luarocks
    executable = luarocks-5.1
    rocks = 
        lua-zlib
        luadbi-sqlite3
