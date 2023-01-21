<!DOCTYPE html>
<head>
    % import os
    <base href="{{ base_url }}" data-ws-port="{{ os.getenv("WS_PORT", default='8021') }}">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="static/app.css">
    <script type="module" src="static/app.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8">
</head>
<body>