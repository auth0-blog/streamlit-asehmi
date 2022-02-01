@echo off
IF NOT [%1]==[] (
    copy env.%1 ".env"
    copy package.json.%1 package.json
    echo Set %1 environment! 
) ELSE (
    echo Provide one of 'local', 'prod' as an argument
)
