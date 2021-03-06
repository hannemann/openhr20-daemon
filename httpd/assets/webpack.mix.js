const mix = require('laravel-mix');

mix.browserSync({
    proxy: {
        target: '127.0.0.1:8020',
        ws: true
    },
    watch: true,
    files: [
        './dist/**/*.css',
        './dist/**/*.js'
    ]
});

mix.sass('src/app.scss', 'dist')
   .js('src/app.js', 'dist')
   .sourceMaps();