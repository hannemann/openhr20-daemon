const mix = require('laravel-mix');

mix.browserSync('127.0.0.1:8020');

mix.sass('src/app.scss', 'dist')
   .js('src/app.js', 'dist')
   .sourceMaps();