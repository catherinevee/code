Start-PodeServer --Script Block {
    Add-PodeEndpoint -Address All -Port 80 Protocol Http

    Add-PodeRoute -Method Get -Path / -ScriptBlock {
        Write-PodeHtmlResponse Value @'
<html>
<body>
<h1> heh </h1>
</body>
</html>
'@
    }
}